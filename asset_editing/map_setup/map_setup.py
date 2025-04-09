###################
##### IMPORTS #####
###################

import os
import sys

main_folder = os.path.dirname(os.path.abspath("..."))
sys.path.append(main_folder)

import json
from enum import IntEnum, StrEnum, auto, unique

from asset_editing.generic_file import Generic_Bin_File_Class
from asset_editing.map_setup.map_setup_asset_ids import \
    MapSetupAssetId
from asset_editing.map_setup.object_names import \
    CategoryEnum, OBJECT_NAMES

###########################
##### LOCAL CONSTANTS #####
###########################

LEVEL_SETUP_EXT:str = ".bin"

TEST_OUTPUT_DIR:str = 'test_output/'
DECOMPRESSED_DIR:str = f'{TEST_OUTPUT_DIR}decompressed/'
MAP_SETUP_LOGGING_DIR:str = "asset_editing/map_setup/map_setup_logging/"

@unique
class MapSetupEnums(StrEnum):
    CAMERAS = auto()
    OBJECTS = auto()
    UNKNOWN = auto()

@unique
class CameraEnums(StrEnum):
    CAMERA_ID = auto()
    CAMERA_TYPE = auto()
    POSITION = auto()
    X_POSITION = auto()
    Y_POSITION = auto()
    Z_POSITION = auto()
    ROTATION = auto()
    YAW = auto()
    PITCH = auto()
    ROLL = auto()
    SECTION_5 = auto()
    SECTION_5_LINE_1 = auto()
    SECTION_5_LINE_2 = auto()
    SECTION_5_LINE_3 = auto()
    SECTION_6 = auto()
    SECTION_6_LINE_1 = auto()
    SECTION_6_LINE_2 = auto()
    SECTION_7 = auto()
    SECTION_7_LINE_1 = auto()
    SECTION_7_LINE_2 = auto()
    SECTION_8 = auto()
    SECTION_8_LINE_1 = auto()
    SECTION_9 = auto()
    SECTION_9_LINE_1 = auto()
    SECTION_A = auto()
    SECTION_A_LINE_1 = auto()
    SECTION_B = auto()
    SECTION_B_LINE_1 = auto()
    SECTION_C = auto()
    SECTION_C_LINE_1 = auto()
    SECTION_D = auto()
    SECTION_D_LINE_1 = auto()
    SECTION_E = auto()
    SECTION_E_LINE_1 = auto()
    SECTION_F = auto()
    SECTION_F_LINE_1 = auto()
    SECTION_10 = auto()
    SECTION_10_LINE_1 = auto()
    SECTION_11 = auto()
    SECTION_11_LINE_1 = auto()
    SECTION_12 = auto()
    SECTION_12_LINE_1 = auto()
    SECTION_13 = auto()
    SECTION_13_LINE_1 = auto()

@unique
class ObjectEnum(StrEnum):
    OBJECT_NAME = auto()
    X_POSITION = auto()
    Y_POSITION = auto()
    Z_POSITION = auto()
    UNK_6_BIT_15 = auto()
    CATEGORY = auto()
    UNK_6_BIT_0 = auto()
    ACTOR_ID = auto()
    UNK_A = auto()
    UNK_B = auto()
    UNK_C_BIT_15 = auto() # Selector?
    SCALE = auto()
    UNK_10 = auto()
    UNK_11 = auto()
    UNK_12 = auto()
    UNK_13 = auto()

@unique
class UnknownEnum(StrEnum):
    UNKNOWN = auto()

###########################
##### SETUP FUNCTIONS #####
###########################

def create_map_setup_logging_dir():
    '''
    PyDoc
    '''
    if not os.path.exists(MAP_SETUP_LOGGING_DIR):
        os.makedirs(MAP_SETUP_LOGGING_DIR)
        print(f"The directory '{MAP_SETUP_LOGGING_DIR}' has been created.")
    else:
        print(f"The directory '{MAP_SETUP_LOGGING_DIR}' already exists.")

#####################
##### MAP SETUP #####
#####################

