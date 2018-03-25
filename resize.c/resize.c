/**
 * Copies a BMP piece by piece, just because.
 */
       
#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    char *n = argv[1];
    int enlargeByN = atoi(n);
    
    // ensure proper usage
    if (argc != 4 || enlargeByN < 1 || enlargeByN > 100)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }
    
    BITMAPFILEHEADER new_bf = bf;
    BITMAPINFOHEADER new_bi = bi;
    
    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int new_padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    //biHeight
    new_bi.biHeight = bi.biHeight *= enlargeByN;
    //biWidth
    new_bi.biWidth =  bi.biWidth *= enlargeByN;
    //biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + padding * abs(bi.biHeight)
    new_bi.biSizeImage = ((sizeof(RGBTRIPLE) * new_bi.biWidth) + new_padding) * abs(new_bi.biHeight);
    //bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER)
    new_bf.bfSize = new_bi.biSizeImage + 54;  

    // write outfile's BITMAPFILEHEADER
    fwrite(&new_bf, sizeof(BITMAPFILEHEADER), 1, outptr);
    
    // write outfile's BITMAPINFOHEADER
    fwrite(&new_bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            //increase each pixel by n horizontally
            //for each row
                //for each pixel in row
                    //write to outfile n times
                //write to outfiles padding    
                //skip over infiles padding
            
            //for each row
                //for each pixel
                    //write to array n times
                //for n times
                    //write array to outfile
                    //write outfile padding
                //skip over infile padding

            // write RGB triple to outfile
            fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
        }

        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);

        // then add it back (to demonstrate how)
        for (int k = 0; k < padding; k++)
        {
            fputc(0x00, outptr);
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}

//TODO
//open file
//update outfiles header info
    //file size = bfSize (total size of file pixels, padding, header)
        //bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER)
        //+ sizeof(BITMAPINFOHEADER)
    //image size = biSizeImage (total including pixels and padding)
        //sizeof(RGBTRIPLE) * bi.biWidth + padding * abs(bi.biHeight)
    //width = biWidth (not including padding)
    //height = biHeight
//read infiles scanline, pixel by pixel
//resize horizontally
//remember padding!
//resize vertically

//increase each pixel by n vertically
    //if not multiple of 4 add padding (0x00)
    //find closest multiple above add padding to
    //padding = (4 - (bi.biWidth * (sizeof(RGBTRIPLE)) % 4) % 4