import csv 
def filewriter(sentence1,n):
    name = input("enter filename: ")
    filename = name + ".csv"
    print(filename)
    l = sentence.split(",")
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(l)
    i = 0
    revlist = l[::-1]
    buffer = [] 
    #while i<n:
    #    buffer.append(revlist.pop())
    return revlist

sentence = input("enter sentence: ")
n = int(input("enter length of buffer: "))
l1 = filewriter(sentence,n)
print(l1)