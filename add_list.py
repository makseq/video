import json, sys, os


try:
    files = json.load(open('files.json', 'r'))
except:
    files = []

new = os.listdir(sys.argv[1])
new = [f.decode('cp1251') for f in new]
files += new
json.dump(files, open('files.json', 'w'))