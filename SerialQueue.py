from queue import Queue
from threading import Thread
import serial
import Logging as Log
import time

class SerialQueue():
    """Starts a thread that holds a queue.
    Will dequeue action codes and send them to the arduino serial.
    After dequeuing a code, it shall wait a configurable time before
    attempting to dequeue the next action code.
    """
    def __init__(self, arduino: serial.Serial, maxsize: int, dequeue_interval_seconds: float) -> None:
        self._arduino = arduino
        self._dequeue_interval_seconds = dequeue_interval_seconds
        self._queue = Queue(maxsize=maxsize)

        self._thread = Thread(target=self._dequeue, daemon=True)
        self._thread.start()
    
    def _dequeue(self):
        """Try to dequeue action code from queue.
        After dequeuing a code, wait before dequeuing again.
        """
        while True:
            # attempt to dequeue an item. Wait until there is an item to dequeue
            action_code = self._queue.get(block=True, timeout=None)
            # send action code to serial port
            self._serial_send_actionCode(action_code)
            # wait before dequeuing again
            time.sleep(self._dequeue_interval_seconds)


    def _serial_send_actionCode(self, action_code):
        """Send action code to the arduino serial."""
        try:
            self._arduino.write(bytes(action_code, 'utf-8'))
        except:
            Log.log(
                text=f"Ardiuno not connected! Cannot write to serial.",
                logFlag="|WARNING|"
            )
        else:
            Log.log(
                text=f"Dequeued the item '{action_code}'. Code sent to serial.",
                logFlag="|Debug|"
            )

    def enqueue(self, action_code: str):
        """Try to place an action code on the queue.
        If queue is full, discard code and log an error message.
        action code should be in the form '<123>', where 123 is the num code.
        """
        try:
            self._queue.put(action_code, block=False)
        except:
            # queue is full. log event.
            Log.log(
                text=f"Failed to enqueue the item '{action_code}'. The queue is full.", 
                logFlag="|ERROR|"
            )
        else:
            # item queued successfully. log event.
            Log.log(
                text=f"Successfully enqueued the item '{action_code}'",
                logFlag="|Debug|"
            )
    
