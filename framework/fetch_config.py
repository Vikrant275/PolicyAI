import sys,os
import yaml
from framework.custom_exception import CustomException
from framework import CONFIG_FILES_PATH

class GetConfig:
    def __init__(self,filename:str=None,arguments:str=None):
        self.filename = filename
        self.arguments = arguments

    def load(self):
        try:
            file = os.path.join(CONFIG_FILES_PATH, self.filename)
            print(f'config loading from {file} ')
            with open(file,'r') as f:
                config = yaml.load(f,Loader=yaml.FullLoader)
            if(config is None):
                raise FileNotFoundError(f'config : [{0}] file not found'.format(file))
            else:
                return config
        except Exception as e:
            raise CustomException(e,sys)

    def get(self):
        try:
            if self.filename and self.arguments is None:
                print("filename or arguments is None")
                return None
            else:
                config = self.load()
                content = config.get(self.arguments)

                return content

        except Exception as e:
            raise CustomException(e,sys)

