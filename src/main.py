import os,sys

import ollama

from framework.custom_exception import CustomException
from framework.logger import logging

from ETL_Pipeline.entity.config_entity import Settings

from RAG.retrieve.retrieve import SearchEngine
from RAG.Agumented.augment import AugmentPromt

class GenerateAnswer:
    def __init__(self):
        self.settings = Settings()
        self.retriever = SearchEngine()
        self.augment = AugmentPromt()

    def generateAnswer(self,query):
        try:
            logging.info("Generating Answer")

            results = self.retriever.initiate_retrival(query.lower())
            logging.info(f'Successfully initiated retrieval for "{query}" with results: {results}')

            logging.info("Generating Prompt using contex ")
            prompt =  self.augment.create_prompt(query,results)


            response = ollama.chat(
                model=self.settings.llm_model,
                messages=[
                    {
                    'role': 'user',
                    'content': prompt

                }
                ],
            )

            return response
        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)


if __name__ == "__main__":
    input_user_query = input("Please enter your query: ")


    generate_answer = GenerateAnswer()
    response = generate_answer.generateAnswer(input_user_query)

    print(response['message']['content'])