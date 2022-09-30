#!/bin/env python3
#
# Remember the times before T9?
# Pass your message as the first argument.
#
# Eg: phone.py "44 33 555 555 666 9 666 777 555 3"
import sys

def main(code):
    code = code.split(" ")
    decode = {
             0:[" "],
             1:[" "],
             2:["A","B","C"],
             3:["D","E","F"],
             4:["G","H","I"],
             5:["J","K","L"],
             6:["M","N","O"],
             7:["P","Q","R","S"],
             8:["T","U","V"],
             9:["W","X","Y","Z"]
             }
    
    for c in code:
        try:
            times = len(c)
            idx = times - 1
            key = int(c[0])
            print(decode[key][idx], end = "")
        except:
            print(c, end = "")
    print()
    return


if __name__ == "__main__":
    try:
        code = sys.argv[1]
    except:
        print(f"Usage: {sys.argv[0]} '44 33 555 555 666 0 9 666 777 555 3'")
        sys.exit(1)
    main(code)
