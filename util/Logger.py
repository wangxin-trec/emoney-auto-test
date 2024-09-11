import logging,os,colorlog
from logging.handlers import RotatingFileHandler
from datetime import datetime
import pytz  # Import pytz for timezone handling
from util.Config import ConfigInfo

log_path = ConfigInfo.File.LogPath
if not os.path.exists(log_path): os.mkdir(log_path)

log_colors_config = {
    "DEBUG": "white",
    "INFO": "cyan",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}

default_formats = {
    "color_format": "%(log_color)s%(asctime)s: %(message)s",
    "log_format": "%(asctime)s: %(message)s"
}

class HandleLog:
    def __init__(self):
        self.__now_time = datetime.now().strftime("%Y-%m-%d")
        self.__all_log_path = os.path.join(log_path, self.__now_time + "-all" + ".log")
        self.__error_log_path = os.path.join(log_path, self.__now_time + "-error" + ".log")
        self.__logger = logging.getLogger()
        self.__logger.setLevel(logging.DEBUG)
        
        # Define Tokyo timezone
        self.tokyo_tz = pytz.timezone('Asia/Tokyo')

    @staticmethod
    def __init_logger_handler(log_path):
        logger_handler = RotatingFileHandler(filename=log_path, maxBytes=5 * 1024 * 1024, backupCount=30, encoding="utf-8")
        return logger_handler

    @staticmethod
    def __init_console_handle():
        console_handle = colorlog.StreamHandler()
        return console_handle

    def __format_time(self, record, datefmt=None):
        # Convert UTC time to Tokyo time
        utc_time = datetime.utcfromtimestamp(record.created)
        tokyo_time = utc_time.astimezone(self.tokyo_tz)
        return tokyo_time.strftime(datefmt)

    def __set_log_handler(self, logger_handler, level=logging.DEBUG):
        logger_handler.setLevel(level=level)
        self.__logger.addHandler(logger_handler)

    def __set_color_handle(self, console_handle):
        console_handle.setLevel(logging.DEBUG)
        self.__logger.addHandler(console_handle)

    @staticmethod
    def __set_color_formatter(console_handle, color_config):
        formatter = colorlog.ColoredFormatter(default_formats["color_format"], log_colors=color_config)
        console_handle.setFormatter(formatter)

    def __set_log_formatter(self, file_handler):
        # Use custom formatter for Tokyo time
        formatter = logging.Formatter(fmt=default_formats["log_format"], datefmt="%Y-%m-%d %H:%M:%S")
        formatter.converter = self.__format_time  # Use custom time format function
        file_handler.setFormatter(formatter)

    @staticmethod
    def __close_handler(file_handler):
        file_handler.close()

    def __console(self, level, message):
        all_logger_handler = self.__init_logger_handler(self.__all_log_path)
        error_logger_handler = self.__init_logger_handler(self.__error_log_path)
        console_handle = self.__init_console_handle()
        self.__set_log_formatter(all_logger_handler)
        self.__set_log_formatter(error_logger_handler)
        self.__set_color_formatter(console_handle, log_colors_config)
        self.__set_log_handler(all_logger_handler)
        self.__set_log_handler(error_logger_handler, level=logging.ERROR)
        self.__set_color_handle(console_handle)
        if level == "info":
            self.__logger.info(message)
        elif level == "debug":
            self.__logger.debug(message)
        elif level == "warning":
            self.__logger.warning(message)
        elif level == "error":
            self.__logger.error(message)
        elif level == "critical":
            self.__logger.critical(message)
        self.__logger.removeHandler(all_logger_handler)
        self.__logger.removeHandler(error_logger_handler)
        self.__logger.removeHandler(console_handle)
        self.__close_handler(all_logger_handler)
        self.__close_handler(error_logger_handler)

    def debug(self, message):
        self.__console("debug", message)

    def info(self, message):
        self.__console("info", message)

    def warning(self, message):
        self.__console("warning", message)

    def error(self, message):
        self.__console("error", message)

    def critical(self, message):
        self.__console("critical", message)

logger = HandleLog()