import os,sys
path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from core import ftp_server_main




if __name__ == "__main__":
    ftp_server_main.main()