class Map_Setup(Generic_Bin_File_Class):
    def __init__(self, file_dir:str, asset_id:int):
        '''
        PyDoc
        '''
        self._file_dir:str = file_dir
        self._asset_id:int = asset_id
        self._cameras:dict = {}
        self._objects:list = []
        self._unknown:list = []
        file_path:str = self.create_asset_file_path(file_dir, asset_id, LEVEL_SETUP_EXT)
        super().__init__(file_path)
    
    ###################
    ##### LOGGING #####
    ###################

    def print_map_setup(self, file_path:str):
        '''
        PyDoc
        '''
        map_setup_dict:dict = {
            MapSetupEnums.CAMERAS: self._cameras,
            MapSetupEnums.OBJECTS: self._objects,
            MapSetupEnums.UNKNOWN: self._unknown,
        }
        with open(file_path, "w+") as json_file:
            json.dump(map_setup_dict, json_file, indent=4)
    
    ###################
    ##### CAMERAS #####
    ###################

    def _read_cameras(self, current_index:int):
        '''
        PyDoc
        '''
        highest_camera_id:int = self._read_bytes_as_int(current_index, 4) # Bruh IDK
        current_index += 4
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        while(next_bytes == 0x01):
            current_index = self._read_camera_info(current_index)
            next_bytes:int = self._read_bytes_as_int(current_index, 1)
        return current_index

    def _read_camera_info(self, current_index:int):
        '''
        PyDoc
        '''
        camera_id, current_index = self._read_camera_section_1(current_index)
        camera_type, current_index = self._read_camera_section_2(current_index)
        if(camera_type not in self._cameras):
            self._cameras[camera_type] = {}
        if(camera_type == 0x01):
            camera_info, current_index = self._read_camera_type_1(current_index)
        elif(camera_type == 0x02):
            camera_info, current_index = self._read_camera_type_2(current_index)
        elif(camera_type == 0x03):
            camera_info, current_index = self._read_camera_type_3(current_index)
        elif(camera_type == 0x04):
            camera_info, current_index = self._read_camera_type_4(current_index)
        elif(camera_type == 0x05):
            camera_info, current_index = self._read_camera_type_5(current_index)
        elif(camera_type == 0x06):
            camera_info, current_index = self._read_camera_type_6(current_index)
        elif(camera_type == 0x07):
            camera_info, current_index = self._read_camera_type_7(current_index)
        elif(camera_type == 0x08):
            camera_info, current_index = self._read_camera_type_8(current_index)
        else:
            print("Error: Camera Type Does Not Match Known Types")
            print(f"\tCurrent Index: {hex(current_index - 1)}")
            print(f"\tNext Byte: {hex(camera_type)}")
            exit(1)
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x00):
            print("Error: Camera Info did not end with 0x00")
            print(f"Camera Id: {camera_id}")
            print(f"Camera Type: {camera_type}")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        self._cameras[camera_type][camera_id] = camera_info
        return current_index

    ### CAMERA SECTIONS ###

    def _read_camera_section_1(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x01):
            print("Error: Camera Id Section did not start with 0x01")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        camera_id:int = self._read_bytes_as_int(current_index, 4)
        current_index += 4
        return camera_id, current_index

    def _read_camera_section_2(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x02):
            print("Error: Camera Type Section did not start with 0x02")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        camera_type:int = self._read_bytes_as_int(current_index, 4)
        current_index += 4
        return camera_type, current_index

    def _read_camera_section_3(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x03):
            print("Error: Camera Position Section did not start with 0x03")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        x_position:float = self._read_bytes_as_float(current_index)
        current_index += 4
        y_position:float = self._read_bytes_as_float(current_index)
        current_index += 4
        z_position:float = self._read_bytes_as_float(current_index)
        current_index += 4
        return x_position, y_position, z_position, current_index

    def _read_camera_section_4(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x04):
            print("Error: Camera Rotation Section did not start with 0x04")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        yaw:float = self._read_bytes_as_float(current_index)
        current_index += 4
        pitch:float = self._read_bytes_as_float(current_index)
        current_index += 4
        roll:float = self._read_bytes_as_float(current_index)
        current_index += 4
        return yaw, pitch, roll, current_index

    def _read_camera_section_5(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x05):
            print("Error: Camera Section 5 did not start with 0x05")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        section_5_line_1:float = self._read_bytes_as_float(current_index)
        current_index += 4
        section_5_line_2:float = self._read_bytes_as_float(current_index)
        current_index += 4
        section_5_line_3:float = self._read_bytes_as_float(current_index)
        current_index += 4
        return section_5_line_1, section_5_line_2, section_5_line_3, current_index

    def _read_camera_section_6(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x06):
            print("Error: Camera Section 6 did not start with 0x06")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        section_6_line_1:float = self._read_bytes_as_float(current_index)
        current_index += 4
        section_6_line_2:float = self._read_bytes_as_float(current_index)
        current_index += 4
        return section_6_line_1, section_6_line_2, current_index

    def _read_camera_section_7(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x07):
            print("Error: Camera Section 7 did not start with 0x07")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        section_7_line_1:float = self._read_bytes_as_float(current_index)
        current_index += 4
        section_7_line_2:float = self._read_bytes_as_float(current_index)
        current_index += 4
        return section_7_line_1, section_7_line_2, current_index

    def _read_camera_section_8(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x08):
            print("Error: Camera Section 8 did not start with 0x08")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        section_8_line_1:float = self._read_bytes_as_float(current_index)
        current_index += 4
        return section_8_line_1, current_index

    def _read_camera_section_9(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x09):
            print("Error: Camera Section 9 did not start with 0x09")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        section_9_line_1:float = self._read_bytes_as_float(current_index)
        current_index += 4
        return section_9_line_1, current_index

    def _read_camera_section_A(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x0A):
            print("Error: Camera Section A did not start with 0x0A")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        section_a_line_1:int = self._read_bytes_as_int(current_index, 2, True)
        current_index += 2
        return section_a_line_1, current_index

    def _read_camera_section_B(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x0B):
            print("Error: Camera Section B did not start with 0x0B")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        section_b_line_1:float = self._read_bytes_as_float(current_index)
        current_index += 4
        return section_b_line_1, current_index

    def _read_camera_section_C(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x0C):
            print("Error: Camera Section C did not start with 0x0C")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        section_c_line_1:float = self._read_bytes_as_float(current_index)
        current_index += 4
        return section_c_line_1, current_index

    def _read_camera_section_D(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x0D):
            print("Error: Camera Section D did not start with 0x0D")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        section_d_line_1:int = self._read_bytes_as_int(current_index, 4, True)
        current_index += 4
        return section_d_line_1, current_index

    def _read_camera_section_E(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x0E):
            print("Error: Camera Section E did not start with 0x0E")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        section_e_line_1:int = self._read_bytes_as_int(current_index, 4, True)
        current_index += 4
        return section_e_line_1, current_index

    def _read_camera_section_F(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x0F):
            print("Error: Camera Section F did not start with 0x0F")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        section_f_line_1:int = self._read_bytes_as_int(current_index, 4, True)
        current_index += 4
        return section_f_line_1, current_index

    def _read_camera_section_10(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x10):
            print("Error: Camera Section 10 did not start with 0x10")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        section_10_line_1:int = self._read_bytes_as_int(current_index, 4, True)
        current_index += 4
        return section_10_line_1, current_index

    def _read_camera_section_11(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x11):
            print("Error: Camera Section 11 did not start with 0x11")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        section_11_line_1:float = self._read_bytes_as_float(current_index)
        current_index += 4
        return section_11_line_1, current_index

    def _read_camera_section_12(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x12):
            print("Error: Camera Section 12 did not start with 0x12")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        section_12_line_1:float = self._read_bytes_as_float(current_index)
        current_index += 4
        return section_12_line_1, current_index

    def _read_camera_section_13(self, current_index:int):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(current_index, 1)
        if(next_bytes != 0x13):
            print("Error: Camera Section 13 did not start with 0x13")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 1
        section_13_line_1:int = self._read_bytes_as_int(current_index, 4, True)
        current_index += 4
        return section_13_line_1, current_index

    ### CAMERA TYPES ###

    def _read_camera_type_1(self, current_index:int):
        '''
        PyDoc
        '''
        x_position, y_position, z_position, current_index = \
            self._read_camera_section_3(current_index)
        section_5_line_1, section_5_line_2, section_5_line_3, current_index =\
            self._read_camera_section_5(current_index)
        section_6_line_1, section_6_line_2, current_index =\
            self._read_camera_section_6(current_index)
        section_7_line_1, section_7_line_2, current_index = \
            self._read_camera_section_7(current_index)
        section_d_line_1, current_index = self._read_camera_section_D(current_index)
        camera_info:dict = {
            CameraEnums.POSITION: {
                CameraEnums.X_POSITION: x_position,
                CameraEnums.Y_POSITION: y_position,
                CameraEnums.Z_POSITION: z_position,
            },
            CameraEnums.SECTION_5: {
                CameraEnums.SECTION_5_LINE_1: section_5_line_1,
                CameraEnums.SECTION_5_LINE_2: section_5_line_2,
                CameraEnums.SECTION_5_LINE_3: section_5_line_3,
            },
            CameraEnums.SECTION_6: {
                CameraEnums.SECTION_6_LINE_1: section_6_line_1,
                CameraEnums.SECTION_6_LINE_2: section_6_line_2,
            },
            CameraEnums.SECTION_7: {
                CameraEnums.SECTION_7_LINE_1: section_7_line_1,
                CameraEnums.SECTION_7_LINE_2: section_7_line_2,
            },
            CameraEnums.SECTION_D: {
                CameraEnums.SECTION_D_LINE_1: section_d_line_1,
            },
        }
        return camera_info, current_index

    def _read_camera_type_2(self, current_index:int):
        '''
        PyDoc
        '''
        x_position, y_position, z_position, current_index = \
            self._read_camera_section_3(current_index)
        yaw, pitch, roll, current_index = \
            self._read_camera_section_4(current_index)
        camera_info:dict = {
            CameraEnums.POSITION: {
                CameraEnums.X_POSITION: x_position,
                CameraEnums.Y_POSITION: y_position,
                CameraEnums.Z_POSITION: z_position,
            },
            CameraEnums.ROTATION: {
                CameraEnums.YAW: yaw,
                CameraEnums.PITCH: pitch,
                CameraEnums.ROLL: roll,
            },
        }
        return camera_info, current_index

    def _read_camera_type_3(self, current_index:int):
        '''
        PyDoc
        '''
        x_position, y_position, z_position, current_index = \
            self._read_camera_section_3(current_index)
        section_5_line_1, section_5_line_2, section_5_line_3, current_index =\
            self._read_camera_section_5(current_index)
        section_6_line_1, section_6_line_2, current_index =\
            self._read_camera_section_6(current_index)
        section_7_line_1, section_7_line_2, current_index = \
            self._read_camera_section_7(current_index)
        section_b_line_1, current_index = self._read_camera_section_B(current_index)
        section_c_line_1, current_index = self._read_camera_section_C(current_index)
        section_d_line_1, current_index = self._read_camera_section_D(current_index)
        camera_info:dict = {
            CameraEnums.POSITION: {
                CameraEnums.X_POSITION: x_position,
                CameraEnums.Y_POSITION: y_position,
                CameraEnums.Z_POSITION: z_position,
            },
            CameraEnums.SECTION_5: {
                CameraEnums.SECTION_5_LINE_1: section_5_line_1,
                CameraEnums.SECTION_5_LINE_2: section_5_line_2,
                CameraEnums.SECTION_5_LINE_3: section_5_line_3,
            },
            CameraEnums.SECTION_6: {
                CameraEnums.SECTION_6_LINE_1: section_6_line_1,
                CameraEnums.SECTION_6_LINE_2: section_6_line_2,
            },
            CameraEnums.SECTION_7: {
                CameraEnums.SECTION_7_LINE_1: section_7_line_1,
                CameraEnums.SECTION_7_LINE_2: section_7_line_2,
            },
            CameraEnums.SECTION_B: {
                CameraEnums.SECTION_B_LINE_1: section_b_line_1,
            },
            CameraEnums.SECTION_C: {
                CameraEnums.SECTION_C_LINE_1: section_c_line_1,
            },
            CameraEnums.SECTION_D: {
                CameraEnums.SECTION_D_LINE_1: section_d_line_1,
            },
        }
        return camera_info, current_index

    def _read_camera_type_4(self, current_index:int):
        '''
        PyDoc
        '''
        section_d_line_1, current_index = self._read_camera_section_D(current_index)
        section_e_line_1, current_index = self._read_camera_section_E(current_index)
        section_f_line_1, current_index = self._read_camera_section_F(current_index)
        section_10_line_1, current_index = self._read_camera_section_10(current_index)
        section_12_line_1, current_index = self._read_camera_section_12(current_index)
        section_13_line_1, current_index = self._read_camera_section_13(current_index)
        camera_info:dict = {
            CameraEnums.SECTION_D: {
                CameraEnums.SECTION_D_LINE_1: section_d_line_1,
            },
            CameraEnums.SECTION_E: {
                CameraEnums.SECTION_E_LINE_1: section_e_line_1,
            },
            CameraEnums.SECTION_F: {
                CameraEnums.SECTION_F_LINE_1: section_f_line_1,
            },
            CameraEnums.SECTION_10: {
                CameraEnums.SECTION_10_LINE_1: section_10_line_1,
            },
            CameraEnums.SECTION_12: {
                CameraEnums.SECTION_12_LINE_1: section_12_line_1,
            },
            CameraEnums.SECTION_13: {
                CameraEnums.SECTION_13_LINE_1: section_13_line_1,
            },
        }
        return camera_info, current_index

    def _read_camera_type_5(self, current_index:int):
        '''
        PyDoc
        '''
        x_position, y_position, z_position, current_index = \
            self._read_camera_section_3(current_index)
        yaw, pitch, roll, current_index = \
            self._read_camera_section_4(current_index)
        section_8_line_1, current_index = self._read_camera_section_8(current_index)
        section_9_line_1, current_index = self._read_camera_section_9(current_index)
        section_11_line_1, current_index = self._read_camera_section_11(current_index)
        section_a_line_1, current_index = self._read_camera_section_A(current_index)
        section_d_line_1, current_index = self._read_camera_section_D(current_index)
        camera_info:dict = {
            CameraEnums.POSITION: {
                CameraEnums.X_POSITION: x_position,
                CameraEnums.Y_POSITION: y_position,
                CameraEnums.Z_POSITION: z_position,
            },
            CameraEnums.ROTATION: {
                CameraEnums.YAW: yaw,
                CameraEnums.PITCH: pitch,
                CameraEnums.ROLL: roll,
            },
            CameraEnums.SECTION_8: {
                CameraEnums.SECTION_8_LINE_1: section_8_line_1,
            },
            CameraEnums.SECTION_9: {
                CameraEnums.SECTION_9_LINE_1: section_9_line_1,
            },
            CameraEnums.SECTION_11: {
                CameraEnums.SECTION_11_LINE_1: section_11_line_1,
            },
            CameraEnums.SECTION_A: {
                CameraEnums.SECTION_A_LINE_1: section_a_line_1,
            },
            CameraEnums.SECTION_D: {
                CameraEnums.SECTION_D_LINE_1: section_d_line_1,
            },
        }
        return camera_info, current_index

    def _read_camera_type_6(self, current_index:int):
        '''
        PyDoc
        '''
        x_position, y_position, z_position, current_index = \
            self._read_camera_section_3(current_index)
        yaw, pitch, roll, current_index = \
            self._read_camera_section_4(current_index)
        section_8_line_1, current_index = self._read_camera_section_8(current_index)
        section_9_line_1, current_index = self._read_camera_section_9(current_index)
        section_11_line_1, current_index = self._read_camera_section_11(current_index)
        section_a_line_1, current_index = self._read_camera_section_A(current_index)
        section_b_line_1, current_index = self._read_camera_section_B(current_index)
        section_d_line_1, current_index = self._read_camera_section_D(current_index)
        section_f_line_1, current_index = self._read_camera_section_F(current_index)
        camera_info:dict = {
            CameraEnums.POSITION: {
                CameraEnums.X_POSITION: x_position,
                CameraEnums.Y_POSITION: y_position,
                CameraEnums.Z_POSITION: z_position,
            },
            CameraEnums.ROTATION: {
                CameraEnums.YAW: yaw,
                CameraEnums.PITCH: pitch,
                CameraEnums.ROLL: roll,
            },
            CameraEnums.SECTION_8: {
                CameraEnums.SECTION_8_LINE_1: section_8_line_1,
            },
            CameraEnums.SECTION_9: {
                CameraEnums.SECTION_9_LINE_1: section_9_line_1,
            },
            CameraEnums.SECTION_11: {
                CameraEnums.SECTION_11_LINE_1: section_11_line_1,
            },
            CameraEnums.SECTION_A: {
                CameraEnums.SECTION_A_LINE_1: section_a_line_1,
            },
            CameraEnums.SECTION_B: {
                CameraEnums.SECTION_B_LINE_1: section_b_line_1,
            },
            CameraEnums.SECTION_D: {
                CameraEnums.SECTION_D_LINE_1: section_d_line_1,
            },
            CameraEnums.SECTION_F: {
                CameraEnums.SECTION_F_LINE_1: section_f_line_1,
            },
        }
        return camera_info, current_index

    def _read_camera_type_7(self, current_index:int):
        '''
        PyDoc
        '''
        section_f_line_1, current_index = self._read_camera_section_F(current_index)
        camera_info:dict = {
            CameraEnums.SECTION_F: {
                CameraEnums.SECTION_F_LINE_1: section_f_line_1,
            },
        }
        return camera_info, current_index
    
    def _read_camera_type_8(self, current_index:int):
        '''
        PyDoc
        '''
        x_position, y_position, z_position, current_index = \
            self._read_camera_section_3(current_index)
        yaw, pitch, roll, current_index = \
            self._read_camera_section_4(current_index)
        section_9_line_1, current_index = self._read_camera_section_9(current_index)
        section_11_line_1, current_index = self._read_camera_section_11(current_index)
        section_a_line_1, current_index = self._read_camera_section_A(current_index)
        section_d_line_1, current_index = self._read_camera_section_D(current_index)
        section_f_line_1, current_index = self._read_camera_section_F(current_index)
        camera_info:dict = {
            CameraEnums.POSITION: {
                CameraEnums.X_POSITION: x_position,
                CameraEnums.Y_POSITION: y_position,
                CameraEnums.Z_POSITION: z_position,
            },
            CameraEnums.ROTATION: {
                CameraEnums.YAW: yaw,
                CameraEnums.PITCH: pitch,
                CameraEnums.ROLL: roll,
            },
            CameraEnums.SECTION_9: {
                CameraEnums.SECTION_9_LINE_1: section_9_line_1,
            },
            CameraEnums.SECTION_11: {
                CameraEnums.SECTION_11_LINE_1: section_11_line_1,
            },
            CameraEnums.SECTION_A: {
                CameraEnums.SECTION_A_LINE_1: section_a_line_1,
            },
            CameraEnums.SECTION_D: {
                CameraEnums.SECTION_D_LINE_1: section_d_line_1,
            },
            CameraEnums.SECTION_F: {
                CameraEnums.SECTION_F_LINE_1: section_f_line_1,
            },
        }
        return camera_info, current_index

    ###################
    ##### OBJECTS #####
    ###################

    def _read_objects(self, current_index:int):
        '''
        PyDoc
        '''
        num_of_objects:int = self._read_bytes_as_int(current_index, 4)
        current_index += 4
        current_object_count:int = 0
        while(current_object_count < num_of_objects):
            current_index = self._read_object(current_index)
            current_object_count += 1
        return current_index

    def _read_object(self, current_index:int):
        '''
        PyDoc
        '''
        x_position:int = self._read_bytes_as_int(current_index, 2, check_for_negative=True)
        current_index += 2
        y_position:int = self._read_bytes_as_int(current_index, 2, check_for_negative=True)
        current_index += 2
        z_position:int = self._read_bytes_as_int(current_index, 2, check_for_negative=True)
        current_index += 2
        byte_6_u16_bitfield:list = [
            (ObjectEnum.UNK_6_BIT_15, 9),
            (ObjectEnum.CATEGORY, 6),
            (ObjectEnum.UNK_6_BIT_0, 1),
        ]
        byte_6_u16_dict:dict = self._read_bytes_as_bitfield(current_index, 2, byte_6_u16_bitfield)
        current_index += 2
        actor_id:int = self._read_bytes_as_int(current_index, 2)
        current_index += 2
        unk_A:int = self._read_bytes_as_int(current_index, 1)
        current_index += 1
        unk_B:int = self._read_bytes_as_int(current_index, 1)
        current_index += 1
        byte_C_u32_bitfield:list = [
            (ObjectEnum.UNK_C_BIT_15, 9),
            (ObjectEnum.SCALE, 23),
        ]
        byte_C_u32_dict:dict = self._read_bytes_as_bitfield(current_index, 4, byte_C_u32_bitfield)
        current_index += 4
        unk_10:int = self._read_bytes_as_int(current_index, 1)
        current_index += 1
        unk_11:int = self._read_bytes_as_int(current_index, 1)
        current_index += 1
        unk_12:int = self._read_bytes_as_int(current_index, 1)
        current_index += 1
        unk_13:int = self._read_bytes_as_int(current_index, 1)
        current_index += 1
        object_info:dict = {
            ObjectEnum.X_POSITION: x_position,
            ObjectEnum.Y_POSITION: y_position,
            ObjectEnum.Z_POSITION: z_position,
            ObjectEnum.UNK_6_BIT_15: byte_6_u16_dict[ObjectEnum.UNK_6_BIT_15],
            ObjectEnum.CATEGORY: byte_6_u16_dict[ObjectEnum.CATEGORY],
            ObjectEnum.UNK_6_BIT_0: byte_6_u16_dict[ObjectEnum.UNK_6_BIT_0],
            ObjectEnum.ACTOR_ID: actor_id,
            ObjectEnum.UNK_A: unk_A,
            ObjectEnum.UNK_B: unk_B,
            ObjectEnum.UNK_C_BIT_15: byte_C_u32_dict[ObjectEnum.UNK_C_BIT_15],
            ObjectEnum.SCALE: byte_C_u32_dict[ObjectEnum.SCALE],
            ObjectEnum.UNK_10: unk_10,
            ObjectEnum.UNK_11: unk_11,
            ObjectEnum.UNK_12: unk_12,
            ObjectEnum.UNK_13: unk_13,
        }
        object_name:str = self._determinte_object_name(object_info)
        object_info[ObjectEnum.OBJECT_NAME] = object_name
        self._objects.append(object_info)
        return current_index

    def _determinte_object_name(self, object_info:dict):
        '''
        PyDoc
        '''
        object_name:str = "Unknown"
        category:int = object_info[ObjectEnum.CATEGORY]
        category_name:CategoryEnum = CategoryEnum.name_for_value(category)
        if(not category_name):
            return object_name
        actor_id:str = object_info[ObjectEnum.ACTOR_ID]
        object_sub_name:str = OBJECT_NAMES[category].get(actor_id)
        if(not object_sub_name):
            object_sub_name:str = "Unknown"
        object_name:str = f"{category_name} - {object_sub_name}"
        return object_name

    ###################
    ##### UNKNOWN #####
    ###################

    def _read_unknown(self, current_index:int):
        '''
        PyDoc
        '''
        file_length:int = len(self._file_content)
        unknown_bytes:int = self._read_bytes_as_int(current_index, file_length - current_index)
        self._unknown.append(unknown_bytes)

    ################
    ##### MAIN #####
    ################

    def _read_file(self):
        '''
        PyDoc
        '''
        with open(self._file_path, "rb+") as bin_file:
            self._file_content:bytearray = bytearray(bin_file.read())
        current_index:int = 0x00
        next_bytes:int = self._read_bytes_as_int(current_index, 2)
        if(next_bytes != 0x0614):
            print("Error: Map Setup File did not start with 0x0614")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 0x02
        # Cameras
        current_index = self._read_cameras(current_index)
        # Objects
        next_bytes:int = self._read_bytes_as_int(current_index, 3)
        if(next_bytes != 0x00070A):
            print("Error: Objects List did not start with 0x00070A")
            print(f"\tCurrent Index: {hex(current_index)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            exit(1)
        current_index += 3
        current_index = self._read_objects(current_index)
        # Unknown
        self._read_unknown(current_index)

if __name__ == '__main__':
    create_map_setup_logging_dir()
    for asset_id in MapSetupAssetId:
        asset_id_name:str = asset_id.name
        asset_id_value:int = asset_id.value
        print(f"{hex(asset_id_value)} - {asset_id_name}")
        map_obj = Map_Setup(DECOMPRESSED_DIR, asset_id)
        asset_id_str:str = map_obj._convert_int_to_str(asset_id.value, 4)
        file_path:str = f"{MAP_SETUP_LOGGING_DIR}{asset_id_name}.json"
        map_obj.print_map_setup(file_path)