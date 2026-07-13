import time,os,sys
from pathlib import Path
from datetime import datetime
from time import process_time

from framework.custom_exception import CustomException
from framework.logger import logging

from ETL_Pipeline.entity.config_entity import Settings



class Monitor:
    def __init__(self):
        try:
            self.settings = Settings()
            self.monitor_path = Path(self.settings.pdf_documents_path)

        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)

    def live_monitor(self):
        try:
            logging.info("Starting live monitor")
            tracked_files = {f: f.stat().st_mtime for f in self.monitor_path.glob("*.pdf")}

            while True:
                time.sleep(2)
                current_file = list(self.monitor_path.glob("*.pdf"))

                for file in current_file:
                    current_time = file.stat().st_mtime

                    if file not in tracked_files:
                        print(f'New file detected: {file}')
                        logging.info(f'New file detected: {file}')

                        tracked_files[file] = current_time
                    elif current_time != tracked_files[file]:
                        readable_time = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')

                        print(f'Modified {file.name} was chnaged to {readable_time}')
                        logging.info(f'Modified {file.name} was changed to {readable_time}')

                        tracked_files[file] = current_time


                tracked_files = {f: t for f, t in tracked_files.items() if f.exists()}



        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)


if __name__ == '__main__':

    monitor = Monitor()
    monitor.live_monitor()