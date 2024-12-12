import io
import sys
import threading
import time
from contextlib import redirect_stdout

def run():
    with io.StringIO() as stream:

        with redirect_stdout(stream):
            print("Hallo ich bin die Nachricht die du willst2")
            time.sleep(3)
            print("Hallo ich bin die Nachricht die du willst")
        print("test")
        print(stream.getvalue())

thread = threading.Thread(target=run)
thread.start()

time.sleep(1)
print("Ich bin draußen")
thread.join()

print("Ende")