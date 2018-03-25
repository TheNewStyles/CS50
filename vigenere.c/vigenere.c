#include <cs50.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define UPPER_OFFSET 65
#define LOWER_OFFSET 97


string get_plain_text(void);
void print_cipher(int, int, int);
int get_cipher(int , string, int);

int main(int argc, string argv[])
{
    if(argc != 2)
    {
        printf("Wrong amount of arguments entered into command line.");
        return 1;
    }
    
    string arg = argv[1];
    
    for(int i=0, length = strlen(arg); i<length; i++)
    {
        if(!isalpha(arg[i]))
        {
            printf("Please enter only alphanumeric arguments");
            return 1;
        }
    }
    
    string plain_text = get_plain_text();
    int arg_length = strlen(argv[1]);
    
    printf("ciphertext:");
    
    for(int i=0, k=0, length=strlen(plain_text); i<=length; i++)
    {
        int string_index = plain_text[i];
        char cipher;
       
        if( (plain_text[i]>='a' && plain_text[i]<='z') || (plain_text[i]>='A' && plain_text[i]<='Z'))
        {
            cipher = get_cipher(k, arg, arg_length);
            k++;
        }
        else
        {
            cipher = get_cipher(k, arg, arg_length);
        }
       
        if(isupper(string_index))
        {
            print_cipher(string_index, cipher, UPPER_OFFSET);
        }
        else if(islower(string_index))
        {
            print_cipher(string_index, cipher, LOWER_OFFSET);
        }
        else if (plain_text[i] != '\0')
        {
            printf("%c", plain_text[i]);
        }
    }
    printf("\n");
}

string get_plain_text()
{
    string plain_text;
    printf("plaintext:");
    plain_text = get_string();

    return plain_text;
}


void print_cipher(int string_index, int cipher, int offset)
{
    int index = (string_index+cipher)-offset;
    
    if(index > 25)
    {
        index = ((index)%26) + offset;
        printf("%c", index);
    }
    else
    {
      printf("%c", index + offset); 
    }
}

int get_cipher(int iterator, string argv1, int arglength)
{
    int arg_index = argv1[iterator];
    int index = ((iterator)%arglength);
    arg_index = argv1[index];
    int cipher = toupper(arg_index)-UPPER_OFFSET;
    return cipher;
}