#include <iostream>
#include <fstream>
#include <string>
#include <exception>
#include <stdexcept>
#include <cstdint>
#include <cstdio>
#include <memory>

#include "opcode.h"
#include "ram.h"
#include "vm.h"

#define INSIDE_UINT 10
#define INSIDE_INT  11
#define PUSH        50
#define POP         60

using namespace std;

class Ram
{
    protected:
        void*     master;
        uint8_t*  base;
        uint8_t*  type_record;
        uint8_t*  ubyte_ptr;
        uint32_t* uint_ptr;
        int32_t*  int_ptr;

    void
    validate_addr(uint32_t addr)
    {
        if (addr >= memory_size)
        {
            // string errmsg = format("invalid addr: {}", addr);
            // throw runtime_error(errmsg);
            printf("\nram address %u is invalid", addr);
            exit(0);
        }
    }

    void
    validate_datatype(uint32_t addr, uint8_t type)
    {
        // if (type_record[addr] != type)
        // {
        //     // string errmsg = format("access error, type mismatch, ram[{}] is {} not {}", addr, type_record[addr], type);
        //     // throw runtime_error(errmsg);
        //     printf("\naccess error, type mismatch, ram[%u] is %u not %u", addr, type_record[addr], type);
        //     exit(0);
        // }
    }

    public:
        uint32_t  memory_size;

        Ram(uint32_t memory_size, void* master_ptr) : memory_size(memory_size), master(master_ptr)
        {
            type_record = new uint8_t[memory_size];
            base        = (uint8_t*) master;
        }

        ~Ram()
        {
            delete[] type_record;
            free(master);
        }

        void
        print_addr(uint32_t addr)
        {
            validate_addr(addr);

            switch (type_record[addr]) 
            {
                case UINT32_CODE:
                    printf("\nram[%u] = %u", addr, get_uint(addr));
                    break;

                case INT32_CODE:
                    printf("\nram[%u] = %d", addr, get_int(addr));
                    break;

                case UINT8_CODE:
                    printf("\nram[%u] = %u", addr, get_ubyte(addr));
                    break;

                default:
                    printf("INTERNAL ERROR IN _addr()");
                    exit(0);
            }
        }

        void
        loadin_program(const char* file_path)
        {
            if (load_program(file_path, TRUE, master))
            {
                printf("INTERNAL ERROR IN loadin_program()");
                exit(0);
            }
        }

        void
        set_ubyte(uint32_t addr, uint8_t value)
        {
            validate_addr(addr);
            ubyte_ptr  = base + addr;
            *ubyte_ptr = value;
            type_record[addr] = UINT8_CODE;
        }

        void
        set_uint(uint32_t addr, uint32_t value)
        {
            validate_addr(addr);

            uint_ptr  = (uint32_t*) base + addr;
            *uint_ptr = value;
            type_record[addr] = UINT32_CODE;

            for (int i=1; i < UINT_SIZE; i++)
                type_record[addr + i] = INSIDE_UINT;
        }

        void
        set_int(uint32_t addr, int32_t value)
        {
            validate_addr(addr);

            int_ptr  = (int32_t*) base + addr;
            *int_ptr = value;
            type_record[addr] = INT32_CODE;

            for (int i=1; i < INT_SIZE; i++)
                type_record[addr + i] = INSIDE_INT;
        }

        uint8_t
        get_ubyte(uint32_t addr)
        {
            validate_addr(addr);
            validate_datatype(addr, UINT8_CODE);

            ubyte_ptr  = (uint8_t*) base + addr;
            return *ubyte_ptr;
        }

        uint32_t
        get_uint(uint32_t addr)
        {
            validate_addr(addr);
            validate_datatype(addr, UINT32_CODE);

            uint_ptr  = (uint32_t*) base + addr;
            return *uint_ptr;
        }

        int32_t
        get_int(uint32_t addr)
        {
            validate_addr(addr);
            validate_datatype(addr, INT32_CODE);

            int_ptr  = (int32_t*) base + addr;
            return *int_ptr;
        }

        void* 
        get_ptr(uint32_t addr)
        {
            validate_addr(addr);
            return base + addr;
        }
};

class WorkStack : public Ram
{
    uint8_t* top;
    uint32_t obj_count;

