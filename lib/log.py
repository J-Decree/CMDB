import logging
import os
from conf import settings


class PluginLogger(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.error_log_path = settings.ERROR_LOG_FILE
        self.run_log_path = settings.RUN_LOG_FILE
        self.__check_file_exists(self.error_log_path)
        self.__check_file_exists(self.run_log_path)
        self.error_log = None
        self.run_log = None
        self.__init_error_log()
        self.__init_run_log()

    def __check_file_exists(self, file_path):
        if not os.path.exists(file_path):
            raise Exception('%s not exists' % file_path)

    def __init_error_log(self):
        logger = logging.Logger('error_log', logging.error)
        h = logging.FileHandler(self.error_log_path, 'a', encoding='utf8')
        fmt = logging.Formatter(fmt="%(asctime)s - %(levelname)s :  %(message)s")
        h.setFormatter(fmt)
        logger.addHandler(h)
        self.error_log = logger

    def __init_run_log(self):
        logger = logging.Logger('run_log', logging.info)
        h = logging.FileHandler(self.run_log_path, 'a', encoding='utf8')
        fmt = logging.Formatter(fmt="%(asctime)s - %(levelname)s :  %(message)s")
        h.setFormatter(fmt)
        logger.addHandler(h)
        self.run_log = logger

    def log(self, msg, status=True):
        if status:
            self.run_log.info(msg)
        else:
            self.error_log.error(msg)


if __name__ == '__main__':
    p = PluginLogger()
    p.log('love')
