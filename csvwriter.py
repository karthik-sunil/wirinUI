import csv 

def filewriter(sentence,filename, annotation,systime):
    if(not filename[-3:] == "csv"):
        filename = filename + ".csv"
    l = sentence.split(",")
    a = []
    for i,x in enumerate(l):
        l[i] = float(l[i])
        a.append([systime,l[i],annotation])
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(a)
    i = 0
    buffer = [] 
    return l

def filewriterBCI(data,filename, annotation,systime):
    filename = "E:\\Coding\\Wirin\\wirinUI\\newFile2.csv"
    
    a = [[systime] + data + [annotation]]
    
    with open(filename, "a", newline="") as f:
        print(f)
        writer = csv.writer(f)
        writer.writerows(a)
  
    