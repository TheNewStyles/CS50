#include <cs50.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

string get_plain_text(void);
int cast_argv_to_int(string);
void print_error(void);
void cipher_loop(int , string);
void print_error(void);
void print_cipher(int, int, int);

#define UPPER_OFFSET 65
#define LOWER_OFFSET 97


int main(int argc, string argv[])
{
    if(argc == 2)
    {
        int k = cast_argv_to_int(argv[1]);
        string plain_text = get_plain_text();
        printf("ciphertext: ");
        cipher_loop(k, plain_text);
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

void cipher_loop(int offset, string user_input)
{
    for(int i=0, length=strlen(user_input); i<length; i++)
        {
            int string_index = (int)user_input[i];
            int string_index_plus_key = string_index + offset;
            
          
            if(isupper(string_index))
            {
                int upper_cipher_int = string_index_plus_key;
                
                print_cipher(upper_cipher_int, string_index_plus_key, UPPER_OFFSET);
                
            }
            else if(islower(string_index))
            {
                int lower_cipher_int = string_index_plus_key;
                
                print_cipher(lower_cipher_int, string_index_plus_key, LOWER_OFFSET);
            }
            else
            {
                printf("%c", string_index);
            }
        }
}

void print_cipher(int cipher, int index_key, int offset)
{
    cipher = index_key - offset;
    
    if(cipher > 25)
    {
        cipher = ((cipher)%26) + offset;
        printf("%c", cipher);
    }
    else
    {
        printf("%c", cipher + offset);
    }
}