    void
    set_next_top(uint8_t action)
    {
        if (action == PUSH)
        {
            switch (type_record[top_addr])
            {
                case UINT32_CODE:
                    top       += UINT_SIZE;
                    top_addr  += UINT_SIZE;
                    obj_count++;
                    break;

                case INT32_CODE:
                    top       += INT_SIZE;
                    top_addr  += INT_SIZE;
                    obj_count++;
                    break;

                case UINT8_CODE:
                    top++;
                    top_addr++;
                    obj_count++;
                    break;

                default:
                    printf("\nINTERNAL ERROR in set_next_top() ");
                    break;
            }
        }

        else if (action == POP)
        {
            switch (type_record[top_addr])
            {
                case UINT32_CODE:
                    top       -= UINT_SIZE;
                    top_addr  -= UINT_SIZE;
                    obj_count--;
                    break;

                case INT32_CODE:
                    top       -= INT_SIZE;
                    top_addr  -= INT_SIZE;
                    obj_count--;
                    break;

                case UINT8_CODE:
                    top--;
                    top_addr--;
                    obj_count--;
                    break;

                default:
                    printf("\nINTERNAL ERROR in set_next_top() ");
                    break;
            }
        }
    }

    public:
        uint32_t top_addr;

        WorkStack(uint32_t memory_size, void* master_ptr) : 
        Ram(memory_size, master_ptr), top_addr(0), obj_count(0) { top = base; }

        uint32_t
        read_uint_from_top_addr(uint32_t neg_offset)
        {
            if (!top_addr)
            {
                printf("INTERNAL ERROR IN read_uint_from_top_addr()");
                return 0;
            }

            else if (neg_offset < top_addr)
            {
                return 0;
            }

            uint_ptr = (uint32_t*) base + (top_addr - neg_offset);
            return *uint_ptr;
        }

        void
        print_top()
        {
            if (!obj_count)
            {
                printf("\n INTERNAL ERROR in print-top, stack empty.");
            }
            
            switch (type_record[top_addr])
            {
                case UINT32_CODE:
                    printf("\nstack[top] = %u", get_uint(top_addr));
                    break;

                case INT32_CODE:
                    printf("\nstack[top] = %d", get_int(top_addr));
                    break;

                case UINT8_CODE:
                    printf("\nstack[top] = %u", get_ubyte(top_addr));
                    break;

                default:
                    printf("INTERNAL ERROR IN ws.print_top");
                    exit(0);
            }
        }

        int32_t
        read_int_from_top_addr(uint32_t neg_offset)
        {
            if (!obj_count)
            {
                printf("INTERNAL ERROR IN read_int_from_top_addr()");
                return 0;
            }

            else if (neg_offset < top_addr)
            {
                return 0;
            }

            int_ptr = (int32_t*) base + (top_addr - neg_offset);
            return *int_ptr;
        }

        void*
        get_top_ptr()
        {
            if (!obj_count)
                return get_ptr(top_addr);
            
            return get_ptr(top_addr);
        }

        void*
        get_sectop_ptr()
        {
            uint8_t minus_value;

            if (obj_count < 2)
                return nullptr;
        
            switch (type_record[top_addr])
            {
                case UINT32_CODE:
                    minus_value = UINT_SIZE;
                    break;

                case INT32_CODE:
                    minus_value = INT_SIZE;
                    break;

                case UINT8_CODE:
                    minus_value = BYTE_SIZE;
                    break;

                default:
                    printf("INTERNAL ERROR IN get_sec_topptr()");
            }

            return get_ptr(top_addr - minus_value);
        }

        void
        push_ubyte(uint8_t value)
        {
            validate_addr(top_addr + 1);
            type_record[top_addr + 1] = UINT8_CODE;
            set_next_top(PUSH);
            ubyte_ptr = (uint8_t*) top;
            *ubyte_ptr = value;
        }      

        void
        push_uint(uint32_t value)
        {
            validate_addr(top_addr + UINT_SIZE);
            type_record[top_addr + UINT_SIZE] = UINT32_CODE;
            set_next_top(PUSH);
            uint_ptr = (uint32_t*) top;
            *uint_ptr = value;
            for (int i=1; i < UINT_SIZE; i++)
                type_record[top_addr + i] = INSIDE_UINT;
        }    

        void
        push_int(int32_t value)
        {
            validate_addr(top_addr + INT_SIZE);
            type_record[top_addr + INT_SIZE] = INT32_CODE;
            set_next_top(PUSH);
            int_ptr = (int32_t*) top;
            *int_ptr = value;
            for (int i=1; i < INT_SIZE; i++)
                type_record[top_addr + i] = INSIDE_INT;
        }  

