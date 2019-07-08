import threading


def start_read():
    global running

    

    
    print("start reading")
    running = True
    
        
    while(running):
        pass
        #print(running)

t1 = threading.Thread(target=start_read, args=()) 
def stop_read():
    global t1
    eegAnimate.event_source.stop()
    if(t1.isAlive()):
        t1.join()
        
        t1 = threading.Thread(target=start_read, args=()) 
    