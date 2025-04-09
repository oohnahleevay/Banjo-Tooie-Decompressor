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

###########################
##### LOCAL CONSTANTS #####
###########################

MODEL_EXT:str = ".bin"

TEST_OUTPUT_DIR:str = 'test_output/'
DECOMPRESSED_DIR:str = f'{TEST_OUTPUT_DIR}decompressed/'
MODEL_LOGGING_DIR:str = "asset_editing/model/model_logging/"

@unique
class ThreeDimensionalModelEnums(StrEnum):
    GEOMETRY_LAYOUT = auto()
    TEXTURES = auto()
    DISPLAY_LIST = auto()
    VERTICES = auto()
    ANIMATIONS = auto()
    COLLISIONS = auto()
    UNK_20 = auto()
    EFFECTS = auto()
    VERTEX_BONE_MAPPING = auto()
    TEXTURE_ANIMATIONS = auto()
    UNK_34 = auto()
    VERTEX_NORMALS = auto()
    TRI_COUNT = auto()
    VERT_COUNT = auto()

@unique
class TextureEnums(StrEnum):
    MIP_MAPPING = auto()
    TEXTURE_TYPE = auto()
    X_PIXEL_GRID = auto()
    Y_PIXEL_GRID = auto()
    COLOR_INDEX = auto()
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
    U_POSITION = auto()
    V_POSITION = auto()
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

