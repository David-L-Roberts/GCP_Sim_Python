from datetime import datetime
import logging
import os

try:
    dir = "Logs"
    os.mkdir(dir)
except FileExistsError:
    pass

FILE_PATH = f"Logs\\Log_{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(
    filename=FILE_PATH, 
    encoding='utf-8', 
    level=logging.DEBUG, 
    format="%(asctime)s.%(msecs)03d |%(levelname)s| \t%(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Log:
    DEBUG       = "|DEBUG|"
    INFO        = "|INFO|"
    WARNING     = "|WARNING|"
    ERROR       = "|ERROR|"
    CRITICAL    = "|CRITICAL|"

    logLevels = {
        "|DEBUG|": logging.debug,
        "|INFO|": logging.info,
        "|WARNING|": logging.warning,
        "|ERROR|": logging.error,
        "|CRITICAL|": logging.critical
    }

    @classmethod
    def log(cls, text: str, logFlag="|INFO|", timeStamp=False, end="\n"):
        """Log text to both terminal and file.

        Args:
            LogFlag (str):  logging prefix flag. Can take one of the following values:  
                |DEBUG|; |INFO|; |WARNING|; |ERROR|; |CRITICAL|
            timeStamp (bool): choose whether terminal logging should include a timestamp.
                File logging will always include a timestamp.
        """

        cls.log_file(text, logFlag)
        cls.log_terminal(text, timeStamp, logFlag, end)

    @classmethod
    def log_terminal(cls, text: str, timeStamp=True, logFlag="|Info|", end="\n"):
        """Add a date and time stamp to the given text.
        Print text to terminal"""
        if timeStamp: print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}:", end="\t")
        print(f"{logFlag} {text}", end=end)

    @classmethod
    def log_file(cls, text: str, logFlag="|Info|"):
        """Add a date and time stamp to the given text and 
        log it to a file."""
        logFunc = cls.logLevels[logFlag]
        logFunc(text)

    # @classmethod
    # def print(cls, text: str, end="\n"):
    #     """Logs plain text to textbox widget and console. No edits."""
    #     print(text, end=end)