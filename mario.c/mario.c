#include <stdio.h>
#include <cs50.h>
#include <string.h>

void create_pyramids(int);
void draw_left_pyramid(int,int);
void draw_right_pyramid(int);
int get_int_between_0_23(void);
int spaces;
int bricks;
int height;

int main(void)
{
    height = get_int_between_0_23();
    create_pyramids(height);
}


int get_int_between_0_23(void)
{
    int n = 0;
    
    do
    {
        printf("Height:");
        n = get_int();   
    }
    while(n > 23 || n < 0);
    
    return n;
}

void create_pyramids(int pyramidHeight)
{
    for(int i=0; i<pyramidHeight; i++)
    {
        
        draw_left_pyramid(pyramidHeight, i);

        printf("  ");
                
        draw_right_pyramid(i);
        
        printf("\n");
    }
}

void draw_left_pyramid(int totalHeight, int iterator)
{
    for(int j=0; j< (totalHeight - iterator-1); j++)
    {
        printf(" ");
    }
    
    for(int k=0; k<iterator+1; k++)
    {
        printf("#");
    }
}

void draw_right_pyramid(int iterator)
{
    for(int k=0; k<iterator+1; k++)
    {
        printf("#");
    }
}
