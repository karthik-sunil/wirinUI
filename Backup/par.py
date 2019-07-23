import threading
import time
class Hello (threading.Thread):
    def run(self): 
        for i in range(10):
            print("hello")
            time.sleep(1)

class Hi (threading.Thread):
    def run(self): 
        for i in range(10):
            print("hi") 
            time.sleep(1)
obj1 = Hello()
obj2 = Hi()

obj1.start()
obj2.start()

obj1.join()
obj2.join()

print("ok")



