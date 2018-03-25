#include <stdio.h>
#include <cs50.h>
#include <math.h>

long getUserInput(void);
long lastDigit;
int timesToLoopForFirstDigits;
int timesToLoopForSecondDigits;
int totalSummed;
int sumOfLastDigits;
int sumOfProducts;
int checkSum;

long countFirstDigits(long);
long countSecondDigits(long);
int getSumOfLastDigits(int, long);
int getSumOfProducts(int, long);
int findNumberLength(long);
void printInvalid(void);
void getCreditCardType(long);
bool checkSumCheck(int);
void checkCreditCardNumber(bool, long);


int main(void)
{
    long userInput = getUserInput();
    
    timesToLoopForFirstDigits = countFirstDigits(userInput);
    timesToLoopForSecondDigits = countSecondDigits(userInput);
    
    //find the last digit and everyother digit and sum them 
    sumOfLastDigits = getSumOfLastDigits(timesToLoopForFirstDigits, userInput);
    lastDigit = userInput % 10;
    totalSummed = sumOfLastDigits + lastDigit;

    //find the second to last digit and everyother and get their product and sum them
    sumOfProducts = getSumOfProducts(timesToLoopForSecondDigits, userInput);
    
    checkSum = sumOfProducts + totalSummed;
    
    bool isValid = checkSumCheck(checkSum);
    
    checkCreditCardNumber(isValid, userInput);

    return 0;
}

long getUserInput(void)
{
    long num = 0;
    do
    {
        printf("Number:");
        num = get_long_long();
    }
    while(num < 0 || num >= 9999999999999999);
    
    return num;
}

void getCreditCardType(long num)
{
    long count = 0;
    count = findNumberLength(num);
       
    if(count == 15)
    {
        int firstTwoDigits = num / 10000000000000;
        
        if(firstTwoDigits == 34 || firstTwoDigits == 37)
        {
            printf("AMEX\n"); 
        }
        else
        {
            printInvalid();
        }
        
    }
    else if(count == 16)  
    {   
        int firstTwoDigits = num / 100000000000000;
        int firstDigit = num / 1000000000000000;
        
        if(firstTwoDigits == 51 || firstTwoDigits == 52 || firstTwoDigits == 53 || firstTwoDigits == 54 || firstTwoDigits == 55)
        {
            printf("MASTERCARD\n");
        }
        else if(firstDigit == 4)
        {
            printf("VISA\n"); 
        }
        else
        {
            printInvalid();
        }
    }
    else if(count == 13) 
    {
        int firstDigit = num / 1000000000000;
        
        if(firstDigit == 4)
        {
            printf("VISA\n"); 
        }
        else
        {
            printInvalid();
        }
    }
    else 
    {
        printInvalid();
    }
}


void printInvalid()
{
    printf("INVALID\n");    
}


int getSumOfLastDigits(int num, long ccNumber)
{
    long secondFromLastDigit;
    long moduloDivider = 100;
    
    for(int i=0; i<num; i++)
    {
        secondFromLastDigit = (ccNumber / moduloDivider) % 10;
        moduloDivider *= 100;
        sumOfLastDigits+= secondFromLastDigit;
    }
    return sumOfLastDigits;
}



int getSumOfProducts(int num, long ccNumber)
{
    int product;
    long secondToLastDigit;
    long moduloDivider = 10;
    
    for(int i=0; i<num; i++)
    {
        secondToLastDigit = (ccNumber / moduloDivider) % 10;
        moduloDivider *= 100;
        
        if(secondToLastDigit <=4)
        {
            product = secondToLastDigit * 2;
            sumOfProducts += product;
        }
        else
        {
        switch(secondToLastDigit)
            {
                case 5 :
                {
                    product = 1;
                    sumOfProducts += product;
                    break;
                }
                case 6 :
                {
                    product = 3;
                    sumOfProducts += product;
                    break;
                }
                case 7 :
                { 
                    product = 5;
                    sumOfProducts += product;
                    break;
                }
                case 8 :
                {
                    product = 7;
                    sumOfProducts += product;
                    break;
                }
                case 9 :
                {
                    product = 9;
                    sumOfProducts += product;
                    break;
                }
            }
        }
    }
    return sumOfProducts;
}


long countFirstDigits(long num)
{
    long count=0;
    if(num % 2 != 0)
    {
        count = findNumberLength(num);
        
        return (count/2)+1;
    }
    else
    {
        return countSecondDigits(num);
    }
}



long countSecondDigits(long num)
{
    long count=0;
    count = findNumberLength(num);
    
    return count/2;
}

int findNumberLength(long num)
{
    long count=0;
    while(num>0)
    {
        count++;
        num/=10;
    }
    return count;
}

bool checkSumCheck(int num)
{
    bool isValid = true;
    int lastDigitOfChecksum;
    lastDigitOfChecksum = num % 10;
    
    if(lastDigitOfChecksum != 0)
    {
        isValid = false;
    }
    
    return  isValid;
}

void checkCreditCardNumber(bool valid, long ccNumber)
{
    if(valid)
    {
        getCreditCardType(ccNumber);
    }
    else
    {
        printInvalid(); 
    }
}