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
from asset_editing.model.model_asset_ids import \
    ModelAssetId

###########################
##### LOCAL CONSTANTS #####
###########################

MODEL_EXT:str = ".bin"

TEST_OUTPUT_DIR:str = 'test_output/'
DECOMPRESSED_DIR:str = f'{TEST_OUTPUT_DIR}decompressed/'
MODEL_LOGGING_DIR:str = "asset_editing/model/model_logging/"

@unique
class TwoDimensionalModelEnums(StrEnum):
    FRAME_COUNT = auto()
    HEADER_UNK_2 = auto()
    HEADER_UNK_3 = auto()
    HEADER_UNK_4 = auto()
    HEADER_UNK_6 = auto()
    HEADER_UNK_8 = auto()
    HEADER_UNK_A = auto()
    HEADER_UNK_C = auto()
    HEADER_UNK_E = auto()
    FRAMES = auto()
    VERTICES = auto()
    DISPLAY_LIST = auto()

@unique
class FrameEnums(StrEnum):
    UNK_0 = auto()
    UNK_1 = auto()
    UNK_2 = auto()
    UNK_4 = auto()
    UNK_6 = auto()
    FRAME_OFFSET = auto()
    PIXELS = auto()

@unique
class TextureType(IntEnum):
    COLOR_INDEX_4_BIT =         (1 << 0)
    COLOR_INDEX_8_BIT =         (1 << 1)
    RED_GREEN_BLUE_ALPHA_5551 = (1 << 2)
    RED_GREEN_BLUE_ALPHA_8888 = (1 << 3)
    INTENSITY_ALPHA_44 =        (1 << 4)

@unique
class VertexEnums(StrEnum):
    X_POSITION = auto()
    Y_POSITION = auto()
    Z_POSITION = auto()
    U_COORDINATE = auto()
    V_COORDINATE = auto()
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    ALPHA = auto()

###########################
##### SETUP FUNCTIONS #####
###########################

def create_model_logging_dir():
    '''
    PyDoc
    '''
    if not os.path.exists(MODEL_LOGGING_DIR):
        os.makedirs(MODEL_LOGGING_DIR)
        print(f"The directory '{MODEL_LOGGING_DIR}' has been created.")
    else:
        print(f"The directory '{MODEL_LOGGING_DIR}' already exists.")

##################
##### MODELS #####
##################

