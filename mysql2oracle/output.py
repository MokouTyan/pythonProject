import sys
from datetime import date, timedelta

yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
class Logger(object):
    def __init__(self, filename=yesterday+'.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

print('print something')
sys.stdout = Logger(stream=sys.stdout)
# now it works
print("output")