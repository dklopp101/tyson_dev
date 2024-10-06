#ifndef RAM_H
#define RAM_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include <string.h>

#define RAMSIZE         0x7FFFFFFF

#define IP_START_ADDR_ADDR 0

int
load_program(const char* file_path, uint8_t do_silent, void* ram);


void*
init_ram(uint32_t size, uint8_t do_silent);

#ifdef __cplusplus
}
#endif

#endif // RAM.H