class TwoDimensionalModel(Generic_Bin_File_Class):
    def __init__(self, file_dir:str, asset_id:int):
        '''
        PyDoc
        '''
        self._file_dir:str = file_dir
        self._asset_id:int = asset_id
        self._frames:dict = {}
        self._vertices:list = []
        self._display_list:list = []
        file_path:str = self.create_asset_file_path(file_dir, asset_id, MODEL_EXT)
        super().__init__(file_path)
    
    ###################
    ##### LOGGING #####
    ###################

    def print_model(self, file_path:str):
        '''
        PyDoc
        '''
        pass

    ########################
    ##### MODEL HEADER #####
    ########################

    def _read_2d_model_header(self):
        '''
        PyDoc
        '''
        frame_count:int = self._read_bytes_as_int(0x00, 2)
        header_unk_2:int = self._read_bytes_as_int(0x02, 1)
        header_unk_3:int = self._read_bytes_as_int(0x03, 1)
        header_unk_4:int = self._read_bytes_as_int(0x04, 2)
        header_unk_6:int = self._read_bytes_as_int(0x06, 2)
        header_unk_8:int = self._read_bytes_as_int(0x08, 2)
        header_unk_A:int = self._read_bytes_as_int(0x0A, 2)
        header_unk_C:int = self._read_bytes_as_int(0x0C, 2)
        header_unk_E:int = self._read_bytes_as_int(0x0E, 2)
        model_info:dict = {
            TwoDimensionalModelEnums.FRAME_COUNT: frame_count,
            TwoDimensionalModelEnums.HEADER_UNK_2: header_unk_2,
            TwoDimensionalModelEnums.HEADER_UNK_3: header_unk_3,
            TwoDimensionalModelEnums.HEADER_UNK_4: header_unk_4,
            TwoDimensionalModelEnums.HEADER_UNK_6: header_unk_6,
            TwoDimensionalModelEnums.HEADER_UNK_8: header_unk_8,
            TwoDimensionalModelEnums.HEADER_UNK_A: header_unk_A,
            TwoDimensionalModelEnums.HEADER_UNK_C: header_unk_C,
            TwoDimensionalModelEnums.HEADER_UNK_E: header_unk_E,
        }
        frames_start_address:int = self._read_bytes_as_int(0x10, 4)
        vertices_start_address:int = self._read_bytes_as_int(0x14, 4)
        display_list_start_address:int = self._read_bytes_as_int(0x18, 4)
        model_offsets:dict = {
            TwoDimensionalModelEnums.FRAMES: frames_start_address,
            TwoDimensionalModelEnums.VERTICES: vertices_start_address,
            TwoDimensionalModelEnums.DISPLAY_LIST: display_list_start_address,
        }
        return model_info, model_offsets

    ##################
    ##### FRAMES #####
    ##################

    def _read_2d_model_frames_header(self,
            frame_start_offset:int, frame_count:int):
        '''
        PyDoc
        '''
        start_index:int = 0x1C
        for curr_frame_count in range(frame_count):
            unk_0:int = self._read_bytes_as_int(start_index, 1)
            unk_1:int = self._read_bytes_as_int(start_index + 0x01, 1)
            unk_2:int = self._read_bytes_as_int(start_index + 0x02, 2)
            unk_4:int = self._read_bytes_as_int(start_index + 0x04, 2)
            unk_6:int = self._read_bytes_as_int(start_index + 0x06, 2) # Maybe Padding?
            frame_offset:int = self._read_bytes_as_int(start_index + 0x08, 4)
            self._frames[curr_frame_count] = {
                FrameEnums.UNK_0: unk_0,
                FrameEnums.UNK_1: unk_1,
                FrameEnums.UNK_2: unk_2,
                FrameEnums.UNK_4: unk_4,
                FrameEnums.UNK_6: unk_6,
                FrameEnums.FRAME_OFFSET: frame_offset,
                FrameEnums.PIXELS: [],
            }
            start_index += 0xC
        if(start_index % 0x8 == 0x4):
            next_bytes:int = self._read_bytes_as_int(start_index, 4)
            if(next_bytes != 0xAAAAAAAA):
                print("Error: Expected Padding Not Found")
                print(f"\tCurrent Index: {hex(start_index)}")
                print(f"\tNext Byte: {hex(next_bytes)}")
                raise Exception("Expected Padding Not Found")
                exit(1)
        for curr_frame_count in self._frames:
            frame_start_index:int = frame_start_offset + self._frames[curr_frame_count][FrameEnums.FRAME_OFFSET]
            self._read_frame_pixels(frame_start_index, curr_frame_count)
    
    def _read_frame_pixels(self,
            start_index:int, curr_frame_count:int):
        '''
        PyDoc
        '''
        pass

    ###############
    ##### UNK #####
    ###############

    def _read_2d_model_vertices(self,
            vertices_start_index:int, display_list_start_index:int):
        '''
        PyDoc
        '''
        vertex_info_length:int = 0x10
        for curr_index in range(vertices_start_index, display_list_start_index, vertex_info_length):
            x_position:int = self._read_bytes_as_int(curr_index, 2, True)
            y_position:int = self._read_bytes_as_int(curr_index + 0x02, 2, True)
            z_position:int = self._read_bytes_as_int(curr_index + 0x04, 2, True)
            # padding 2
            u_coordinate:int = self._read_bytes_as_int(curr_index + 0x08, 2, True)
            v_coordinate:int = self._read_bytes_as_int(curr_index + 0x0A, 2, True)
            red:int = self._read_bytes_as_int(curr_index + 0x0C, 1)
            green:int = self._read_bytes_as_int(curr_index + 0x0D, 1)
            blue:int = self._read_bytes_as_int(curr_index + 0x0E, 1)
            alpha:int = self._read_bytes_as_int(curr_index + 0x0F, 1)
            vertex_info:dict = {
                VertexEnums.X_POSITION: x_position,
                VertexEnums.Y_POSITION: y_position,
                VertexEnums.Z_POSITION: z_position,
                VertexEnums.U_COORDINATE: u_coordinate,
                VertexEnums.V_COORDINATE: v_coordinate,
                VertexEnums.RED: red,
                VertexEnums.GREEN: green,
                VertexEnums.BLUE: blue,
                VertexEnums.ALPHA: alpha,
            }
            self._vertices.append(vertex_info)

    ########################
    ##### DISPLAY LIST #####
    ########################

    def _read_2d_model_display_list(self, display_list_start_index:int):
        '''
        PyDoc
        '''
        end_of_file_index:int = len(self._file_content)
        display_list_command_length:int = 0x08
        for curr_index in range(display_list_start_index, end_of_file_index, display_list_command_length):
            display_list_command:int = self._read_bytes_as_int(curr_index, display_list_command_length)
            self._display_list.append(display_list_command)

    ################
    ##### MAIN #####
    ################

    def _read_file(self):
        '''
        PyDoc
        '''
        with open(self._file_path, "rb+") as bin_file:
            self._file_content:bytearray = bytearray(bin_file.read())
        header_unk_4:int = self._read_bytes_as_int(0x04, 2)
        if(header_unk_4 != 0x00BE):
            return
        model_info, model_offsets = self._read_2d_model_header()
        self._read_2d_model_frames_header(
            model_offsets[TwoDimensionalModelEnums.FRAMES],
            model_info[TwoDimensionalModelEnums.FRAME_COUNT])
        self._read_2d_model_vertices(
            model_offsets[TwoDimensionalModelEnums.VERTICES],
            model_offsets[TwoDimensionalModelEnums.DISPLAY_LIST]
            )
        self._read_2d_model_display_list(
            model_offsets[TwoDimensionalModelEnums.DISPLAY_LIST])