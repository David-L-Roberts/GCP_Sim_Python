from datetime import datetime

def log(text: str, timeStamp=False, logFlag="|Info|", end="\n"):
    """Log text to both terminal and file.

    Args:
        LogFlag (str):  logging prefix flag. Can take one of the following values:  
            |Debug|; |Info|; |WARNING|; |ERROR|
        timeStamp (bool): choose whether terminal logging should include a timestamp.
            File logging will always include a timestamp.
    """

    # log_file(text, logFlag, end)
    # if logFlag != "|Debug|":
    log_terminal(text, timeStamp, logFlag, end)


def log_terminal(text: str, timeStamp=True, logFlag="|Info|", end="\n"):
    """Add a date and time stamp to the given text.
    Print text to terminal"""
    if timeStamp: print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}:", end="\t")
    print(f"{logFlag} {text}", end=end)


def log_file(text: str, logFlag="|Info|", end="\n"):
    """Add a date and time stamp to the given text and 
    log it to a file."""
    file_path = f"Logs\\Log_{datetime.now().strftime('%Y-%m-%d')}.log"
    with open(file_path, "a") as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}:")
        file.write(f"\t{logFlag} {text}{end}")

