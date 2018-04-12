import cs50, sys

def main():
    k = getArgs()
    if k == 1:
        print(1)
    else:
        userInput = getUserInput()
        cipher(k, userInput)
    
def getArgs():
    if len(sys.argv) != 2 or int(sys.argv[1]) < 0:
        return 1
    return sys.argv[1]

def getUserInput():
    print("plaintext: ")
    return cs50.get_string()

def cipher(k, plaintext):
    for i in range(len(plaintext)):
        ascii = ord(plaintext[i].upper())
        indexPlusKey = (ascii + int(k)) - 65
        
        if ascii >= 65 or ascii <= 90:
           if (indexPlusKey > 25):
               cipher = ((indexPlusKey)%26)+65
               print(chr(cipher), end="", flush=True)
           else:
               True
               print(chr(indexPlusKey+65), end="", flush=True)
        else: 
            print(i, end="", flush=True)

if __name__ == "__main__":
    main()