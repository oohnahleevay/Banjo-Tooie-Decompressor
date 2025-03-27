'''
Purpose:
'''

###################
##### IMPORTS #####
###################

import struct
import json

##############################
##### GENERIC FILE CLASS #####
##############################

class Generic_Bin_File_Class():
    '''
    PyDoc
    '''
    def __init__(self, file_path:str):
        self._file_path:str = file_path
        self._file_content:bytearray = None
        self._read_file()

    ###################
    ##### GENERIC #####
    ###################

    def _read_bytes(self, index_start:int, byte_count:int):
        '''
        PyDoc
        '''
        byte_data:bytearray = self._file_content[index_start:index_start + byte_count]
        return byte_data

    ###################
    ##### NUMBERS #####
    ###################

    # INTEGERS

    def _read_bytes_as_int(self,
            index_start:int, byte_count:int, check_for_negative:bool=False):
        '''
        PyDoc
        '''
        byte_data:bytearray = self._read_bytes(index_start, byte_count)
        integer_value = int.from_bytes(byte_data, byteorder='big', signed=check_for_negative)
        return integer_value

    def _write_int_as_bytes(self,
            integer_value:int, byte_count:int):
        '''
        PyDoc
        '''
        signed:bool = (integer_value < 0)
        byte_data:bytearray = integer_value.to_bytes(byte_count, byteorder='big', signed=signed)
        self._file_content += byte_data
    
    # FLOATS

    def _read_bytes_as_float(self,
            index_start:int):
        '''
        PyDoc
        '''
        byte_data:bytearray = self._read_bytes(index_start, 4)
        float_value = struct.unpack('>f', byte_data)[0]
        return float_value
    
    def _write_float_as_bytes(self,
            float_value:float):
        '''
        PyDoc
        '''
        byte_data:bytearray = struct.pack('>f', float_value) # '>f' specifies big-endian float
        self._file_content += byte_data
    
    # BITFIELDS

    def _read_bytes_as_bitfield(self,
            index_start:int, byte_count:int, bitfield_map:list):
        '''
        PyDoc

        Usage:
            bitfields = [
                ('field1', 4), # 4 bits for field1
                ('field2', 3), # 3 bits for field2
                ('field3', 5), # 5 bits for field3
            ]
            integer = 0b101101110110
        '''
        integer_value:int = self._read_bytes_as_int(index_start, byte_count, False)
        result:dict = {}
        for bitfield_name, bitfield_bits in reversed(bitfield_map):
            result[bitfield_name] = integer_value & ((1 << bitfield_bits) - 1)
            integer_value >>= bitfield_bits
        return result
    
    def _write_bitfield_as_bytes(self,
            bitfield_map:list, values:list, byte_count:int):
        '''
        PyDoc

        Usage:
            bitfields = [
                ('field1', 4), # 4 bits for field1
                ('field2', 3), # 3 bits for field2
                ('field3', 5) # 5 bits for field3
            ]
            values = [
                0b1011, # Value for field1
                0b101, # Value for field2
                0b11110 # Value for field3
            ]
        '''
        integer_value = 0
        for (bitfield_name, bitfield_bits), value in zip(bitfield_map, values):
            integer_value = (integer_value << bitfield_bits) | value
        byte_data:bytearray = self._write_int_as_bytes(integer_value, byte_count)
    
    ###################
    ##### STRINGS #####
    ###################
    
    #########################
    ##### MIPS COMMANDS #####
    #########################

    #######################
    ##### CONVERSIONS #####
    #######################
    
    def create_asset_file_path(self,
            file_dir:str, asset_id:int, file_ext:str=".bin"):
        '''
        PyDoc
        '''
        asset_id_str:str = self._convert_int_to_str(asset_id, 0)
        file_path:str = f"{file_dir}{asset_id_str}{file_ext}"
        return file_path

    def _convert_int_to_str(self, int_val:int, leading_zero_count:int):
        '''
        PyDoc
        '''
        int_str:str = str(hex(int_val))[2:]
        if(int_val < 0):
            int_str = int_str[1:]
        str_val:str = int_str.zfill(leading_zero_count).upper()
        if(int_val < 0):
            str_val = f"-{str_val}"
        return str_val
    
    ######################
    ##### JSON FILES #####
    ######################

    def print_as_json(self, file_path:str):
        '''
        PyDoc
        '''
        with open(file_path, "w+") as json_file:
            json.dump(self._file_content, json_file, indent=4)
    
    ##########################
    ##### MAIN FUNCTIONS #####
    ##########################

    def _read_file(self):
        '''
        Reads a file as a byte array.
        '''
        with open(self._file_path, "rb+") as bin_file:
            self._file_content:bytearray = bytearray(bin_file.read())

    def save_changes(self, file_path:str=None):
        '''
        PyDoc
        '''
        if(file_path is None):
            file_path = self._file_path
        with open(file_path, "wb+") as bin_file:
            bin_file.write(self._file_content)

if __name__ == '__main__':
    pass
