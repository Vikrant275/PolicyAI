import os,sys
from framework.custom_exception import CustomException
from framework.logger import logging

from ETL_Pipeline.entity.config_entity import Settings

from  qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams



class LoadData:

    def __init__(self,settings):
        self.settings = settings

        self.path_db = self.settings.path_of_db
        os.makedirs(self.path_db, exist_ok=True)
        logging.info(f"Created directory {self.path_db}")

        self.COLLECTION_NAME = self.settings.collection_name
        self.VECTOR_SIZE = self.settings.vector_size

        self.client = QdrantClient(path=self.path_db)


    def create_db(self):
        try:

            if not self.client.collection_exists(collection_name=self.COLLECTION_NAME):
                logging.info(f"Collection doesn't exist. Creating fresh collection: {self.COLLECTION_NAME}")
                # self.client.create_collection(self.COLLECTION_NAME)

                # Apply string formatting (.capitalize()) to prevent Pydantic casing errors
                self.client.create_collection(
                    collection_name=self.COLLECTION_NAME,
                    vectors_config=VectorParams(
                        size=self.VECTOR_SIZE,
                        distance=self.settings.distance.capitalize()
                    ),
                )
                logging.info(f"Successfully Created collection {self.COLLECTION_NAME}")
            else:
                logging.info(f"Collection {self.COLLECTION_NAME} already exists. Appending to existing records.")

            return True
        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)

    def load_data(self,chunk_elements,embedded_elements):
        try:
            logging.info(f"Creating points from chunks and embedded elements ")
            if self.create_db() == True:
                num_vectors = embedded_elements.shape[0] if hasattr(embedded_elements, 'shape') else len(embedded_elements)

                if len(chunk_elements) == num_vectors:
                    # Convert numpy elements directly into lists inside structural generator loops
                    points = [
                        PointStruct(
                            id=idx,
                            vector=vectors.tolist() if hasattr(vectors, 'tolist') else list(vectors),
                            payload=payload
                        )
                        for idx, (vectors, payload) in enumerate(zip(embedded_elements, chunk_elements))
                    ]

                    operation = self.client.upsert(
                        collection_name=self.COLLECTION_NAME,
                        wait = True,
                        points = points
                    )

                    print(f"Successfully uploaded {len(points)} points to in-memory Qdrant!")
                    return True

                logging.warn(f'{len(chunk_elements)} chunks were not uploaded in qdrant db')
                print(f'{len(chunk_elements)} chunks were not uploaded in qdrant db')

            logging.error(f'qdrant db was not uploaded at {self.path_db}')
            print(f'qdrant db was not uploaded at {self.path_db}')

            return False
        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)