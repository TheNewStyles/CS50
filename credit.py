import cs50, sys

def main():
    ccNum = getUserInput()
    if not ccNum is None:
        isCorrectLength = checkLength(ccNum)
        hasPassedCheckSum = checkSum(ccNum)
        if (isCorrectLength and hasPassedCheckSum):
            defineCard(ccNum)
        else:
            print("INVALID")
            
def getUserInput():
    if len(sys.argv) != 2: 
        return
    return int(sys.argv[1])

def checkLength(ccNum):
    print("length")
    length = len(str(ccNum))
    if length == 13 or length == 15 or length == 16:
        return True
    return False

def checkSum(ccNum):
    ccNumStr = str(ccNum)
    products = []
    otherDigits = []
    sum = 0
    
    for i in range(len(ccNumStr)-2 , -1, -2):
        product = (int(ccNumStr[i]) * 2)
        if product < 10:
            products.append(product)
        else:
            list = [int(d) for d in str(product)]
            products.extend(list)
    
    for i in range(len(ccNumStr)-1, -1, -2):
        otherDigits.append(int(ccNumStr[i]))
       
    products.extend(otherDigits)
    
    for i in range(len(products)):
        sum += products[i]
        
    if sum % 10 == 0:
        return True
    else:
        return False

def defineCard(ccNum):
    twoDigits = int(str(ccNum)[:2])
    
    if int(str(ccNum)[:1]) == 4:
        print("VISA")
    elif twoDigits == 34 or twoDigits == 37:
        print("AMEX")
    elif twoDigits == 51 or twoDigits == 52 or twoDigits == 53 or twoDigits == 54 or twoDigits == 55:
        print("MASTERCARD")
    
    
if __name__ == "__main__":
    main()