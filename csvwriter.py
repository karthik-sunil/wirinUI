import csv 
def filewriter(sentence,filename, annotation,systime):
    #name = input("enter filename: ")
    filename = filename + ".csv"
    print(filename)
    print(sentence)
    l = sentence.split(",")
    a = []
    for i,x in enumerate(l):
        l[i] = float(l[i])
        a.append([systime,l[i],annotation])
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(a)
    i = 0
    #revlist = l[::-1]
    buffer = [] 
    #while i<n:
    #    buffer.append(revlist.pop())
    return l
