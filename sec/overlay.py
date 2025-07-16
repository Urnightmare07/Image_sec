import os
from PIL import Image
import sys

if len(sys.argv) != 3:
    print("This takes two arguments; the two images to be combined.")
    exit()

fileA = str(sys.argv[1])
fileB = str(sys.argv[2])

if not os.path.isfile(fileA):
    print("The first file does not exist.")
    exit()

if not os.path.isfile(fileB):
    print("The second file does not exist.")
    exit()

infile1 = Image.open(os.path.join(fileA))
infile2 = Image.open(os.path.join(fileB))
outfile = Image.new('1', infile1.size)

for x in range(infile1.size[0]):
    for y in range(infile1.size[1]):
        outfile.putpixel((x, y), max(
            infile1.getpixel((x, y)), infile2.getpixel((x, y))))

outfile.show('decrypted.png')
