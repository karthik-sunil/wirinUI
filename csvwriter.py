import csv 

def filewriter(sentence,filename, annotation,systime):
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
