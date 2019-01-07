import os
IP="127.0.0.1"
PORT=8090
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACCOUNT_PATH = os.path.join(BASE_DIR,"conf","user.cfg")
#print(ACCOUNT_PATH)