import os,sys

from dotenv import load_dotenv
load_dotenv()

from framework.custom_exception import CustomException
from framework.logger import logging

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

from ETL_Pipeline.entity.config_entity import Settings

class Transform:
    def __init__(self,settings: Settings):
        self.settings = settings

    def split_into_chunks(self,text_elements):
        try:

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.settings.chunk_size,
                chunk_overlap=self.settings.chunk_overlap,
                separators=self.settings.separators
            )

            text_chunk = []

            for text in text_elements:
                chunks = splitter.split_text(text['content'])
                for chunk in chunks:
                    text_chunk.append({
                        'content': chunk,
                        'metadata':{'page': text['page'],'document': text['document_name']}
                    })
            return text_chunk
        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)

    def convert_dense_vector(self,text_elements):
        try:
            os.environ["HF_TOKEN"] = os.getenv('HF_TOKEN')
            os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
            embedding = SentenceTransformer(
                self.settings.embedding_model,
                local_files_only=True
            )
            embedded_vectors = embedding.encode(text_elements)
            return embedded_vectors
        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)
