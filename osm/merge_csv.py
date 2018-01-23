

# fout=open("./data/sorted/Sunday.csv","a")  # Sunday
fout=open("./data/sorted/Monday.csv","a")

# first file:
for line in open("./data/sorted/6_6.csv"):
    fout.write(line)
# now the rest:
for num in range(1, 365):
    try:
        f = open("./data/sorted/6_"+str(num)+".csv")
    except IOError as e:
        continue
    f.next()  # skip the header
    for line in f:
        fout.write(line)
    f.close()  # not really needed
fout.close()