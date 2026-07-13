import os,sys


from framework.logger import logging
from framework.custom_exception import CustomException

from ETL_Pipeline.entity.config_entity import Settings


class AugmentPromt:
    def __init__(self):
        self.settings = Settings()


    def get_contex(self,search_result):
        try:
            logging.info('getting context from search result')

            context_str = ""
            for result in search_result:
                context_text = str(result['payload']['content'])
                context_str += f' {context_text} \n\n'

            return context_str
        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)

    def create_prompt(self,query,context_result):
        try:
            logging.info('creating promt from context result')

            prompt_template = f"""You are an expert HR and Corporate Compliance assistant.
            Your goal is to answer the user's question accurately using ONLY the official company policies provided in the Reference Context below.

            ---
            REFERENCE CONTEXT FROM COMPANY POLICIES:
            {context_result}
            ---

            USER QUESTION:
            "{query}"

            Instructions:
            1. Answer the user's question comprehensively using the facts found in the context above.
            2. Cite the source document name and page number for your claims.
            3. If the context does not contain the answer, state honestly that you do not know. Do not make up information.

            Final Answer:"""

            return prompt_template

        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)


