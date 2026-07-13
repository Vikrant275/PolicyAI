import os,sys
from pathlib import Path
import pdfplumber
import json

from framework.logger import logging
from framework.custom_exception import CustomException
from tenacity import retry, stop_after_attempt, wait_exponential

from ETL_Pipeline.entity.artifact_entity import ExtractedEntity
from ETL_Pipeline.entity.config_entity import Settings

class Extract:
    def __init__(self):
        try:
            self.cache = {}
        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def pdfextract(self,pdf_file_path):
        text_elem = []
        table_elem =[]
        try:
            folder_path = Path(pdf_file_path)
            pdf_files = list(folder_path.glob('*.pdf'))

            for pdf_path in pdf_files:
                logging.info(f"opening [{pdf_path.name}] file ")
                print(f'opening [{pdf_path.name}] file ')

                with pdfplumber.open(pdf_path) as pdf:
                    for page_num, page in enumerate(pdf.pages):
                        if page_num > Settings.from_page:
                            text = page.extract_text()
                            if text:
                                text_elem.append(
                                    {
                                        'content': text,
                                        'page': page_num,
                                        'document_name': pdf_path.name
                                    }
                                )

            return text_elem
        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)


