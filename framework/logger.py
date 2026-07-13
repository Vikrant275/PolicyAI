import logging
import sys,os
from datetime import datetime
from framework.fetch_config import GetConfig

script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
# script_name_1 = os.path.splitext(os.path.basename(sys.argv[0]))[1]


root_path = GetConfig('file_path.yaml','root_path').get()
log_path = os.path.join(root_path,GetConfig('file_path.yaml','logs').get())

os.makedirs(log_path, exist_ok=True)
LOG_FILE_PATH = os.path.join(log_path, '{0}_{1}.log'.format(script_name,datetime.now().strftime('%m_%d_%Y_%H_%M_%S')))

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.DEBUG,
    # format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    format = f'%(asctime)s - %(levelname)s - %(message)s - %(name)s - %(lineno)d'
    )

