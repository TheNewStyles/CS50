#include <cs50.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

string get_plain_text(void);
int cast_argv_to_int(string);
void print_error(void);
void print_cipher(int , string);
void print_error(void);
void print_lower_case_cipher(int, int);
void print_upper_case_cipher(int, int);

#define UPPER_OFFSET 65
#define UPPER_BOUNDARY 90
#define LOWER_OFFSET 97
#define LOWER_BOUNDARY 122

int main(int argc, string argv[])
{
    if(argc == 2)
    {
        int k = cast_argv_to_int(argv[1]);
        string plain_text = get_plain_text();
        printf("ciphertext: ");
        print_cipher(k, plain_text);
        printf("\n");
        
        return 0;
    }
    else
    {
        print_error();
        return 1;
    }
}


void print_error(void)
{
    printf("Wrong argument count entered\n");
}

string get_plain_text()
{
    string plain_text;
    
    do
    {
        printf("plaintext:");
        plain_text = get_string();
    }
    while(plain_text == NULL);
    
    return plain_text;
}

int cast_argv_to_int(string arg)
{
    int num = atoi(arg);
    
    if(num >= 0)
    {
        return num;
    }
    else
    {
        printf("Changed negative argument to positive \n");
        return num * -1;
    }
}

void print_cipher(int offset, string user_input)
{
    for(int i=0, length=strlen(user_input); i<length; i++)
        {
            int string_index = (int)user_input[i];
            int string_index_plus_key = string_index + offset;
            
            //check if upper case
            if(string_index >= UPPER_OFFSET && string_index <= UPPER_BOUNDARY)
            {
                int upper_cipher_int = (string_index_plus_key)-UPPER_OFFSET;
                
                print_upper_case_cipher(upper_cipher_int, string_index_plus_key);
                
            }
            //check if lower case
            else if(string_index >= LOWER_OFFSET && string_index <= LOWER_BOUNDARY)
            {
                int lower_cipher_int = (string_index_plus_key)-LOWER_OFFSET;
                
                print_lower_case_cipher(lower_cipher_int, string_index_plus_key);
            }
            //or special characters do not change
            else
            {
                printf("%c", string_index);
            }
        }
}

void print_upper_case_cipher(int cipher, int index_key)
{
    cipher = (index_key)-UPPER_OFFSET;
    
    if(cipher > 25)
    {
        cipher = ((cipher)%26) + UPPER_OFFSET;
        printf("%c", cipher);
    }
    else
    {
       printf("%c", cipher + UPPER_OFFSET); 
    }
}

void print_lower_case_cipher(int cipher, int index_key)
{
    cipher = index_key - LOWER_OFFSET;
    
    if(cipher > 25)
    {
        cipher = ((cipher)%26) + LOWER_OFFSET;
        printf("%c", cipher);
    }
    else
    {
        printf("%c", cipher + LOWER_OFFSET);
    }
}