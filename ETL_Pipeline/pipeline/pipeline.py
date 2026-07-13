from pdfplumber.utils import extract_text

import os,sys
from framework.custom_exception import CustomException
from framework.logger import logging

from ETL_Pipeline.components.extract import Extract
from ETL_Pipeline.components.transform import Transform
from ETL_Pipeline.entity.config_entity import Settings
from ETL_Pipeline.components.load_data import LoadData
from src.utils import *


class Pipeline:
    def __init__(self):
        self.settings = Settings()
        self.extract = Extract()
        self.transform = Transform(self.settings)
        self.load_data = LoadData(self.settings)

    def Extraction(self,path):
        try:
            logging.info('Extracting text from {}'.format(path))
            text_elements = self.extract.pdfextract(path)

            logging.info('Successfully extracted text from {}'.format(path))

            os.makedirs(os.path.dirname(self.settings.text_elem_file_path), exist_ok=True)

            save_pickle(self.settings.text_elem_file_path,text_elements)
            logging.info('Successfully saved text to {}'.format(self.settings.text_elem_file_path))
            return self.settings.text_elem_file_path

        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)

    def Transformation(self,text_element_path):
        try:
            logging.info('loading text from {}'.format(text_element_path))
            text_element = load_pickle(text_element_path)

            logging.info('Transforming text')
            split_chunks = self.transform.split_into_chunks(text_element)

            logging.info('Successfully transformed text into chunks and saving {}'.format(self.settings.chunks_file_path))

            save_pickle(self.settings.chunks_file_path,split_chunks)
            logging.info('Successfully saved chunks to {}'.format(self.settings.chunks_file_path))

            return self.settings.chunks_file_path

        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)

    def Transformation2(self,chunks_file_path):
        try:
            logging.info('loading text from {}'.format(chunks_file_path))
            chunks_elements = load_pickle(chunks_file_path)

            logging.info('Successfully loaded text from {}'.format(chunks_file_path))

            logging.info('Transforming chunks into dense vectors')

            embedded_vectors =[]
            for chunk in chunks_elements:
                embedded_vec = self.transform.convert_dense_vector(chunk.get('content'))
                embedded_vectors.append(embedded_vec)

            vector_matrix = np.array(embedded_vectors, dtype=np.float64)

            logging.info('Successfully transformed chunks into dense vectors')

            logging.info('Saving dense vectors to {}'.format(Settings().embedded_vec_file_path))
            save_array(Settings().embedded_vec_file_path, vector_matrix)
            logging.info('Successfully saved dense vectors to {}'.format(self.settings.embedded_vec_file_path))

            return self.settings.embedded_vec_file_path

        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)

    def load(self,chunk_elements_path,embedded_elements_path):
        try:
            logging.info('Loading text from {} and vectors from {}'.format(chunk_elements_path, embedded_elements_path))

            chunk_elements = load_pickle(chunk_elements_path)
            logging.info('Successfully loaded text from {}'.format(chunk_elements_path))

            embedded_elements = load_array(embedded_elements_path)
            logging.info('Successfully loaded text from {}'.format(embedded_elements_path))

            itrev = self.load_data.load_data(chunk_elements,embedded_elements)

            if itrev:
                logging.info('Successfully store vectors and contex in db')
                return itrev


        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)

    def run_pipeline(self):
        try:
            logging.info('Starting pipeline execution')
            print('starting pipeline execution')

            text_elem_file_path = self.Extraction(self.settings.pdf_documents_path)

            chunks_file_path = self.Transformation(text_elem_file_path)

            embed_vector_file_path = self.Transformation2(chunks_file_path)

            self.load(chunks_file_path,embed_vector_file_path)

            logging.info('Successfully pipeline execution')
            print('successfully pipeline execution')

            return True

        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)











