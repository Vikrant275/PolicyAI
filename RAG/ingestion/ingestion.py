import os,sys

from framework.logger import logging
from framework.custom_exception import CustomException

from ETL_Pipeline.entity.config_entity import Settings
from ETL_Pipeline.pipeline.pipeline import Pipeline


class DataIngestion:
    def __init__(self):
        self.settings = Settings()
        self.pipeline = Pipeline()

    def initiate_data_ingestion(self):
        try:
            logging.info("Initiating data ingestion")
            self.pipeline.run_pipeline()
            logging.info("Finished data ingestion")
        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)


if __name__ == "__main__":

    dataingestion = DataIngestion()
    dataingestion.initiate_data_ingestion()