        uint32_t
        pop_uint()
        {
            if (!obj_count)
            {
                printf("\nINTERNAL ERROR IN pop_uint()");
                return 0;
            }

            uint_ptr = (uint32_t*) top;
            set_next_top(POP);
            return *uint_ptr;
        }  

        uint8_t
        pop_ubyte()
        {
            if (!obj_count)
            {
                printf("\nINTERNAL ERROR IN pop_ubyte()");
                return 0;
            }

            ubyte_ptr = (uint8_t*) top;
            set_next_top(POP);
            return *ubyte_ptr;
        }

        int32_t
        pop_int()
        {
            if (!obj_count)
            {
                printf("\nINTERNAL ERROR IN pop_int()");
                return 0;
            }

            int_ptr = (int32_t*) top;
            set_next_top(POP);
            return *int_ptr;
        }  

        uint32_t
        read_uint(uint32_t addr)
        {
            if (!obj_count)
            {
                // process popping empty stack here.
                return 0;
            }

            else if (addr > top_addr)
            {
                return 0;
            }

            uint_ptr = (uint32_t*) base + addr;
            return *uint_ptr;
        }

        int32_t
        read_int(int32_t addr)
        {
            if (!obj_count)
            {
                // process popping empty stack here.
                return 0;
            }

            else if (addr > top_addr)
            {
                return 0;
            }

            int_ptr = (int32_t*) base + addr;
            return *int_ptr;
        }

        uint32_t
        read_from_top_uint(uint32_t neg_offset)
        {
            if (!obj_count)
            {
                // process popping empty stack here.
                return 0;
            }

            uint_ptr = (uint32_t*) top;
            return *uint_ptr;
        }

        uint32_t
        read_top_uint()
        {
            if (!obj_count)
            {
                // process popping empty stack here.
                return 0;
            }

            uint_ptr = (uint32_t*) top;
            return *uint_ptr;
        }

        uint32_t
        read_sectop_uint()
        {
            if (!obj_count)
            {
                // process popping empty stack here.
                return 0;
            }

            uint_ptr = (uint32_t*) top - WORDSIZE;
            return *uint_ptr;
        }

        int32_t
        read_top_int()
        {
            if (!obj_count)
            {
                // process popping empty stack here.
                return 0;
            }

            int_ptr = (int32_t*) top;
            return *int_ptr;
        }

        int32_t
        read_sectop_int()
        {
            if (obj_count < 2)
            {
                // process popping empty stack here.
                return 0;
            }

            int_ptr = (int32_t*) top - WORDSIZE;
            return *int_ptr;
        }

        void
        remove(uint32_t count = 1)
        {
            if (!obj_count)
            {
                printf("\nINTERNAL ERROR IN remove()");
                return;
            }

            for (int i; i < count; i++)
                set_next_top(POP);
        }
};

class CallStack {
    uint32_t* array;

    public:
        uint32_t next_ndx;

        CallStack()
        {
            array    = new uint32_t[RECUR_MAX];
            next_ndx = 0;

            for (int i=0; i < RECUR_MAX; i++)
                array[i] = 0;
        }

        ~CallStack()
        {
            delete[] array;
        }

        void
        push_addr(uint32_t addr)
        {
            if (next_ndx != RECUR_MAX)
            {
                next_ndx++;
                array[next_ndx] = addr;
            }
        }

        uint32_t
        pop_addr()
        {
            if (next_ndx)
            {
                next_ndx--;
                return array[next_ndx + 1];
            }

            return 0;
        }
};


class DebugVM
{
    WorkStack* workstack;
    CallStack* callstack;
    Ram*       ram;

    uint32_t   pc;           // program-counter.
    uint32_t   loop_counter; // loop-base pointer.
    uint32_t   loop_body;    // loop-end pointer.
    uint32_t   loop_end;     // loop counter.

    bool       breakpoint_hit;
    bool       exec_locked;
    bool       die_op_hit;

    uint32_t  uint_arg_left;
    uint32_t  uint_arg_right;
    uint32_t  uint_result;
    uint32_t  uint_result2;
    
    int32_t   int_arg_left;
    int32_t   int_arg_right;
    int32_t   int_result;
    int32_t   int_result2;

    uint32_t  src_addr;
    uint32_t  dst_addr;

    bool      bool_result;
    bool      zero_div;