class ThreeDimensionalModel(Generic_Bin_File_Class):
    def __init__(self, file_dir:str, asset_id:int):
        '''
        PyDoc
        '''
        self._file_dir:str = file_dir
        self._asset_id:int = asset_id
        self._geo_type:int = None
        self._geometry_layout:dict = {}
        self._textures:dict = {}
        self._display_list:dict = {}
        self._vertices:dict = {}
        self._animations:dict = {}
        self._collision:dict = {}
        self._unk_20:dict = {}
        self._effects:dict = {}
        self._vertex_bone_mapping:dict = {}
        self._texture_animations:dict = {}
        self._unk_34:dict = {}
        self._vertex_normals:dict = {}
        self._tri_count:int = None
        self._vert_count:int = None
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

    def _validate_model_file(self):
        '''
        PyDoc
        '''
        next_bytes:int = self._read_bytes_as_int(0x00, 4)
        if(next_bytes != 0x0000000B):
            print("Error: Model File did not start with 0x0000000B")
            print(f"\tCurrent Index: {hex(0x00)}")
            print(f"\tNext Bytes: {hex(next_bytes)}")
            raise Exception("Invalid 3D Model File Header")
            exit(1)

    def _read_3d_model_header(self):
        '''
        PyDoc
        '''
        geometry_layout_offset:int = self._read_bytes_as_int(0x04, 4)
        texture_setup_offset:int = self._read_bytes_as_int(0x08, 2)
        self._geo_type:int = self._read_bytes_as_int(0x0A, 2)
        display_list_setup_offset:int = self._read_bytes_as_int(0x0C, 4)
        vertex_store_setup_offset:int = self._read_bytes_as_int(0x10, 4)
        # padding 4?
        animation_setup:int = self._read_bytes_as_int(0x18, 4)
        collision_setup:int = self._read_bytes_as_int(0x1C, 4)
        unk_20:int = self._read_bytes_as_int(0x20, 4)
        effects_setup:int = self._read_bytes_as_int(0x24, 4)
        vertex_bone_mapping:int = self._read_bytes_as_int(0x28, 4)
        texture_animation_setup:int = self._read_bytes_as_int(0x2C, 4)
        # padding 4?
        unk_34:int = self._read_bytes_as_int(0x34, 4)
        vertex_normals_offset:int = self._read_bytes_as_int(0x38, 4)
        tri_count:int = self._read_bytes_as_int(0x44, 2)
        vert_count:int = self._read_bytes_as_int(0x46, 2)
        # padding 8?
        model_offsets:dict = {
            ThreeDimensionalModelEnums.GEOMETRY_LAYOUT: geometry_layout_offset,
            ThreeDimensionalModelEnums.TEXTURES: texture_setup_offset,
            ThreeDimensionalModelEnums.DISPLAY_LIST: display_list_setup_offset,
            ThreeDimensionalModelEnums.VERTICES: vertex_store_setup_offset,
            ThreeDimensionalModelEnums.ANIMATIONS: animation_setup,
            ThreeDimensionalModelEnums.COLLISIONS: collision_setup,
            ThreeDimensionalModelEnums.UNK_20: unk_20,
            ThreeDimensionalModelEnums.EFFECTS: effects_setup,
            ThreeDimensionalModelEnums.VERTEX_BONE_MAPPING: vertex_bone_mapping,
            ThreeDimensionalModelEnums.TEXTURE_ANIMATIONS: texture_animation_setup,
            ThreeDimensionalModelEnums.UNK_34: unk_34,
            ThreeDimensionalModelEnums.VERTEX_NORMALS: vertex_normals_offset,
        }
        return model_offsets

    ##################################
    ##### GEOMETRY LAYOUT OFFSET #####
    ##################################

    def _read_3d_model_geometry_layout_header(self):
        '''
        PyDoc
        '''
        pass

    ####################
    ##### TEXTURES #####
    ####################

    def _read_3d_model_texture_header(self, index_start:int):
        '''
        PyDoc
        '''
        # Might need segmented branch for display list stuff
        bytes_to_load:int = self._read_bytes_as_int(index_start, 4)
        texture_count:int = self._read_bytes_as_int(index_start + 0x04, 2)
        external_textures:int = self._read_bytes_as_int(index_start + 0x06, 2)
        textures_starting_address:int = index_start + 0x08 + 0x08 * texture_count
        for current_count in range(texture_count):
            texture_info_start_index:int = index_start + 0x08 + 0x08 * current_count
            texture_segment_address:int = self._read_bytes_as_int(texture_info_start_index, 4)
            mip_mapping:int = self._read_bytes_as_int(texture_info_start_index + 0x04, 1)
            texture_type:int = self._read_bytes_as_int(texture_info_start_index + 0x05, 1)
            x_pixel_grid:int = self._read_bytes_as_int(texture_info_start_index + 0x06, 1)
            y_pixel_grid:int = self._read_bytes_as_int(texture_info_start_index + 0x07, 1)
            texture_info:dict = {
                TextureEnums.MIP_MAPPING: mip_mapping,
                TextureEnums.TEXTURE_TYPE: texture_type,
                TextureEnums.X_PIXEL_GRID: x_pixel_grid,
                TextureEnums.Y_PIXEL_GRID: y_pixel_grid,
                TextureEnums.COLOR_INDEX: [],
                TextureEnums.PIXELS: [],
            }
            texture_start_address:int = textures_starting_address + texture_segment_address
            texture_info:dict = self._read_texture_pixels(texture_start_address, texture_info)
            self._textures[current_count] = texture_info
    
    def _read_3d_model_texture_pixels(self, texture_start_address:int, texture_info:dict):
        '''
        PyDoc
        '''
        texture_type:int = texture_info[TextureEnums.TEXTURE_TYPE]
        # texture_type -> 1 << Num
        if(texture_type == TextureType.COLOR_INDEX_4_BIT):
            texture_info:dict = self._read_color_index_4_bit_texture(texture_start_address, texture_info)
        elif(texture_type == TextureType.COLOR_INDEX_8_BIT):
            texture_info:dict = self._read_color_index_8_bit_texture(texture_start_address, texture_info)
        elif(texture_type == TextureType.RED_GREEN_BLUE_ALPHA_5551):
            texture_info:dict = self._read_red_blue_green_alpha_5551_texture(texture_start_address, texture_info)
        elif(texture_type == TextureType.RED_GREEN_BLUE_ALPHA_8888):
            texture_info:dict = self._read_red_blue_green_alpha_8888_texture(texture_start_address, texture_info)
        elif(texture_type == TextureType.INTENSITY_ALPHA_44):
            texture_info:dict = self._read_intensity_alpha_44_texture(texture_start_address, texture_info)
        else:
            print(f"ERROR: Unknown Texture Type {hex(texture_type)}")
            raise Exception("Unknown Texture Type")
            exit(1)
        return texture_info

    def _parse_red_green_blue_alpha_5551_color(self, color:int):
        '''
        PyDoc
        '''
        red:int = color >> 11
        green:int = (color >> 6) & 0b11111
        blue:int = (color >> 1) & 0b11111
        alpha:int = color & 1
        return red, green, blue, alpha

    def _parse_red_green_blue_alpha_8888_color(self, color:int):
        '''
        PyDoc
        '''
        red:int = color >> 0x18
        green:int = (color >> 0x10) & 0b11111111
        blue:int = (color >> 0x8) & 0b11111111
        alpha:int = color & 0b11111111
        return red, green, blue, alpha
    
    def _parse_intensity_alpha_44_color(self, color:int):
        '''
        PyDoc
        '''
        intensity:int = color >> 4
        alpha:int = color & 0b1111
        return intensity, alpha

    def _read_rgba_5551_color_index(self,
            texture_start_address:int, texture_info:dict, color_index_size:int):
        '''
        PyDoc
        '''
        color_byte_size:int = 0x2
        text_end_address:int = texture_start_address + color_index_size * color_byte_size
        for start_index in range(texture_start_address, text_end_address, color_byte_size):
            color:int = self._read_bytes_as_int(start_index, 2)
            parsed_color:tuple = self._parse_red_green_blue_alpha_5551_color(color)
            texture_info[TextureEnums.COLOR_INDEX].append(parsed_color)
        return texture_info, text_end_address

    def _read_color_index_4_bit_texture(self,
            texture_start_address:int, texture_info:dict):
        '''
        PyDoc
        '''
        # Color Index
        color_index_size:int = 0x10
        texture_info, pixel_start_address = \
            self._read_rgba_5551_color_index(texture_start_address, texture_info, color_index_size)
        # Pixels
        x_size:int = texture_info[TextureEnums.X_PIXEL_GRID]
        y_size:int = texture_info[TextureEnums.Y_PIXEL_GRID]
        pixel_end_address:int = pixel_start_address + (x_size * y_size) // 2
        for pixel_byte in range(pixel_start_address, pixel_end_address):
            byte_val:int = self._read_bytes_as_int(pixel_byte, 1)
            left_color_index_val:int = byte_val >> 4
            right_color_index_val:int = byte_val & 0b1111
            texture_info[TextureEnums.PIXELS].append(left_color_index_val)
            texture_info[TextureEnums.PIXELS].append(right_color_index_val)
        return texture_info

    def _read_color_index_8_bit_texture(self,
            texture_start_address:int, texture_info:dict):
        '''
        PyDoc
        '''
        # Color Index
        color_index_size:int = 0x100
        texture_info, pixel_start_address = \
            self._read_rgba_5551_color_index(texture_start_address, texture_info, color_index_size)
        # Pixels
        x_size:int = texture_info[TextureEnums.X_PIXEL_GRID]
        y_size:int = texture_info[TextureEnums.Y_PIXEL_GRID]
        pixel_end_address:int = pixel_start_address + x_size * y_size
        for pixel_byte in range(pixel_start_address, pixel_end_address):
            color_index_val:int = self._read_bytes_as_int(pixel_byte, 1)
            texture_info[TextureEnums.PIXELS].append(color_index_val)
        return texture_info

    def _read_red_blue_green_alpha_5551_texture(self,
            texture_start_address:int, texture_info:dict):
        '''
        PyDoc
        '''
        x_size:int = texture_info[TextureEnums.X_PIXEL_GRID]
        y_size:int = texture_info[TextureEnums.Y_PIXEL_GRID]
        color_byte_size:int = 0x02
        texture_end_address:int = texture_start_address + (x_size * y_size) * color_byte_size
        for pixel_byte in range(texture_start_address, texture_end_address, color_byte_size):
            color:int = self._read_bytes_as_int(pixel_byte, 2)
            parsed_color:tuple = self._parse_red_green_blue_alpha_5551_color(color)
            texture_info[TextureEnums.PIXELS].append(parsed_color)
        return texture_info

    def _read_red_blue_green_alpha_8888_texture(self,
            texture_start_address:int, texture_info:dict):
        '''
        PyDoc
        '''
        x_size:int = texture_info[TextureEnums.X_PIXEL_GRID]
        y_size:int = texture_info[TextureEnums.Y_PIXEL_GRID]
        color_byte_size:int = 0x04
        texture_end_address:int = texture_start_address + (x_size * y_size) * color_byte_size
        for pixel_byte in range(texture_start_address, texture_end_address, color_byte_size):
            color:int = self._read_bytes_as_int(pixel_byte, color_byte_size)
            parsed_color:tuple = self._parse_red_green_blue_alpha_8888_color(color)
            texture_info[TextureEnums.PIXELS].append(parsed_color)
        return texture_info

    def _read_intensity_alpha_44_texture(self,
            texture_start_address:int, texture_info:dict):
        '''
        PyDoc
        '''
        x_size:int = texture_info[TextureEnums.X_PIXEL_GRID]
        y_size:int = texture_info[TextureEnums.Y_PIXEL_GRID]
        texture_end_address:int = texture_start_address + (x_size * y_size)
        for pixel_byte in range(texture_start_address, texture_end_address):
            color:int = self._read_bytes_as_int(pixel_byte, 1)
            parsed_color:tuple = self._parse_intensity_alpha_44_color(color)
            texture_info[TextureEnums.PIXELS].append(parsed_color)
        return texture_info

    ########################
    ##### DISPLAY LIST #####
    ########################

    def _read_3d_model_display_list_header(self, index_start:int):
        '''
        PyDoc
        '''
        total_command_count:int = self._read_bytes_as_int(index_start, 4)
        # padding 4
        index_start += 0x08
        current_command_count:int = 0
        while(current_command_count < total_command_count):
            # Parse these commands at some point ¯\_(ツ)_/¯
            # https://hack64.net/wiki/doku.php?id=f3dex2
            display_list_command:int = self._read_bytes_as_int(index_start, 8)
            self._display_list[current_command_count] = display_list_command
            index_start += 8
            current_command_count += 1

    ####################
    ##### VERTICES #####
    ####################

    def _read_3d_model_vertices_header(self, index_start:int):
        '''
        PyDoc
        '''
        min_x_coordinate:int = self._read_bytes_as_int(index_start, 2, True)
        min_y_coordinate:int = self._read_bytes_as_int(index_start + 0x02, 2, True)
        min_z_coordinate:int = self._read_bytes_as_int(index_start + 0x04, 2, True)
        max_x_coordinate:int = self._read_bytes_as_int(index_start + 0x06, 2, True)
        max_y_coordinate:int = self._read_bytes_as_int(index_start + 0x08, 2, True)
        max_z_coordinate:int = self._read_bytes_as_int(index_start + 0x0A, 2, True)
        center_x_coordinate:int = self._read_bytes_as_int(index_start + 0x0C, 2, True)
        center_y_coordinate:int = self._read_bytes_as_int(index_start + 0x0E, 2, True)
        center_z_coordinate:int = self._read_bytes_as_int(index_start + 0x10, 2, True)
        unk_12:int = self._read_bytes_as_int(index_start + 0x12, 2, True)
        unk_14:int = self._read_bytes_as_int(index_start + 0x14, 2, True)
        total_vertex_count:int = self._read_bytes_as_int(index_start + 0x16, 2, True) // 2
        current_vertex_count:int = 0
        index_start += 0x18
        while(current_vertex_count < total_vertex_count):
            vertex_info:dict = self._read_vertex_info(index_start)
            self._vertices[current_vertex_count] = vertex_info
            index_start += 0x10
            current_vertex_count += 1

    def _read_3d_model_vertex_info(self, index_start:int):
        '''
        PyDoc
        '''
        x_position:int = self._read_bytes_as_int(index_start, 2, True)
        y_position:int = self._read_bytes_as_int(index_start + 0x02, 2, True)
        z_position:int = self._read_bytes_as_int(index_start + 0x04, 2, True)
        # Padding 2
        u_position:int = self._read_bytes_as_int(index_start + 0x08, 2, True)
        v_position:int = self._read_bytes_as_int(index_start + 0x0A, 2, True)
        red:int = self._read_bytes_as_int(index_start + 0x0C, 1)
        green:int = self._read_bytes_as_int(index_start + 0x0D, 1)
        blue:int = self._read_bytes_as_int(index_start + 0x0E, 1)
        alpha:int = self._read_bytes_as_int(index_start + 0x0F, 1)
        vertex_info:dict = {
            VertexEnums.X_POSITION: x_position,
            VertexEnums.Y_POSITION: y_position,
            VertexEnums.Z_POSITION: z_position,
            VertexEnums.U_POSITION: u_position,
            VertexEnums.V_POSITION: v_position,
            VertexEnums.RED: red,
            VertexEnums.GREEN: green,
            VertexEnums.BLUE: blue,
            VertexEnums.ALPHA: alpha,
        }
        return vertex_info

    ######################
    ##### ANIMATIONS #####
    ######################

    def _read_3d_model_animations_header(self):
        '''
        PyDoc
        '''
        pass

    ######################
    ##### COLLISIONS #####
    ######################

    def _read_3d_model_collisions_header(self):
        '''
        PyDoc
        '''
        pass
    
    ##################
    ##### UNK 20 #####
    ##################

    def _read_3d_model_unk_20(self):
        '''
        PyDoc
        '''
        pass

    ###################
    ##### EFFECTS #####
    ###################

    def _read_3d_model_effects_header(self):
        '''
        PyDoc
        '''
        pass

    ###############################
    ##### VERTEX-BONE MAPPING #####
    ###############################

    def _read_3d_model_vertex_bone_mapping_header(self):
        '''
        PyDoc
        '''
        pass

    ##############################
    ##### TEXTURE ANIMATIONS #####
    ##############################

    def _read_3d_model_texture_animations_header(self):
        '''
        PyDoc
        '''
        pass

    ##################
    ##### UNK 34 #####
    ##################

    def _read_3d_model_unk_34(self):
        '''
        PyDoc
        '''
        pass

    ##########################
    ##### VERTEX NORMALS #####
    ##########################

    def _read_3d_model_vertex_normals_header(self):
        '''
        PyDoc
        '''
        pass

    ################
    ##### MAIN #####
    ################

    def _developer_debugging(self, model_offsets:dict):
        '''
        PyDoc
        '''
        # for item in model_offsets:
        #     if(model_offsets[item] == 0x0):
        #         return
        # print("IT HAS EVERYTHING!")
        if(model_offsets[ThreeDimensionalModelEnums.ANIMATIONS] == 0x0):
            return
        print("HERE!")
        exit(0)

    def _read_3d_model_file(self):
        '''
        PyDoc
        '''
        with open(self._file_path, "rb+") as bin_file:
            self._file_content:bytearray = bytearray(bin_file.read())
        self._validate_model_file()
        model_offsets:dict = self._read_3d_model_header()
        # self._developer_debugging(model_offsets)
        # self._read_3d_model_geometry_layout_header()
        self._read_3d_model_texture_header(model_offsets[ThreeDimensionalModelEnums.TEXTURES])
        # self._read_3d_model_display_list_header()
        # self._read_3d_model_vertices_header()
        # self._read_3d_model_animations_header()
        # self._read_3d_model_collisions_header()
        # self._read_3d_model_unk_20()
        # self._read_3d_model_effects_header()
        # self._read_3d_model_vertex_bone_mapping_header()
        # self._read_3d_model_texture_animations_header()
        # self._read_3d_model_unk_34()
        # self._read_3d_model_vertex_normals_header()