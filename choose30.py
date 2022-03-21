import sys
import random

if len(sys.argv) < 2:
    print("You need a file")
    exit

sFname = sys.argv[1]
oInfile = open(sFname, "r")
oOutfile1 = open(sFname + ".1", "w")
oOutfile2 = open(sFname + ".2", "w")


for sLine in oInfile:
    nFile = random.randint(0,3)
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