    // main debugger execution loop.
    void
    main_loop()
    {
        pc = IP_START_ADDR_ADDR;

        do
        {
            exec_handle();
        } while (!die_op_hit);
        
        workstack->print_top();
    }

    // execution-handle, controls the execution of program, basically controls the locking mechanism inbetween
    // each instruction. runs the user-input functions inbetween the opcode's execution.
    void
    exec_handle()
    {
        //check_for_breakpoint();

        // if (exec_locked || breakpoint_hit)
        // {
        //     get_user_input();
        //     process_user_input();
        // }

        exec_opcode(ram->get_ubyte(pc));
    }

    void
    exec_opcode(uint8_t opcode)
    {
        switch (opcode)
        {
            case die_op:      exec_die_op();     break;
            case nop_op:      exec_nop_op();     break;
            case nspctr_op:   exec_nspctr_op();  break;
            case nspctst_op:  exec_nspctst_op(); break;
            case test_die_op: exec_test_die_op();break;
            case call_op:     exec_call_op();    break;
            case ret_op:      exec_ret_op();     break;
            case swtch_op:    exec_swtch_op();   break;
            case jmp_op:      exec_jmp_op();     break;
            case je_op:       exec_je_op();      break;  
            case jn_op:       exec_jn_op();      break;  
            case jl_op:       exec_jl_op();      break;  
            case jg_op:       exec_jg_op();      break;  
            case jls_op:      exec_jls_op();     break;  
            case jgs_op:      exec_jgs_op();     break;  
            case loop_op:     exec_loop_op();    break;  
            case lcont_op:    exec_lcont_op();   break;  
            case lbrk_op:     exec_lbrk_op();    break; 
            case psh_op:      exec_psh_op();     break;  
            case pop_op:      exec_pop_op();     break;  
            case pop2_op:     exec_pop2_op();    break;  
            case popn_op:     exec_popn_op();    break;  
            case pshfr_op:    exec_pshfr_op();   break;  
            case movtr_op:    exec_movtr_op();   break;  
            case stktr_op:    exec_movtr_op();   break;  
            case cpyr_op:     exec_movtr_op();   break;  
            case setr_op:     exec_movtr_op();   break;  
            case pshfrr_op:   exec_movtr_op();   break;  
            case pshfrs_op:   exec_movtr_op();   break;  
            case inc_op:      exec_movtr_op();   break;  
            case dec_op:      exec_movtr_op();   break;  
            case add_op:      exec_movtr_op();   break;  
            case sub_op:      exec_movtr_op();   break;  
            case mul_op:      exec_movtr_op();   break;  
            case div_op:      exec_movtr_op();   break;  
            case mod_op:      exec_movtr_op();   break;  
            case incs_op:     exec_movtr_op();   break;  
            case decs_op:     exec_movtr_op();   break;  
            case adds_op:     exec_movtr_op();   break;  
            case subs_op:     exec_movtr_op();   break;  
            case muls_op:     exec_movtr_op();   break;  
            case divs_op:     exec_movtr_op();   break;  
            case mods_op:     exec_movtr_op();   break;  
            case and_op:      exec_movtr_op();   break;  
            case not_op:      exec_movtr_op();   break;  
            case xor_op:      exec_movtr_op();   break;  
            case or_op:       exec_movtr_op();   break;  
            case lshft_op:    exec_movtr_op();   break;  
            case rshft_op:    exec_movtr_op();   break;  
            case lrot_op:     exec_movtr_op();   break;  
            case rrot_op:     exec_movtr_op();   break;  
            case ands_op:     exec_movtr_op();   break;  
            case nots_op:     exec_movtr_op();   break;  
            case xors_op:     exec_movtr_op();   break;  
            case ors_op:      exec_movtr_op();   break;  
            case lshfts_op:   exec_movtr_op();   break;  
            case rshfts_op:   exec_movtr_op();   break;  
            case lrots_op:    exec_movtr_op();   break;  
            case rrots_op:    exec_movtr_op();   break;  
            case brkp_op:     exec_movtr_op();   break;  

            default:
                // Handle unknown opcode
                break;
            }
    }

    void
    exec_die_op()
    {
        die_op_hit = true;
    }

    void
    exec_nop_op()
    {
        pc++;
    }
    
    void
    exec_nspctr_op()
    {
        uint32_t nspct_addr;
        uint32_t nspct_value;

        pc++;
        nspct_addr  = ram->get_uint(pc);
        nspct_value = ram->get_uint(nspct_addr);
        printf("ram[%u] = %u", nspct_addr, nspct_value);
        pc += UINT_SIZE;
    }
    
