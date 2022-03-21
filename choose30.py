import sys
import random

if len(sys.argv) < 2:
    print("You need a file")
    exit

sFname = sys.argv[1]
oInfile = open(sFname, "r")
if "txt" in sFname:
    oOutfile1 = open(sFname.replace("txt", "1.txt"), "w")
    oOutfile2 = open(sFname.replace("txt", "2.txt"), "w")
else:
    raise Exception("we need to have a txt file")

for sLine in oInfile:
    nFile = random.randint(0,2)
    if nFile == 0:
        oOutfile1.write(sLine)
    elif nFile == 1:
        oOutfile2.write(sLine)
    else:
        oOutfile1.write(sLine)
        oOutfile2.write(sLine)
oInfile.close()
oOutfile1.close()
oOutfile2.close()

