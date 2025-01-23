from datetime import datetime

def log(text: str, timeStamp=True, logFlag="|Info|"):
    """Log text to both terminal and file.

    Args:
        LogFlag (str):  logging prefix flag. 
                    Can take one of the following values:
                    |Debug|; |Info|; |WARNING|; |ERROR|
    """

    log_file(text, timeStamp, logFlag)
    if logFlag != "|Debug|":
        log_terminal(text, timeStamp, logFlag)

def log_terminal(text: str, timeStamp=True, logFlag="|Info|"):
    """Add a date and time stamp to the given text.
    Print text to terminal"""
    if timeStamp: print(f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}:")
    print(f"\t{logFlag}{text}")

def log_file(text: str, timeStamp=True, logFlag="|Info|"):
    """Add a date and time stamp to the given text and 
    log it to a file."""
    file_path = f"Logs\\Log_{datetime.utcnow().strftime('%Y-%m-%d')}.log"
    with open(file_path, "a") as file:
        if timeStamp: file.write(f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')}:\n")
        file.write(f"\t{logFlag}{text}\n")



def log_btnPress(btn_type: str):
    """Log button press to both terminal and file."""
    message = f"\tButton [{btn_type}] was pressed."
    log_terminal(message)
    log_file(message)
