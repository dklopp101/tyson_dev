#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include <string.h>

#include "ram.h"

int
load_program(const char* file_path, uint8_t do_silent, void* ram)
{
    FILE*  file;
	size_t file_size;
	size_t bytes_read;

    file = fopen(file_path, "rb");
	
    if (!do_silent)
    {
        if (file == NULL)
        {
            perror("Error opening file");
            return 1;
        }
    }

    // get the file size then rewind file.
    fseek(file, 0, SEEK_END);
    file_size = ftell(file);
    rewind(file);

	// read file into ram
    bytes_read = fread(ram, sizeof(uint8_t), file_size, file);
  	
    if (!do_silent)
    {
        if (bytes_read != file_size)
            perror("Error reading file");
    }

    fclose(file);
    return 0;
}

void*
init_ram(uint32_t size, uint8_t do_silent)
{
	void* ram = malloc(size);
	
    if (!do_silent)
    {
        if (ram == NULL)
        {
            perror("Error allocating furst-vm ram memory!");
            return NULL;
        }
    }

	return ram;
}