    void
    exec_nspctrs_op()
    {
        uint32_t nspct_addr;
        int32_t  nspct_value;
        
        pc++;
        nspct_addr  = ram->get_uint(pc);
        nspct_value = ram->get_int(nspct_addr);
        printf("ram[%u] = %d", nspct_addr, nspct_value);
        pc += UINT_SIZE;
    }

    void
    exec_nspctst_op()
    {
        uint32_t nspct_addr;
        uint32_t  nspct_value;
        
        pc++;
        nspct_addr  = ram->get_uint(pc);
        nspct_value = workstack->read_uint_from_top_addr(nspct_addr);
        printf("workstack[%u] = %u", nspct_addr, nspct_value);
        pc += UINT_SIZE;
    }

    void
    exec_nspctsts_op()
    {
        uint32_t nspct_addr;
        int32_t  nspct_value;
        
        pc++;
        nspct_addr  = ram->get_uint(pc);
        nspct_value = workstack->read_int_from_top_addr(nspct_addr);
        printf("workstack[%u] = %d", nspct_addr, nspct_value);
        pc += UINT_SIZE;
    }

    void
    exec_test_die_op()
    {
        pc++;
    }
    
    void
    exec_call_op()
    {
        pc++;
        callstack->push_addr(pc + UINT_SIZE);
        pc = ram->get_uint(pc);
    }
    
    void
    exec_ret_op()
    {
        pc = callstack->pop_addr();
    }
    
    void
    exec_swtch_op() 
    {
        pc++;
    }
    
    void
    exec_jmp_op()
    {
        pc++;
        pc = ram->get_uint(pc);
    }
    
    void
    exec_je_op()
    {
        pc++;
        bool_result = memcmp(workstack->get_top_ptr(), workstack->get_sectop_ptr(), WORDSIZE);

        if (!bool_result)
            pc = ram->get_uint(pc);
        else
            pc += UINT_SIZE;
    }
    
    void
    exec_jn_op()
    {
        pc++;
        bool_result = memcmp(workstack->get_top_ptr(), workstack->get_sectop_ptr(), WORDSIZE);

        if (bool_result)
            pc = ram->get_uint(pc);
        else
            pc += UINT_SIZE;
    }
    
    void
    exec_jl_op()
    {
        uint_arg_left  = workstack->read_top_uint();
        uint_arg_right = workstack->read_sectop_uint();
        uint_result    = uint_arg_left < uint_arg_right;
        
        pc++;

        if (uint_result)
            pc = ram->get_uint(pc);
        else
            pc += UINT_SIZE;
    }

    void
    exec_jg_op()
    {
        uint_arg_left  = workstack->read_top_uint();
        uint_arg_right = workstack->read_sectop_uint();
        uint_result    = uint_arg_left > uint_arg_right;
        
        pc++;

        if (uint_result)
            pc = ram->get_uint(pc);
        else
            pc += UINT_SIZE;
    }
    
    void
    exec_jls_op()
    {
        int_arg_left  = workstack->read_top_uint();
        int_arg_right = workstack->read_sectop_uint();
        int_result    = int_arg_left < int_arg_right;
        
        pc++;

        if (int_result)
            pc = ram->get_uint(pc);
        else
            pc += UINT_SIZE;
    }
    
    void
    exec_jgs_op()
    {
        int_arg_left  = workstack->read_top_int();
        int_arg_right = workstack->read_sectop_int();
        int_result    = int_arg_left > int_arg_right;
        
        pc++;

        if (int_result)
            pc = ram->get_uint(pc);
        else
            pc += UINT_SIZE;
    }
    
    void
    exec_loop_op()
    {
        pc++;

        loop_counter = ram->get_uint(pc);
        pc += UINT_SIZE;

        loop_body = ram->get_uint(pc);
        pc += UINT_SIZE;

        loop_end  = ram->get_uint(pc);
        pc += UINT_SIZE;
    }
    
    void
    exec_lcont_op()
    {
        if (loop_counter)
        {
            loop_counter--;
            pc = loop_body;
        }
        else 
        {
            pc = loop_end;
        }
    }
    
    void
    exec_lbrk_op()
    {
        pc = loop_end;
    }
    
    void
    exec_psh_op()
    {
        uint32_t psh_value;
        pc++;
        psh_value = ram->get_uint(pc);
        workstack->push_uint(psh_value);
        pc += UINT_SIZE;
    }
    
