from assembler import *

class Disassembler:
# NOTE: self.prog_list differs from self.prog_list in Assembler(). In Assembler() 
# self.prog_list is a list of lists where each list is an instruction 
# [[opcode, operand, operand], [opcode, operand, operand], [opcode, operand, operand]].
# Whereas in Disassembler() self.prog_list is a list of the program's integers, 
# [opcode, operand, operand, opcode, operand, operand].

    def __init__(self, 
                 input_path=None,
                 text_output_path=None,
                 report_output_path=None):
        
        self.input_path         = input_path
        self.text_output_path   = text_output_path
        self.report_output_path = report_output_path
        self.input_file         = None
        self.output_text_file   = None
        self.output_report_file = None
        self.report_output_file = None
        self.metadata           = MetadataDisassembler()
        self.disassembly_text   = []
        self.prog_list          = []
        self.prog_report        = [] # list of strings representing each integer value read from input file.
        self.bytes_read_count   = 0
        self.bytearray          = None

    def open_input_file(self,
                        input_path=None):
        
        if self.input_path is None:

            if input_path is None:
                raise Exception("Error: No input path specified!")
            
            else:
                self.input_path = input_path

        try:
            self.input_file = open(self.input_path, 'rb')
        except FileNotFoundError:
            print('\nError: Unable to open input-file:[%s], file does not exist!\n' % self.input_path)  
        except IOError:
            print('Error: An I/O error occurred! when opening file: [%s]' % self.input_path)
        except PermissionError:
            print("Error: You do not have permission to access this file: [%s]" % self.input_path)
        except IsADirectoryError:
            print("Error: The specified input-path: [%s] for report is a directory, not a file!" % self.input_path)
        except OSError as e:
            print("Error: An I/O error occurred while attempting to open input-file: [%s]\n    more info: %s" % (self.input_path, e))

    def open_output_file(self,
                        output_path=None):
        
        if self.output_path is None:

            if output_path is None:
                raise Exception("Error: No output-path specified!")
            
            else:
                self.output_path = output_path

        try:
            self.output_file = open(self.output_path, 'r')
        except FileNotFoundError:
            print('\nError: Unable to open input-file:[%s], file does not exist!\n' % self.input_path)  
        except IOError:
            print('Error: An I/O error occurred! when opening file: [%s]' % self.input_path)
        except PermissionError:
            print("Error: You do not have permission to access this file: [%s]" % self.input_path)
        except IsADirectoryError:
            print("Error: The specified input-path: [%s] for report is a directory, not a file!" % self.input_path)
        except OSError as e:
            print("Error: An I/O error occurred while attempting to open input-file: [%s]\n    more info: %s" % (self.input_path, e))

    def read_entire_input_file(self):

        self.open_input_file()




    def read_input_file(self):
        read_buffer = None

        # first read 2 bytes which should be the program starting address.
        read_buffer = self.input_file.read(2)
        self.bytes_read_count += 2

        # attempt to write starting address to self.prog_list[0].
        try:
            self.prog_list.append(struct.unpack('h', read_buffer)[0])
        except struct.error:
            print('\nError: Error when unpacking bytes from file: %s\n' % self.input_path)

        # read 2 bytes(one furst-vm integer, int16_t) at a time
        # then append them to self.prog_list as we go.
        try:
            while True:
                self.bytes_read_count += 2

                # read 2 bytes from input file.
                read_buffer = self.input_file.read(2)

                # if read_buffer is empty break from loop.
                if not read_buffer: break

                # Unpack the bytes into an int16_t value
                value = struct.unpack('h', read_buffer)[0]

                # append value to program list.
                self.prog_list.append(value)

                # build then append integer's report string to report-list.
                self.prog_report.append("\nBytes: %d :: Addr: %d :: Value: %d" % (self.bytes_read_count, self.bytes_read_count//2-1, value))
                
        except struct.error:
            print('\nError: Error when unpacking bytes from file: %s\n' % self.input_path)

        # finished reading bytes from the input-file, close the file.
        self.input_file.close()

    def write_report(self, 
                    report_output_path=None):

        if self.report_output_path is None:

            if report_output_path is None:
                raise Exception("Error: No output-path for report specified!")
            
            else:
                self.report_output_path = report_output_path

        try:

            # attempt to open/create report file.
            with open(self.report_output_path, 'w') as report_output_file:

                for integers_report_str in self.prog_report:

                    report_output_file.write(integers_report_str)

        except IOError:
            print("Error: I/O error occurred! when writing to: %s" % self.report_output_path)
        except PermissionError:
            print("Error: You do not have permission to access this file: %s" % self.report_output_path)
        except IsADirectoryError:
            print("Error: The specified output-path: %s for report is a directory, not a file!" % self.report_output_path)
        except OSError as e:
            print("Error: An I/O error occurred while attempting to write to report-file: %s! -> %s" % (self.report_output_path, e))

    def disassemble_prog(self):
        # confirm a program has been disassembled.
        if not self.prog_list:
            raise Exception("Error: No program to decompile!")
        
        # iterate through prog-list interpreting each integer into it's
        # string form as they come, append each string onto self.disassembly_text

        class MetadataDisassembler:
    def __init__(self, input_path=None):
        self.input_path        = input_path
        self.start_addr        = None
        self.keep_symbols_flag = None
        self.creation_date_str = None
        self.first_instr_addr  = None
        self.label_tbl_size    = None
        self.macro_tbl_size    = None
        self.symtbl_size       = None
        self.raw_flags         = None
        self.raw_creation_date = None
        self.raw_symtbl        = None
        self.bytes_read_count  = 0

    def unpack_raw_flags(self):
        # confirm flags have been read.
        if self.raw_flags is None:
            raise Exception("Error: Tried to interpret FLAGS metadata before it was read from file: [%s]" % self.input_path)

        # Extract the FLAGS which is LSB from self.raw_flags
        FLAGS = self.raw_flags & 0xFF

        # Check if keep_symbols flag is on or off.
        if (FLAGS & 0x01) == 1:
            self.keep_symbols_flag = True
        else:
            self.keep_symbols_flag = False

    def unpack_raw_creation_date(self):
        pass

    def unpack_bytes(self, byteArray):
    # takes a bytearray of metadata and splits it up into its parts,
    # assigning it to this classes member attributes.

        try:
            # first 2 bytes is the start-address.
            self.start_addr = struct.unpack(FURST_DATAFORMAT, byteArray[:2])[0]
            self.bytes_read_count += 2

            # Next 2 bytes is the FLAGS, then unpack them.
            self.raw_flags = struct.unpack(FURST_DATAFORMAT, byteArray[2:4])[0]
            self.bytes_read_count += 2
            self.unpack_raw_flags()

            # Next 2 bytes is the creation datestamp, then unpack it.
            self.raw_creation_date = struct.unpack(FURST_DATAFORMAT, byteArray[4:6])[0]
            self.bytes_read_count += 2
            self.unpack_raw_creation_date()

            # Next 2 bytes is the address of the first program instruction(not starting instruction).
            self.first_instr_addr = struct.unpack(FURST_DATAFORMAT, byteArray[6:8])[0]
            self.bytes_read_count += 2

            # check if we have a symbol-table, if so read it.
            if self.keep_symbols_flag:
                # Next 2 bytes is the label-table size
                self.label_tbl_size = struct.unpack(FURST_DATAFORMAT, byteArray[8:10])[0]
                self.bytes_read_count += 2

                # Next 2 bytes is the macro-table size
                self.macro_tbl_size = struct.unpack(FURST_DATAFORMAT, byteArray[10:12])[0]
                self.bytes_read_count += 2


                # calculate total symbol-table size & instruction starting byte.
                self.symtbl_size     = self.label_tbl_size + self.macro_tbl_size
                self.prog_start_byte = self.symtbl_size + 12 # 12 is the metadata before symtbl.

                # now use symtbl-size to create a new bytearray of just the raw symbol-table:
                self.raw_symtbl = bytearray(byteArray[12 : self.prog_start_byte])
                
            # no symbol-table. so program-starting-byte is first byte
            # after first-instr-addr metadata field.
            else:
                self.prog_start_byte = 8

        except struct.error:
            print('\nError: Error when unpacking bytes from file: [%s]\n' % self.input_path) 

        # check the calculated program-start-byte against the first-instr-addr in file's
        # metadata(multiplied by 2 because each addr is 2 bytes). If these do not match
        # then the file's first-instr-addr metadata field is incorrect.
        if (self.prog_start_byte // 2) != self.first_instr_addr:
            raise Exception("Error: First instruction address metadata field does not line up with calculated program starting byte! in file: [%s]" % self.input_path)

        # check program-start-byte against count of bytes the function just read.
        if self.prog_start_byte != self.bytes_read_count:
            raise Exception("Error: File's Program start byte metadata field does not match dissasembler's bytes-read-count in file: [%s]" % self.input_path)

        # metadata(except raw-symtbl) dissasembly complete.