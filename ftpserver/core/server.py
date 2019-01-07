import socketserver,os
import json
import configparser
from conf import settings
class myserver(socketserver.BaseRequestHandler):
    def handle(self):
        while 1 :
            #conn=self.request
            data=self.request.recv(1024).strip()
            data=json.loads(data.decode("utf8"))
            if data.get("action"):
                if hasattr(self,data.get("action")):
                    func=getattr(self,data.get("action"))
                    func(**data)
                else:
                    print("Invalid cmd")
            else:
                print("Invalid cmd")


    def send_response(self,state_code):
        response={"status_code":state_code}
        self.request.sendall(json.dumps(response).encode("utf8"))
    def auth(self,**data):

        username=data["username"]
        password=data["password"]
        user=self.authenticate(username,password)

        if user:
            self.send_response(254)
        else:
            self.send_response(253)


    def authenticate(self,user,pwd):
        cfg=configparser.ConfigParser()
        cfg.read(settings.ACCOUNT_PATH)

        if user in cfg.sections():

            if cfg[user]["Password"]==pwd:
                self.user=user
                self.mainpath= os.path.join(settings.BASE_DIR,"home",self.user)
                print("passed authentication")
                return user
    def put(self,**data):
        file_name=data.get("file_name")
        file_size=data.get("file_size")
        target_path=data.get("target_path")
        abs_path = os.path.join(self.mainpath,target_path,file_name)
        has_received = 0
        if os.path.exists(abs_path):
            file_has_size = os.stat(abs_path).st_size
            if file_has_size < file_size:
                self.request.sendall("800".encode("utf8"))
                choice=self.request.recv(1024).decode("utf8")
                if choice == "Y":
                    self.request.sendall(str(file_has_size).encode("utf8"))
                    has_received+=file_has_size
                    f = open(abs_path,"ab")
                else:
                    f=open(abs_path,"wb")
            else:
                self.request.sendall("801".encode("utf8"))
                return
        else:
            self.request.sendall("802".encode("utf8"))
            f=open(abs_path,"wb")
        while has_received < file_size:
            try:
                data = self.request.recv(1024)
            except Exception as e:
                break
            f.write(data)
            has_received+= len(data)
        f.close()

    def ls(self,**data):
        file_list=os.listdir(self.mainpath)
        file_dir = "\n".join(file_list)
        if not len(file_list):
            file_dir="dir empty "
        data = self.request.sendall(file_dir.encode("utf8"))
    def mkdir(self,**data):
        dirname = data.get("dirname")
        path = os.path.join(self.mainpath,dirname)
        if not os.path.exists(path):
            if "/" in dirname:
                os.makedirs(path)
            else:
                os.mkdir(path)
            self.request.sendall("dirname is success".encode("utf8"))
        else:
            self.request.sendall("dirname is exists".encode("utf8"))




    def cd(self,**data):
        dirname=data.get("dirname")
        if dirname == "..":
            self.mainpath=os.path.dirname(self.mainpath)
        else:
            self.mainpath = os.path.join(self.mainpath,dirname)
        self.request.sendall(self.mainpath.encode("utf8"))