    void
    exec_pop_op()
    {
        workstack->remove(1);
        pc++;
    }
    
    void
    exec_pop2_op()
    {
        workstack->remove(2);
        pc++;
    }

    void
    exec_popn_op()
    {
        uint32_t pop_count;
        pc++;
        pop_count = ram->get_uint(pc);
        workstack->remove(pop_count);
        pc += UINT_SIZE;
    }

    
    void
    exec_pshfr_op()
    {
        uint32_t psh_value;
        uint32_t src_addr;
        pc++;
        src_addr  = ram->get_uint(pc);
        psh_value = ram->get_uint(src_addr);
        workstack->push_uint(psh_value);
        pc += UINT_SIZE;
    }
    
    void
    exec_poptr_op()
    {
        uint32_t popped_value = workstack->pop_uint();
        uint32_t dst_addr;
        pc++;
        dst_addr = ram->get_uint(pc);
        ram->set_uint(dst_addr, popped_value);
        pc += UINT_SIZE;
    }
    
    void
    exec_movtr_op()
   {
        uint32_t copied_value = workstack->read_top_uint();
        uint32_t dst_addr;
        pc++;
        dst_addr = ram->get_uint(pc);
        ram->set_uint(dst_addr, copied_value);
        pc += UINT_SIZE;
    }
    
    void
    exec_stktr_op()
   {
        uint32_t copied_value;
        uint32_t src_addr;
        uint32_t dst_addr;
        pc++;
        src_addr = ram->get_uint(pc);
        pc += UINT_SIZE;
        dst_addr = ram->get_uint(pc);
        copied_value = workstack->read_uint(src_addr);
        ram->set_uint(dst_addr, copied_value);
        pc += UINT_SIZE;
    }
    
    void
    exec_cpyr_op()
   {
        uint32_t copied_value;
        uint32_t src_addr;
        uint32_t dst_addr;
        pc++;
        src_addr = ram->get_uint(pc);
        pc += UINT_SIZE;
        dst_addr = ram->get_uint(pc);
        copied_value = ram->get_uint(src_addr);
        ram->set_uint(dst_addr, copied_value);
        pc += UINT_SIZE;
    }
    
    
    void
    exec_setr_op()
    {
        uint32_t value;
        uint32_t dst_addr;
        pc++;
        dst_addr = ram->get_uint(pc);
        pc += UINT_SIZE;
        value = ram->get_uint(pc);
        ram->set_uint(dst_addr, value);
        pc += UINT_SIZE;
    }
    
    void
    exec_pshfrr_op()
    {
        uint32_t psh_value;
        uint32_t src_addr;
        uint32_t final_src_addr;
        pc++;
        src_addr  = ram->get_uint(pc);
        final_src_addr = ram->get_uint(src_addr);
        psh_value = ram->get_uint(final_src_addr);
        workstack->push_uint(psh_value);
        pc += UINT_SIZE;
    }
    
    void
    exec_pshfrs_op()
    {
        int32_t psh_value;
        uint32_t src_addr;
        uint32_t final_src_addr;
        pc++;
        src_addr  = workstack->read_top_uint();
        final_src_addr = ram->get_uint(src_addr);
        psh_value = ram->get_int(final_src_addr);
        workstack->push_int(psh_value);
        pc += UINT_SIZE;
    }
    
    void
    exec_inc_op()
    {
        uint_arg_left  = workstack->read_top_uint();
        uint_result    = uint_arg_left++;
        workstack->push_uint(uint_result);
        pc++;
    }
    
    void
    exec_dec_op()
    {
        uint_arg_left  = workstack->read_top_uint();
        uint_result    = uint_arg_left--;
        workstack->push_uint(uint_result);
        pc++;
    }        
    
    void
    exec_add_op()
    {
        uint_arg_left   = workstack->read_top_uint();
        uint_arg_right  = workstack->read_sectop_uint();
        uint_result     = uint_arg_left + uint_arg_right;
        workstack->push_uint(uint_result);
        pc++;
    }        
    
    void
    exec_sub_op()
    {
        uint_arg_left   = workstack->read_top_uint();
        uint_arg_right  = workstack->read_sectop_uint();
        uint_result     = uint_arg_left - uint_arg_right;
        workstack->push_uint(uint_result);
        pc++;
    }        

    void
    exec_mul_op()
    {
        uint_arg_left   = workstack->read_top_uint();
        uint_arg_right  = workstack->read_sectop_uint();
        uint_result     = uint_arg_left * uint_arg_right;
        workstack->push_uint(uint_result);
        pc++;
    }        
    
