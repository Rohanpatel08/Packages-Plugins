import os
import sys
import pathlib
import logging
from datetime import datetime

from autofw.utilities.config_utils import LOG_LEVEL


class CustomLogger:
    TIME_FORMAT = '%d-%m-%y %H-%M-%S'
    LOG_FORMAT = "%(asctime)s[%(filename)s:%(lineno)s:%(funcName)s][%(levelname)s] %(message)s"
    LOG_FILE_NAME = 'Test_Log.log'
    dir_name = 'test_output'

    def __init__(self, log_level=logging.DEBUG):
        self.log_level = log_level
        self.parent_dir = pathlib.Path().absolute()
        self.dir = None
        self.time_stamp = datetime.strftime(datetime.now(), self.TIME_FORMAT)
        self.run_path = None
        self.log_file_path = None
        self._logger = None

    def set_path(self):
        self.dir = self.parent_dir / self.dir_name
        self.run_path = self.dir / pathlib.Path('run_' + self.time_stamp)
        self.log_file_path = self.run_path / self.LOG_FILE_NAME

    def make_log_dir(self):
        is_exist = self.dir.exists()
        if not is_exist:
            os.mkdir(self.dir)
        os.mkdir(self.run_path)

    def add_handlers(self):
        formatter = logging.Formatter(self.LOG_FORMAT, datefmt=self.TIME_FORMAT)

        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(self.log_level)
        stream_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)
        self._logger.addHandler(stream_handler)

    def setup_logger(self, log_dir=None):
        log_dir = pathlib.Path().absolute() if log_dir is None else log_dir
        if isinstance(log_dir, str):
            self.parent_dir = pathlib.Path(log_dir).absolute()
        self.set_path()
        self.make_log_dir()
        self._logger = logging.getLogger('ia_bu_logger')
        self.add_handlers()
        self._logger.setLevel(self.log_level)

    def __getattr__(self, item):
        if self._logger is None:
            pass
        if self._logger and hasattr(self._logger, item):
            return getattr(self._logger, item)
        raise AttributeError(f"Logger does not have the attribute {item}")


logger = CustomLogger(LOG_LEVEL)
