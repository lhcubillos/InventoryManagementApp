f = open("data.txt","r")
f2 = open("data2.txt","w")

for line in f:
    l = line.split(",")
    homeopatia = int(line.split(",")[1])
    if homeopatia == 0:
        l[1] = 'false'
        f2.write(",".join(l))
    else:
        l[1] = 'true'
        f2.write(",".join())