    void
    exec_div_op()
    {
        uint_arg_left   = workstack->read_top_uint();
        uint_arg_right  = workstack->read_sectop_uint();

        if (!uint_arg_left || !uint_arg_right)
        {
            zero_div = true;
        }
        else 
        {
            uint_result     = uint_arg_left / uint_arg_right;
            workstack->push_uint(uint_result);
        }

        pc++;
    }        
    
    void
    exec_mod_op()
    {
        uint_arg_left   = workstack->read_top_uint();
        uint_arg_right  = workstack->read_sectop_uint();

        if (!uint_arg_right)
        {
            zero_div = true;
        }
        else 
        {
            uint_result     = uint_arg_left % uint_arg_right;
            workstack->push_uint(uint_result);
        }

        pc++;
    }
    
    void
    exec_incs_op()
    {
        int_arg_left  = workstack->read_top_int();
        int_result    = int_arg_left++;
        workstack->push_int(int_result);
        pc++;
    }
    
    void
    exec_decs_op()
    {
        int_arg_left  = workstack->read_top_int();
        int_result    = int_arg_left--;
        workstack->push_int(int_result);
        pc++;
    }        
    
    void
    exec_adds_op()
    {
        int_arg_left   = workstack->read_top_int();
        int_arg_right  = workstack->read_sectop_int();
        int_result     = int_arg_left + int_arg_right;
        workstack->push_int(int_result);
        pc++;
    }        
    
    void
    exec_subs_op()
    {
        int_arg_left   = workstack->read_top_int();
        int_arg_right  = workstack->read_sectop_int();
        int_result     = int_arg_left - int_arg_right;
        workstack->push_int(int_result);
        pc++;
    }        

    void
    exec_muls_op()
    {
        int_arg_left   = workstack->read_top_int();
        int_arg_right  = workstack->read_sectop_int();
        int_result     = int_arg_left * int_arg_right;
        workstack->push_int(int_result);
        pc++;
    }        
    
    void
    exec_divs_op()
    {
        int_arg_left   = workstack->read_top_int();
        int_arg_right  = workstack->read_sectop_int();

        if (!int_arg_left || !int_arg_right)
        {
            zero_div = true;
        }
        else 
        {
            int_result     = int_arg_left / int_arg_right;
            workstack->push_int(int_result);
        }

        pc++;
    }        
    
    void
    exec_mods_op()
    {
        int_arg_left   = workstack->read_top_int();
        int_arg_right  = workstack->read_sectop_int();

        if (!int_arg_right)
        {
            zero_div = true;
        }
        else 
        {
            int_result = int_arg_left % int_arg_right;
            workstack->push_int(int_result);
        }

        pc++;
    }
    
    void exec_and_op()
    {
        uint_arg_left   = workstack->read_top_uint();
        uint_arg_right  = workstack->read_sectop_uint();
        uint_result     = uint_arg_left & uint_arg_right;
        workstack->push_uint(uint_result);
        pc++;
    }        
    
    void exec_not_op()
    {
        uint_arg_left   = workstack->read_top_uint();
        uint_result     = !uint_arg_left;
        workstack->push_uint(uint_result);
        pc++;
    }
    
    void exec_xor_op()
    {
        uint_arg_left   = workstack->read_top_uint();
        uint_arg_right  = workstack->read_sectop_uint();
        uint_result     = uint_arg_left ^ uint_arg_right;
        workstack->push_uint(uint_result);
        pc++;
    }        
    
    void exec_or_op()
    {
        uint_arg_left   = workstack->read_top_uint();
        uint_arg_right  = workstack->read_sectop_uint();
        uint_result     = uint_arg_left | uint_arg_right;
        workstack->push_uint(uint_result);
        pc++;
    }        
    
    void exec_lshft_op()
    {
        uint_arg_left   = workstack->read_top_uint();
        uint_arg_right  = workstack->read_sectop_uint();
        uint_result     = uint_arg_left << uint_arg_right;
        workstack->push_uint(uint_result);
        pc++;
    }        
    
    void exec_rshft_op()
    {
        uint_arg_left   = workstack->read_top_uint();
        uint_arg_right  = workstack->read_sectop_uint();
        uint_result     = uint_arg_left >> uint_arg_right;
        workstack->push_uint(uint_result);
        pc++;
    }   
    
