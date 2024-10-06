#ifndef VM_H
#define VM_H

#ifdef __cplusplus
extern "C" {
#endif


#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>

#define TRUE  1
#define FALSE 0

#define WORDSIZE        4
#define DOUBLE_WORDSIZE 8
#define WS              WORDSIZE
#define DWS             DOUBLE_WORDSIZE
#define WS_BITS         32
#define DWS_BITS        64
#define OPCODE_SIZE     1
#define RECUR_MAX       0x3E8
#define STACK_SIZE      100000

#define NOTYPE_CODE     0
#define UINT32_CODE     1
#define INT32_CODE      2 
#define NOSIGN_CODE     3
#define ADDR_CODE       4
#define UINT8_CODE      5

#define UINT_SIZE WORDSIZE
#define INT_SIZE  WORDSIZE
#define BYTE_SIZE 1

#define UINT32_RAM_NSPCT_MSG "ram[%u] (uint32) = %u"
#define INT32_RAM_NSPCT_MSG  "ram[%u] (uint32) = %d"
#define UINT32_STK_NSPCT_MSG "wstk[%u] (uint32) = %u"
#define INT32_STK_NSPCT_MSG  "wstk[%u] (uint32) = %d"
#define UINT8_STK_NSPCT_MSG  "ram[%u] (uint32) = %u"
#define INT8_STK_NSPCT_MSG   "ram[%u] (uint32) = %d"
#define UINT8_RAM_NSPCT_MSG  "ram[%u] (uint32) = %u"
#define INT8_RAM_NSPCT_MSG   "ram[%u] (uint32) = %d"

#define INTERNAL_ERROR_MSG "fvm: encountered an internal error, shutting down."

int
dump_wstk(void* bsp);

int
eval_process(void* ram);

int
run_fbin(const char* file_path);

int main();

// format string thingies:    
//     printf("Signed Integer: %d\n", a);
//     printf("Unsigned Integer: %u\n", b);
//     printf("Float: %f\n", c);
//     printf("Character: %c\n", d);
//     printf("String: %s\n", str);

#ifdef __cplusplus
}
#endif

#endif // VM.