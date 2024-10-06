#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>

#define build_optable()                   \
    void* optable[34] = {                 \
        &&die,                            \
        &&nop,                            \
        &&call,                           \
        &&ret,                            \
        &&jmp,                            \
        &&je,                             \
        &&jn,                             \
        &&jl,                             \
        &&jg,                             \
        &&loop,                           \
        &&lcont,                          \
        &&lbrk,                           \
        &&push,                           \
        &&pop,                            \
        &&pop2,                           \
        &&popn,                           \
        &&pushfh,                         \
        &&popth,                          \
        &&movth,                          \
        &&stkth,                          \
        &&cpyh,                           \
        &&seth,                           \
        &&pshfhh,                         \
        &&pshfhs,                         \
        &&inc,                            \
        &&dec,                            \
        &&add,                            \
        &&sub,                            \
        &&mul,                            \
        &&div,                            \
        &&mod,                            \
        &&nspct,                          \
        &&nspctst,                        \
        &&test_die                        \
    };

#define SP_START_ADDR 0xFFFF

#define RECUR_MAX 0x3E8

#define PROGRAM_START_BYTE 0x00

#define exec_next() goto *optable[RAM[PC]]

inline
int
load_program(const uint8_t* file_path, int16_t* RAM)
{
    FILE *file;
	size_t file_size;
	size_t bytes_read;

    file = fopen(file_path, "rb");
	
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }

    // Get the file size then rewind file.
    fseek(file, 0, SEEK_END);
    file_size = ftell(file);
    rewind(file);

	// read file into RAM
    bytes_read = fread(RAM, sizeof(uint8_t), file_size, file);
	
    if (bytes_read != file_size) {
        perror("Error reading file");
    }

    fclose(file);
    return 0;
}

inline
int16_t*
init_RAM(const uint8_t* file_path)
{
	int err;
	
	// get some memory for the RAM.
	int16_t* RAM = (int16_t*) malloc(sizeof(int16_t) * 0xFFFF);
	
	if (RAM == NULL) {
        perror("Error allocating furst-vm RAM memory!");
        return (int16_t*) NULL;
    }
	
	// load program into RAM.
	err = load_program(file_path, RAM);
	if (err) return (int16_t*) NULL;
	
	return RAM;
}

inline 
int16_t
eval_process(int16_t* RAM) 
{
    build_optable();

	uint16_t  CSTK[RECUR_MAX];    // call-stack.
    uint16_t  PC;                 // program-counter.
    uint16_t  LC = 0;             // loop-counter.
    uint16_t  LB;                 // loop-body addr.
    uint16_t  LE;                 // loop-end addr.
    uint16_t  SP = SP_START_ADDR; // stack-pointer address.
    uint16_t  CP = 0x00;          // call-stack pointer address.
	int       RETC = 0;           // vm return-state-code.   
	
	// start execution.
    exec_next();

    die:
        free(RAM);
        return (int16_t) RETC;

    nop:
        PC++;
        exec_next();

    call:
        CP++;
        CSTK[CP] = RAM[PC+2];
        PC = RAM[PC+1];
        exec_next();

    ret:
        PC = RAM[CSTK[CP]];
        CP--;
        exec_next();

    jmp:
        PC = RAM[PC+1];
        exec_next();

    je:
        if (RAM[SP] == RAM[SP-1])
            PC = RAM[PC+1];
        else
            PC += 2;
        exec_next();

    jn:
        if (RAM[SP] != RAM[SP-1])
            PC = RAM[PC+1];
        else
            PC += 2;
        exec_next();

    jl:
        if (RAM[SP] < RAM[SP-1])
            PC = RAM[PC+1];
        else
            PC += 2;
        exec_next();

    jg:
        if (RAM[SP] > RAM[SP-1])
            PC = RAM[PC+1];
        else
            PC += 2;
        exec_next();

    loop:
        LC = 0;
        LB = RAM[PC+1];
        LE = RAM[PC+2];
        PC = LB;
        exec_next();

    lcont:
        LC--;
        if (LC)
            PC = LB;
        else
            PC = LE;
        exec_next();

    lbrk:
        PC = LE;
        exec_next();

    push:
        SP++;
        RAM[SP] = RAM[PC+1];
        PC += 2;
        exec_next();

    pop:
        SP--;
        PC++;
        exec_next();

    pop2:
        SP -= 2;
        PC++;
        exec_next();

    popn:
        SP -= RAM[PC+1];
        PC += 2;
        exec_next();

    pushfh:
        SP++;
        RAM[SP] = RAM[RAM[PC+1]];
        PC += 2;
        exec_next();

    popth:
        RAM[PC+1] = RAM[SP];
        SP--;
        PC++;
        exec_next();

    movth:
        RAM[PC+1] = RAM[SP];
        PC++;
        exec_next();

    stkth:
        RAM[PC+1] = RAM[SP];
        PC++;
        exec_next();

    cpyh:
        RAM[PC+1] = RAM[PC+2];
        PC += 2;
        exec_next();

    seth:
        RAM[PC+1] = RAM[RAM[PC+2]];
        PC += 2;
        exec_next();

    pshfhh:
		RAM[++SP] = RAM[RAM[++PC]];
		PC++;
		exec_next();
        
    pshfhs:
		RAM[++SP] = RAM[RAM[SP-1]];
		PC++;
		exec_next();

    inc:
        RAM[SP]++;
        PC++;
        exec_next();

    dec:
        RAM[SP]--;
        PC++;
        exec_next();

    add:
        RAM[++SP] = RAM[SP] + RAM[SP-1];
        SP++;
        PC++;
        exec_next();

    sub:
        RAM[++SP] = RAM[SP] - RAM[SP-1];
        SP++;
        PC++;
        exec_next();

    mul:
        RAM[++SP] = RAM[SP] * RAM[SP-1];
        SP++;
        PC++;
        exec_next();

    div:
        RAM[++SP] = RAM[SP] * RAM[SP-1];
        SP++;
        PC++;
        exec_next();

    mod:
        RAM[++SP] = RAM[SP] % RAM[SP-1];
        SP++;
		PC++;
        exec_next();

    nspct:
        printf("RAM[%" PRIu16 "] = %" PRId16 "\n", RAM[++PC], RAM[++PC]);
        PC++;
        exec_next();

    nspctst:
        printf("RAM[SP] = %" PRId16 "\n", RAM[SP]);
        exec_next();

    test_die:
        return (int) RAM[SP];
}


int16_t
run_furst(const uint8_t* prog_file_path)
{
	// initialise RAM.
	int16_t* RAM = init_RAM(prog_file_path);
	int16_t  retval;
	
	if (RAM == NULL) return 1;
	
	return eval_process(RAM);
}

int main() {
	int16_t retval = run_furst("testy.fbin");
	if (!retval) {
		printf("\n furst-vm ran successfully!\ntop-stack: %d", retval);
	} else {
		printf("furst-vm encountered an issue!");
	}
	
    return 0; // Return a value to match the function's return type
}