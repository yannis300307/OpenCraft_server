import time
from config import *

class Logs:  # gère les logs
    def __init__(self):
        time_ = time.localtime()
        self.logs_name = "Logs " + time.strftime("%Y-%m-%d - %Hh %Mm %Ss", time_) + ".logs"
        self.write("-" * 20 + time.strftime("%Y/%m/%d - %H:%M:%S", time_) + "-" * 20, False)

    def write(self, msg, print_=True):  # permet d' écrire un log
        t = open(DEFAULT_LOGS_PATH + "\\" + self.logs_name, "a")
        t.writelines(["\n" + str(msg)])
        t.close()
        if print_:
            print("\b" * 3 + str(msg) + "\n> ", end="")
