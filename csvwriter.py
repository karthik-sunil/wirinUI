import csv 
def filewriter(sentence):
    name = input("enter filename: ")
    filename = name + ".csv"
    print(filename)
    l = sentence.split(",")
    writelist = []
    for i in l:
        writelist.append([float(i)]) 

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(writelist)
    i = 0
    buffer = l 
    #while i<n:
    #    buffer.append(revlist.pop())
    return buffer

sentence = input("enter sentence: ")
#n = int(input("enter length of buffer: "))
l1 = filewriter(sentence)
print(l1)