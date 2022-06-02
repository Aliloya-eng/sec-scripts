#!/user/bin/python3
import json
import sys

print('''
    Usage: escaping4json.py input-file.txt output-file.txt
''')

file = []
input = sys.argv[1]
output = sys.argv[2]
with open(input,"r") as readf:
    for l in readf.readlines():
        file.append((json.dumps(l)[1:-3])+"\n")
readf.close()
print(file)
with open(output,"w") as writef:
    writef.writelines(file)
writef.close()
