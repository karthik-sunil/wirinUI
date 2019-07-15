import threading
import serial

connected = False
port = 'COM4'
baud = 115200
pktinit = 0
pktheader1 = 255
pktheader2 = 250
pktfooter1 = 11
pktfooter2 = 10
pktdatalen = 5
datalen = 20
pktdata = [None]*datalen
parsedata = []
pktcounter = 0
datacounter = 0
#serial_port = serial.Serial(port, baud)
rxstate = pktinit
ECG=[]
Resp =[]
PPG_IR =[]
PPG_Red =[]
Temperature=[]
def packet_parser(packet):
      return(packet[0]|packet[1]<<8|packet[2]<<16|packet[3]<<24)
def handle_data(data):
    #print(data)
    global rxstate,pktdata,datacounter,ECG,Resp,PPG_IR,PPG_Red,Temperature
    if(rxstate == pktinit):
        if(data == pktheader1):
            #print("Packet Header 1 Found")
            rxstate = data
        return None
    if(rxstate == pktheader1):
        if(data == pktheader2):
            #print("Packet Header 2 Found")
            rxstate = data
        else:
            rxstate = pktinit
        return None
    if(rxstate == pktheader2):
        if(datacounter < datalen):
            pktdata[datacounter] = data
            datacounter+=1
        else:
            ECG.append(packet_parser(pktdata[0:4]))
            Resp.append(packet_parser(pktdata[4:8]))
            PPG_IR.append(packet_parser(pktdata[8:12]))
            PPG_Red.append(packet_parser(pktdata[12:16]))
            Temperature.append(packet_parser(pktdata[16:20]))
            #print(PPG_IR[-1])
            #print(parsedata[-1])
            if(data == pktfooter1):
                #print("Packet Footer 1 Found")
                rxstate = data
                datacounter = 0
    if(rxstate == pktfooter1):
        if(data == pktfooter2):
           # print("Packet Footer 2 Found")
            
            rxstate = pktinit
            return None

def read_from_port(port):
   # while not connected:
   #    #serin = ser.read()
   #     connected = True
        ser = serial.Serial(port, baud)
        while True:
           #print("test")
           reading = ser.read()
           handle_data(int.from_bytes(reading,"little"))
if __name__ == "__main__":
    thread = threading.Thread(target=read_from_port, args=(serial_port,))
    thread.start()
