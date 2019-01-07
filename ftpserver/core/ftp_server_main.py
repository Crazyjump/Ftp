import socketserver
import optparse
from conf import settings
from core import server
class main():
    def __init__(self):
        self.op = optparse.OptionParser()
        #self.op.add_option("-s","--s",dest="server")
        #self.op.add_option("-P","--port",dest='port')
        options,args = self.op.parse_args()
        print(args)
        self.verif_args(options,args)

    def verif_args(self,options,args):
        cmd=args[0]
        if hasattr(self,cmd):
            fun=getattr(self,cmd)
            fun()
    def start(self):
        print(" ftp is working...")
        print(settings.IP)
        s = socketserver.ThreadingTCPServer((settings.IP,settings.PORT), server.myserver)
        s.serve_forever()


