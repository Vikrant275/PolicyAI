import os,sys


from framework.logger import logging
from framework.custom_exception import CustomException

from ETL_Pipeline.entity.config_entity import Settings
from ETL_Pipeline.components.transform import Transform

from qdrant_client import QdrantClient


class SearchEngine:
    def __init__(self):
        try:
            self.settings = Settings()
            self.transform = Transform(self.settings)
            self.path_db = self.settings.path_of_db
            self.COLLECTION_NAME = self.settings.collection_name

            self.client = QdrantClient(path=self.path_db)
            logging.info('Qdrant client initialized')
        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)

    def convert_to_vector(self,query):
        try:
            logging.info('Extracting text from {}'.format(query))

            vector_list = self.transform.convert_dense_vector(query)

            logging.info('Successfully extracted text from {}'.format(query))

            return vector_list

        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)

    def retrieve_contex(self,query_vector,top_k: int=3):
        try:
            logging.info('Retrieving context from collection {} and top {}'.format(self.COLLECTION_NAME,top_k))

            clean_query = [float(x) for x in query_vector]

            search_result = self.client.query_points(
                collection_name=self.COLLECTION_NAME,
                query=clean_query,
                limit=top_k
            )
            retrieved_contexts = []
            for result in search_result.points:
                retrieved_contexts.append({
                    'score': result.score,
                    'payload': result.payload,
                })

            return retrieved_contexts


        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)


    def initiate_retrival(self,query):
        try:
            logging.info('Initiating retrival')

            query_vector_list = self.convert_to_vector(query)
            result = self.retrieve_contex(query_vector_list)

            return result
        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)


if __name__ == '__main__':

    search = SearchEngine()
    query = 'PURPOSE OF THIS POLICY'
    results = search.initiate_retrival(query.lower())
    print(results)

