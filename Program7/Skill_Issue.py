SENTINEL = [0x0, 0xFF, 0x0, 0x0, 0xFF, 0x0]

def FIND(bits=[], interval=1):
    i=0
    ret = []
    for j in range(0,len(bits),interval):
        bit = bits[j]
        if bit == SENTINEL[i]: #check if sentinal
            i+=1
        else: #add message to list
            i = 0
        ret.append(bit)
        if i == len(SENTINEL): return(ret[:len(ret)-len(SENTINEL)])
    return(None)

from PIL import Image
import sys


def toList(dataType, offset, file):
    # open image in grayscale
    image = Image.open(file).convert("L")
    width, height = image.size
    # set offset
    startY = offset // width
    startX = offset % width
    data = []

    # chatgpt helped with some of this
    # iterates over image
    for y in range(startY, height):
        for x in range(startX if y == startY else 0, width):
            byte_value = image.getpixel((x, y))
    
            if dataType == 'byte':
                data.append(hex(byte_value))
            elif dataType == 'bit':
                bit_value = bin(byte_value)
                data.append(bit_value)

        # reset x after first row
        startX = 0

    # display data collected
    if dataType == 'byte':
        print(f"byte after offset: {data[:10]}")
    elif dataType == 'bit':
        print(f"bit after offset: {data[:10]}")

    return data


def main():
    # takes command line arguments
    dataType = sys.argv[1]
    offset = int(sys.argv[2])
    file = "stegged-bit.bmp"

    print(FIND(toList(dataType, offset, file)))

    

main()
