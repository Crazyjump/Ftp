class xx:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def dd(self):
        print("xx")
    def __call__(self):
        print(self.name)


d=xx("xx",29)
d()