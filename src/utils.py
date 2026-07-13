import pickle,sys
import numpy as np
from framework.custom_exception import CustomException
from framework.logger import logging

def load_pickle(filename_path):
    try:
        logging.info("loading pickle")
        with open(filename_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        logging.error(e)
        raise CustomException(e,sys)

def save_pickle(filename, obj):
    try:
        logging.info("saving pickle")
        with open(filename, 'wb') as f:
            pickle.dump(obj, f)
    except Exception as e:
        logging.error(e)
        raise CustomException(e,sys)

def save_array(filename, array):
    try:
        logging.info("saving array")
        with open(filename, 'wb') as f:
            np.save(f, array)

    except Exception as e:
        logging.error(e)
        raise CustomException(e,sys)

def load_array(filename):
    try:
        logging.info("loading array")
        with open(filename, 'rb') as f:
            return np.load(f)
    except Exception as e:
        logging.error(e)
        raise CustomException(e,sys)