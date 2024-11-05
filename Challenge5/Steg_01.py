import argparse
import sys

# sentinel to look for
SENTINEL = bytearray([0x00, 0xff, 0x00, 0x00, 0xff, 0x00])

# storing hidden bytes in image
def storeByte(wrapper, hidden, offset, interval):
    i = 0
    while i < len(hidden):
        wrapper[offset] = hidden[i]
        offset += interval
        i += 1

    # hides sentinel in message
    for byte in SENTINEL:
        wrapper[offset] = byte
        offset += interval

    return wrapper
    
def BinaryDecode(code, bit):
    # We first convert the string to an array and remove the newline character
    bruh = bin(int.from_bytes(code, byteorder=sys.byteorder))
    ar = list(bruh)
    del ar[-1]
    
    # variable setup #
    decrypted = [] # we will store solved elements of the message here
    tempstr = "" # we will store binary characters here until they are ready to be solved
    group = 0 # this will keep track of if we've reached the bit size
    index = 0 # iterates through the entire array once

    # iterates through the entire array while 
    # repeatedly building chunks of size bit
    while index < len(ar):
        tempstr += ar[index]
        index += 1
        group += 1
        if group >= bit: # this means tempstr is ready to convert
            decrypted += "".join([chr(int(tempstr, 2))]) # we cast the string to an int, then the int to it's respective char
            
            # we clear temstr and group to start again
            tempstr = ""
            group = 0
    
    # we merge the array to a string and print it
    printstr = "".join(decrypted)
    print(printstr)


# get bytes from image
def retrieveByte(wrapper, offset, interval):
    hidden = bytearray()
    sentinel_index = 0

    while offset < len(wrapper):
        byte = wrapper[offset]
        hidden.append(byte)
        offset += interval
        
        if byte == SENTINEL[sentinel_index]:
            sentinel_index += 1
            if sentinel_index == len(SENTINEL):
                break
        else:
            sentinel_index = 0

    return hidden[:-len(SENTINEL)]

# store hidden bits in image
def storeBit(wrapper, hidden, offset):
    for byte in hidden + SENTINEL:
        for bit in range(8):
            wrapper[offset] &= 0b11111110
            wrapper[offset] |= (byte >> (7 - bit)) & 0b00000001
            offset += 1
    return wrapper

# get bits from image
def retrieveBit(wrapper, offset):
    hidden = bytearray()
    i = 0

    while offset < len(wrapper):
        byte = 0
        for bit in range(8): #Honestly no clue if this works but it doesnt follow the byte method i think -JF
            byte = (byte << 1) | (wrapper[offset] & 0b00000001)
            offset += 1

        hidden.append(byte)

        if byte == SENTINEL[i]:  # Check if sentinel
            i += 1
        elif byte==0x0: i=1 #0+0 --go back to pos 1
        elif i==3 and byte==SENTINEL[1]: i=2 #0F0+F --go back to OF
        else: i=0 #restart counter
        
        if i==6:
            return(new[:(len(new)-len(SENTINEL))])

    return hidden #Why is the return different than the Byte method? -JF

def main():
    # get arguments from command line
    # chatgpt helped here
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", action="store_true", help="Store data")
    parser.add_argument("-r", action="store_true", help="Retrieve data")
    parser.add_argument("-b", action="store_true", help="Bit mode")
    parser.add_argument("-B", action="store_true", help="Byte mode")
    parser.add_argument("-o", type=int, default=0, help="Offset (default 0)")
    parser.add_argument("-i", type=int, default=1, help="Interval (default 1)")
    parser.add_argument("-w", required=True, help="Wrapper file")
    parser.add_argument("-H", required=False, help="Hidden file")

    args = parser.parse_args()

    # opens file and get bytes
    with open(args.w, "rb") as f:
        wrapper = bytearray(f.read())

    # if store then it stores bytes or bits
    if args.s:
        with open(args.h, "rb") as f:
            hidden = bytearray(f.read())
        if args.B: # bytes
            wrapper = storeByte(wrapper, hidden, args.o, args.i)
        elif args.b: # bits
            wrapper = storeBit(wrapper, hidden, args.o)
            BinaryDecode(wrapper, 7)
            BinaryDecode(wrapper, 8)
        # output new file
        sys.stdout.buffer.write(wrapper)

    # retrieve data
    elif args.r:
        if args.B: # bytes
            hidden = retrieveByte(wrapper, args.o, args.i)
        elif args.b: # bits
            hidden = retrieveBit(wrapper, args.o)
        # output retrieved data
        sys.stdout.buffer.write(hidden)

main()