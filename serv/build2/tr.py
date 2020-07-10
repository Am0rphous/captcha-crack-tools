import os
from zipfile import ZipFile
zip = ZipFile('hydrants error.zip')
zip.extractall('hydrants error')


"""
print "PARSE"
path = "data"
valid_images = [".jpg",".png"]
for r, d, f in os.walk(path):
    #print r, d, f
    for file in f:
        if valid_images[0] in file or valid_images[1] in file:
           pass#print os.path.join(r, file)
        if ".csv" in file:
           print os.path.join(r, file)
"""
