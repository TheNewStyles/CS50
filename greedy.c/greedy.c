#include <stdio.h>
#include <cs50.h>
#include <math.h>

float get_nonnegative_float(void);
int find_coins(float, int);
int sum_coins(int, int, int, int);
int get_leftOver(int , int);
float changeInCents;
int leftOver;

int main(void)
{
    changeInCents = get_nonnegative_float();
    
    int quarters = find_coins(changeInCents, 25);
    leftOver = get_leftOver(changeInCents , 25);
    
    int dimes = find_coins(leftOver, 10);
    leftOver = get_leftOver(leftOver , 10);
    
    int nickels = find_coins(leftOver, 5);
    leftOver = get_leftOver(leftOver , 5);
    
    int changeDue = sum_coins(quarters, dimes, nickels, leftOver);

    printf("%i\n", changeDue);
}

float get_nonnegative_float(void)
{
    float n = 0;
    
    do
    {
        printf("O hai! How much change is owed? \n");
        n = get_float();
    }
    while(n < 0);
    
    return  round(n*100);
}

int find_coins(float cents, int coinType)
{
    int numCoins = 0;
    
    numCoins = cents/coinType;
    
    return numCoins;
}

int get_leftOver(int change , int coinType)
{
    int num = 0;
    
    return num = change % coinType;
}

int sum_coins(int quarters, int dimes, int nickels, int leftover)
{
    int num = 0;
    
    return num + quarters + dimes + nickels + leftover;
}