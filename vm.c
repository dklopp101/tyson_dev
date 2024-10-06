#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include <string.h>

#include "opcode.h"
#include "ram.h"
#include "vm.h"

// macros used for extracting values/calculating addrs from specific pointers.
#define getOpcode()                   (*((uint8_t*) ip))
#define getOprVal(TYPE)               (*((TYPE*) ip))
#define getTopStkVal(TYPE)            (*((TYPE*) sp))
#define getNextOprVal(TYPE)           (*((TYPE*) (ip += WS)))   // NOTE: this macro actually mutates ip directly!
#define getRamVal(TYPE, ADDR)         (*((TYPE*) (ram + ADDR)))
#define getStkVal(TYPE, ADDR)         (*((TYPE*) (sp + ADDR)))
#define getNegTopStkVal(TYPE, OFFSET) (*((TYPE*) sp - OFFSET)) 
#define calcRelativeRamAddr(POINTER)  ((POINTER) - ram)

// address 0 of ram contains the program starting address(main label).
// so we deref that as a uint32 then add to ram to get a ptr to start instr.
#define programStart                  (ram + (*(uint32_t*) (ram))); 

// goto for jumping to next program operation.
#define nextop()                      goto *optable[getOpcode()]

int
dump_wstk(void* bsp)
{
	return 0;
}

