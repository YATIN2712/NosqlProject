import sys


filename = sys.argv[1].strip()
#print(filename)


#print(start)
#print(end)
with open(filename,'r') as file:
    data=file.readlines()
    key=None
    val=None
    for line in data:
        line=line.strip()
        if line and line.startswith('#####'):
            key=line
        elif line and (not line.startswith('#####')):
            val=line
        if key and val:
            print(key,'&&&&&',val)
            key=None
            val=None

    