    void exec_lrot_op()
    {
        uint_arg_left   = workstack->read_top_uint();
        uint_arg_right  = workstack->read_sectop_uint();

        uint_result = uint_arg_left << uint_arg_right;
        uint_result2 = uint_arg_left >> (WS_BITS - uint_arg_right);
        uint_result  = uint_result | uint_result2;
        workstack->push_uint(uint_result);
        pc++;
    }        
    
    void exec_rrot_op()
    {
        uint_arg_left   = workstack->read_top_uint();
        uint_arg_right  = workstack->read_sectop_uint();
        
        uint_result = uint_arg_left >> uint_arg_right;
        uint_result2 = uint_arg_left << (WS_BITS - uint_arg_right);
        uint_result  = uint_result | uint_result2;
        workstack->push_uint(uint_result);
        pc++;
    }     
    
    void exec_ands_op()
    {
        int_arg_left   = workstack->read_top_int();
        int_arg_right  = workstack->read_sectop_int();
        int_result     = int_arg_left & int_arg_right;
        workstack->push_int(int_result);
        pc++;
    }        
    
    void exec_nots_op()
    {
        int_arg_left   = workstack->read_top_int();
        int_result     = !int_arg_left;
        workstack->push_int(int_result);
        pc++;
    }
    
    void exec_xors_op()
    {
        int_arg_left   = workstack->read_top_int();
        int_arg_right  = workstack->read_sectop_int();
        int_result     = int_arg_left ^ int_arg_right;
        workstack->push_int(int_result);
        pc++;
    }        
    
    void exec_ors_op()
    {
        int_arg_left   = workstack->read_top_int();
        int_arg_right  = workstack->read_sectop_int();
        int_result     = int_arg_left | int_arg_right;
        workstack->push_int(int_result);
        pc++;
    }        
    
    void exec_lshfts_op()
    {
        int_arg_left   = workstack->read_top_int();
        int_arg_right  = workstack->read_sectop_int();
        int_result     = int_arg_left << int_arg_right;
        workstack->push_int(int_result);
        pc++;
    }        
    
    void exec_rshfts_op()
    {
        int_arg_left   = workstack->read_top_int();
        int_arg_right  = workstack->read_sectop_int();
        int_result     = int_arg_left >> int_arg_right;
        workstack->push_int(int_result);
        pc++;
    }        

    void exec_lrots_op()
    {
        int_arg_left   = workstack->read_top_int();
        int_arg_right  = workstack->read_sectop_int();

        int_result = int_arg_left << int_arg_right;
        int_result2 = int_arg_left >> (WS_BITS - int_arg_right);
        int_result  = int_result | int_result2;
        workstack->push_int(int_result);
        pc++;
    }        
    
    void exec_rrots_op()
    {
        int_arg_left   = workstack->read_top_int();
        int_arg_right  = workstack->read_sectop_int();
        
        int_result = int_arg_left >> int_arg_right;
        int_result2 = int_arg_left << (WS_BITS - int_arg_right);
        int_result  = int_result | int_result2;
        workstack->push_int(int_result);
        pc++;
    }     
    
    void exec_brkp_op() {}
    
    void // prompts user the next action, sets user-input-vars based on said input.
    get_user_input()
    {

    }

    // performs corresponding actions based on the user-input-vars.
    void
    process_user_input()
    {

    }

    // checks the breakpoints-datastructure to see if the next instr aligns with a breakpoint.
    // if there is a breakpoint, breakpoint_hit flag is set to true.
    void 
    check_for_breakpoint()
    {

    }

    public:
        DebugVM(Ram* ram = nullptr) :
        ram(ram), exec_locked(true), die_op_hit(false), breakpoint_hit(false)
        {
			workstack = new WorkStack(STACK_SIZE, malloc(STACK_SIZE));
			callstack = new CallStack();
        }

        ~DebugVM()
        {
            delete workstack;
            delete callstack;
        }

        void
        start_debug()
        {
            main_loop();
        }

        void
        loadprog(const char* path)
        {
            ram->loadin_program(path);
        }
};

void
do_test()
{
    printf("\nprog start");
    void* master = init_ram(RAMSIZE, TRUE);
    Ram* ram     = new Ram(RAMSIZE, master);
    DebugVM* dvm = new DebugVM(ram);
    dvm->loadprog("vmt.fbin");
    dvm->start_debug();
    delete dvm;
    delete ram;
}

int main() {
    do_test();
    return 0;
}