int
eval_process(void* ram) 
{
	build_optable();

	uint8_t   wstk[STACK_SIZE];   // work-stack.
	void*     bsp = (void*) wstk; // stack-base-pointer.
	void*     rstk[RECUR_MAX];    // return-stack.
    void*     ip = programStart   // instr-pointer.
    uint32_t  lc = 0;             // loop-counter 
    void*     lb;                 // loop-base instr-ptr.
	void*     le;                 // loop-end instr-ptr
    void*     sp = (void*) wstk;  // stack-pointer.
    void*     rp = rstk;          // return-pointer.
	uint32_t* uint32_ptr;         // uint32-arithmetic-pointer.
	int32_t*  int32_ptr;          // int32-arithmetic-pointer.
	uint32_t  uint32_buf[2];      // uint32-data-buffers.
	int32_t   int32_buf[2];       // int32-data-buffers.
	int       retc = 0;

	// program execution begins here.
    nextop();

	// operation handling code.
    die:
        printf("\nexecuting-ram-addr[%d] die op", calcRelativeRamAddr(ip));
        free(ram);
        return retc;

    nop:
        printf("\nexecuting-ram-addr[%d] nop op", calcRelativeRamAddr(ip));
        ++ip;
        nextop();

    nspctr:
        printf("\nexecuting-ram-addr[%d] nspct op", calcRelativeRamAddr(ip));
		++ip;

		switch (getOprVal(uint8_t)) {
			case UINT32_CODE: 
				++ip;
				printf(UINT32_RAM_NSPCT_MSG, getOprVal(uint32_t), getRamVal(uint32_t, getOprVal(uint32_t)));
				break;

			case INT32_CODE: 
				++ip;
				printf(INT32_RAM_NSPCT_MSG, getOprVal(uint32_t), getRamVal(uint32_t, getOprVal(uint32_t)));
				break;

			case UINT8_CODE: 
				++ip;
				printf(UINT8_RAM_NSPCT_MSG, getOprVal(uint32_t), getRamVal(uint8_t, getOprVal(uint32_t)));
				break;

			default:
				printf(INTERNAL_ERROR_MSG);
				goto die;
		}		

		ip += WS;
        nextop();

    nspctst:
        printf("\nexecuting-ram-addr[%d] nspctst op", calcRelativeRamAddr(ip));
		++ip;

		switch (getOprVal(uint8_t)) {
			case UINT32_CODE: 
				++ip;
				printf(UINT32_STK_NSPCT_MSG, getOprVal(uint32_t), getStkVal(uint32_t, getOprVal(uint32_t)));
				break;

			case INT32_CODE: 
				++ip;
				printf(INT32_STK_NSPCT_MSG, getOprVal(uint32_t), getStkVal(uint32_t, getOprVal(uint32_t)));
				break;

			case UINT8_CODE: 
				++ip;
				printf(UINT8_STK_NSPCT_MSG, getOprVal(uint32_t), getStkVal(uint8_t, getOprVal(uint32_t)));
				break;

			default:
				printf(INTERNAL_ERROR_MSG);
				goto die;
		}		

		ip += WS;
        nextop();

    test_die:
        printf("\nexecuting-ram-addr[%d] test_die op", calcRelativeRamAddr(ip));
		return retc;

    call:
        printf("\nexecuting-ram-addr[%d] call op", calcRelativeRamAddr(ip));
		++rp;
		++ip;
		rp = ip + WS;
		ip = ram + getOprVal(uint32_t);
        nextop();

    ret:
        printf("\nexecuting-ram-addr[%d] ret op", calcRelativeRamAddr(ip));
		ip = rp;
		--rp;
        nextop();

    swtch:
        printf("\nexecuting-ram-addr[%d] swtch op", calcRelativeRamAddr(ip));
        printf("\nUNIMPLEMNTED OPCODE!");
        nextop();

    jmp:
        printf("\nexecuting-ram-addr[%d] jmp op", calcRelativeRamAddr(ip));
		++ip;
		ip = ram + getOprVal(uint32_t);
        nextop();

    je:
        printf("\nexecuting-ram-addr[%d] je op", calcRelativeRamAddr(ip));
		++ip;
		if (!memcmp(sp, sp + WS, WS)) 
			ip = ram + getOprVal(uint32_t); 
		else
			ip += WS; 
        nextop();

    jn:
        printf("\nexecuting-ram-addr[%d] jn op", calcRelativeRamAddr(ip));
		++ip;
		if (memcmp(sp, sp + WS, WS)) 
			ip = ram + getOprVal(uint32_t); 
		else
			ip += WS;
        nextop();

    jl:
        printf("\nexecuting-ram-addr[%d] jl op", calcRelativeRamAddr(ip));
		++ip;
		if ((*(uint32_t*) sp) < (*(uint32_t*) sp - WS)) 
			ip = ram + getOprVal(uint32_t); 
		else
			ip += WS;
        nextop();

    jg:
        printf("\nexecuting-ram-addr[%d] jg op", calcRelativeRamAddr(ip));
		++ip;
		if ((*(uint32_t*) sp) > (*(uint32_t*) sp - WS)) 
			ip = ram + getOprVal(uint32_t); 
		else
			ip += WS;
        nextop();

    jls:
        printf("\nexecuting-ram-addr[%d] jl op", calcRelativeRamAddr(ip));
		++ip;
		if ((*(int32_t*) sp) < (*(int32_t*) sp - WS)) 
			ip = ram + getOprVal(int32_t); 
		else
			ip += WS;
        nextop();

    jgs:
        printf("\nexecuting-ram-addr[%d] jg op", calcRelativeRamAddr(ip));
		++ip;
		if ((*(int32_t*) sp) > (*(int32_t*) sp - WS)) 
			ip = ram + getOprVal(int32_t); 
		else
			ip += WS;
        nextop();
		
    loop:
        printf("\nexecuting-ram-addr[%d] loop op", calcRelativeRamAddr(ip));
		lc = 0;
		++ip;
		lc = getOprVal(uint32_t);
		ip += WS;
		lb = ram + getOprVal(uint32_t); 
		ip += WS;
		le = ram + getOprVal(uint32_t); 
		ip += WS;
        nextop();

    lcont:
        printf("\nexecuting-ram-addr[%d] lcont op", calcRelativeRamAddr(ip));
		if (lc) {
			--lc;
			ip = lb;
		} else {
			ip = le;	
		}
		nextop();
    lbrk:
        printf("\nexecuting-ram-addr[%d] lbrk op", calcRelativeRamAddr(ip));
		ip = le;
        nextop();

    psh:
        printf("\nexecuting-ram-addr[%d] psh op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		memcpy(sp, ip, WS);
		ip += WS;
        nextop();

    pop:
        printf("\nexecuting-ram-addr[%d] pop op", calcRelativeRamAddr(ip));
		++ip;
		sp -= WS;
        nextop();

    pop2:
        printf("\nexecuting-ram-addr[%d] pop2 op", calcRelativeRamAddr(ip));
		++ip;
		sp -= (WS * 2);
        nextop();

    popn:
        printf("\nexecuting-ram-addr[%d] popn op", calcRelativeRamAddr(ip));
		++ip;
		sp -= (WS * getOprVal(uint32_t));
        nextop();

    pshfr:
        printf("\nexecuting-ram-addr[%d] pshfr op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		memcpy(sp, ram + getOprVal(uint32_t), WS);
		ip += WS;
        nextop();

    poptr:
        printf("\nexecuting-ram-addr[%d] poptr op", calcRelativeRamAddr(ip));
		++ip;
		memcpy(ram + getOprVal(uint32_t), sp, WS);
		ip += WS;
		sp -= WS;
        nextop();

    movtr:
        printf("\nexecuting-ram-addr[%d] movtr op", calcRelativeRamAddr(ip));
		++ip;
		memcpy(ram + getOprVal(uint32_t), sp, WS);
		ip += WS;
        nextop();

    stktr:
        printf("\nexecuting-ram-addr[%d] stktr op", calcRelativeRamAddr(ip));
        nextop();

    cpyr:
        printf("\nexecuting-ram-addr[%d] cpyr op", calcRelativeRamAddr(ip));
        nextop();

    setr:
        printf("\nexecuting-ram-addr[%d] setr op", calcRelativeRamAddr(ip));
		++ip;
		memcpy(ram + getOprVal(uint32_t), ip += WS, WS);
		ip += WS;
		nextop();

    pshfrr:
        printf("\nexecuting-ram-addr[%d] pshfrr op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		memcpy(sp, ram + getRamVal(uint32_t, getOprVal(uint32_t)), WS); 
		ip += WS;
        nextop();

    pshfrs:
        printf("\nexecuting-ram-addr[%d] pshfrs op", calcRelativeRamAddr(ip));
		++ip;
		memcpy(sp + WS, ram + getTopStkVal(uint32_t), WS); 
		sp += WS;
		ip += WS;
        nextop();

    inc:
        printf("\nexecuting-ram-addr[%d] inc op", calcRelativeRamAddr(ip));
		++ip;
		uint32_ptr = (uint32_t*) sp;
		(*uint32_ptr)++;
        nextop();

    dec:
        printf("\nexecuting-ram-addr[%d] dec op", calcRelativeRamAddr(ip));
		++ip;
		uint32_ptr = (uint32_t*) sp;
		(*uint32_ptr)--;
        nextop();

    add:
        printf("\nexecuting-ram-addr[%d] add op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		uint32_ptr = (uint32_t*) sp;
		*uint32_ptr = getNegTopStkVal(uint32_t, WS) + getNegTopStkVal(uint32_t, DWS);  
        nextop();

    sub:
        printf("\nexecuting-ram-addr[%d] sub op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		uint32_ptr = (uint32_t*) sp;
		*uint32_ptr = getNegTopStkVal(uint32_t, WS) - getNegTopStkVal(uint32_t, DWS);  
        nextop();

    mul:
        printf("\nexecuting-ram-addr[%d] mul op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		uint32_ptr = (uint32_t*) sp;
		*uint32_ptr = getNegTopStkVal(uint32_t, WS) * getNegTopStkVal(uint32_t, DWS);  
        nextop();

    div:
        printf("\nexecuting-ram-addr[%d] div op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		uint32_ptr = (uint32_t*) sp;
		*uint32_ptr = getNegTopStkVal(uint32_t, WS) / getNegTopStkVal(uint32_t, DWS);  
        nextop();

    mod:
        printf("\nexecuting-ram-addr[%d] mod op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		uint32_ptr = (uint32_t*) sp;
		*uint32_ptr = getNegTopStkVal(uint32_t, WS) % getNegTopStkVal(uint32_t, DWS);  
        nextop();

    and:
        printf("\nexecuting-ram-addr[%d] and op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		uint32_ptr = (uint32_t*) sp;
		*uint32_ptr = getNegTopStkVal(uint32_t, WS) & getNegTopStkVal(uint32_t, DWS);  
        nextop();

    not:
        printf("\nexecuting-ram-addr[%d] not op", calcRelativeRamAddr(ip));
		++ip;
		uint32_ptr = (uint32_t*) sp;
		~(*uint32_ptr);
        nextop();

    xor:
        printf("\nexecuting-ram-addr[%d] xor op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		uint32_ptr = (uint32_t*) sp;
		*uint32_ptr = getNegTopStkVal(uint32_t, WS) ^ getNegTopStkVal(uint32_t, DWS);  
        nextop();

    or:
        printf("\nexecuting-ram-addr[%d] or op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		uint32_ptr = (uint32_t*) sp;
		*uint32_ptr = getNegTopStkVal(uint32_t, WS) | getNegTopStkVal(uint32_t, DWS);  
        nextop();

    lshft:
        printf("\nexecuting-ram-addr[%d] lshft op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		uint32_ptr = (uint32_t*) sp;
		*uint32_ptr = getNegTopStkVal(uint32_t, WS) << getNegTopStkVal(uint32_t, DWS);  
        nextop();

    rshft:
        printf("\nexecuting-ram-addr[%d] rshft op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		uint32_ptr = (uint32_t*) sp;
		*uint32_ptr = getNegTopStkVal(uint32_t, WS) >> getNegTopStkVal(uint32_t, DWS);  
        nextop();

    lrot:
        printf("\nexecuting-ram-addr[%d] lrot op", calcRelativeRamAddr(ip));
		++ip;
		uint32_buf[0] = getNegTopStkVal(uint32_t, WS) << getNegTopStkVal(uint32_t, DWS);  
        uint32_buf[1] = getNegTopStkVal(uint32_t, WS) >> (WS_BITS - getNegTopStkVal(uint32_t, DWS));
		sp += WS;
		uint32_ptr = (uint32_t*) sp;
		*uint32_ptr = uint32_buf[0] | uint32_buf[1];
		nextop();

    rrot:
        printf("\nexecuting-ram-addr[%d] rrot op", calcRelativeRamAddr(ip));
		++ip;
		uint32_buf[0] = getNegTopStkVal(uint32_t, WS) >> getNegTopStkVal(uint32_t, DWS);  
        uint32_buf[1] = getNegTopStkVal(uint32_t, WS) << (WS_BITS - getNegTopStkVal(uint32_t, DWS));
		sp += WS;
		uint32_ptr = (uint32_t*) sp;
		*uint32_ptr = uint32_buf[0] | uint32_buf[1];
		nextop();

    incs:
        printf("\nexecuting-ram-addr[%d] incs op", calcRelativeRamAddr(ip));
		++ip;
		int32_ptr = (int32_t*) sp;
		(*int32_ptr)++;
        nextop();

    decs:
        printf("\nexecuting-ram-addr[%d] decs op", calcRelativeRamAddr(ip));
		++ip;
		int32_ptr = (int32_t*) sp;
		(*int32_ptr)--;
        nextop();

    adds:
        printf("\nexecuting-ram-addr[%d] adds op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		int32_ptr = (int32_t*) sp;
		*int32_ptr = getNegTopStkVal(int32_t, WS) + getNegTopStkVal(int32_t, DWS);  
        nextop();

    subs:
        printf("\nexecuting-ram-addr[%d] subs op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		int32_ptr = (int32_t*) sp;
		*int32_ptr = getNegTopStkVal(int32_t, WS) - getNegTopStkVal(int32_t, DWS);  
        nextop();

    muls:
        printf("\nexecuting-ram-addr[%d] muls op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		int32_ptr = (int32_t*) sp;
		*int32_ptr = getNegTopStkVal(int32_t, WS) * getNegTopStkVal(int32_t, DWS);  
        nextop();

    divs:
        printf("\nexecuting-ram-addr[%d] divs op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		int32_ptr = (int32_t*) sp;
		*int32_ptr = getNegTopStkVal(int32_t, WS) / getNegTopStkVal(int32_t, DWS);  
        nextop();

    mods:
        printf("\nexecuting-ram-addr[%d] mods op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		int32_ptr = (int32_t*) sp;
		*int32_ptr = getNegTopStkVal(int32_t, WS) % getNegTopStkVal(int32_t, DWS);  
        nextop();

    ands:
        printf("\nexecuting-ram-addr[%d] and op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		int32_ptr = (int32_t*) sp;
		*int32_ptr = getNegTopStkVal(int32_t, WS) & getNegTopStkVal(int32_t, DWS);  
        nextop();

    nots:
        printf("\nexecuting-ram-addr[%d] not op", calcRelativeRamAddr(ip));
		++ip;
		int32_ptr = (int32_t*) sp;
		~(*int32_ptr);
        nextop();

    xors:
        printf("\nexecuting-ram-addr[%d] xor op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		int32_ptr = (int32_t*) sp;
		*int32_ptr = getNegTopStkVal(int32_t, WS) ^ getNegTopStkVal(int32_t, DWS);  
        nextop();

    ors:
        printf("\nexecuting-ram-addr[%d] or op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		int32_ptr = (int32_t*) sp;
		*int32_ptr = getNegTopStkVal(int32_t, WS) | getNegTopStkVal(int32_t, DWS);  
        nextop();

    lshfts:
        printf("\nexecuting-ram-addr[%d] lshft op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		int32_ptr = (int32_t*) sp;
		*int32_ptr = getNegTopStkVal(int32_t, WS) << getNegTopStkVal(int32_t, DWS);  
        nextop();

    rshfts:
        printf("\nexecuting-ram-addr[%d] rshft op", calcRelativeRamAddr(ip));
		++ip;
		sp += WS;
		int32_ptr = (int32_t*) sp;
		*int32_ptr = getNegTopStkVal(int32_t, WS) >> getNegTopStkVal(int32_t, DWS);  
        nextop();

    lrots:
        printf("\nexecuting-ram-addr[%d] lrot op", calcRelativeRamAddr(ip));
		++ip;
		int32_buf[0] = getNegTopStkVal(int32_t, WS) << getNegTopStkVal(int32_t, DWS);  
        int32_buf[1] = getNegTopStkVal(int32_t, WS) >> (WS_BITS - getNegTopStkVal(int32_t, DWS));
		sp += WS;
		int32_ptr = (int32_t*) sp;
		*int32_ptr = int32_buf[0] | int32_buf[1];
		nextop();

    rrots:
        printf("\nexecuting-ram-addr[%d] rrot op", calcRelativeRamAddr(ip));
		++ip;
		int32_buf[0] = getNegTopStkVal(int32_t, WS) >> getNegTopStkVal(int32_t, DWS);  
        int32_buf[1] = getNegTopStkVal(int32_t, WS) << (WS_BITS - getNegTopStkVal(int32_t, DWS));
		sp += WS;
		int32_ptr = (int32_t*) sp;
		*int32_ptr = int32_buf[0] | int32_buf[1];
		nextop();

	brkp:
        printf("\nexecuting-ram-addr[%d] brkp op", calcRelativeRamAddr(ip));
		++ip;

		nextop();
}

int
run_fbin(const char* file_path)
{
	// initialise ram.
	void* ram = init_ram(RAMSIZE, 0);
	if (ram == NULL) return 1;
	load_program(file_path, 0, ram);
	return eval_process(ram);
}

int
main(int argc, char* argv[])
{
	// if (argc != 2) {
	// 	printf("\nfvm: no input files.");
	// 	return 0;
	// }

	int retval = run_fbin("vmt.fbin");
	
	printf("\n furst-vm ran successfully!\nretval: %d", retval);
	
	return 0;
}