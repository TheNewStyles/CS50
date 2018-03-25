/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>
#include <stdio.h>
#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false. binary search
 */
bool search(int value, int values[], int n)
{
    int low = 0;
    int high = n-1;
    int mid;
    
    //check if length is greater than 0
    if(n <= 0 || high < low)
    {
        return false;
    }
    
    //binary search
    while(low <= high)
    {
        mid  = low + (high-low)/2;
        
        if(values[mid] == value)
        {
            printf("%i found ", value);
            return true;
        }
        
        else
        {
            if(values[mid] < value)
            {
                low = mid + 1;
            }else
            {
                high = mid - 1;
            }
        }
    }
    
    return 0;
}

/**
 * Sorts array of n values bubble sort
 */
void sort(int values[], int n)
{
    int temp;
    
    for(int i=0, length=n; i<length-1; i++)
    {
        bool swapped = false;
        
        for(int j=0, jlength=n-2; j<=jlength; j++)
        {
            if(values[j] > values[j+1])
            {
                temp = values[j];
                values[j] = values[j+1];
                values[j+1] = temp;
                
                swapped=true;
            }
        }
    }
}
