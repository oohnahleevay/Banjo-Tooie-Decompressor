###################
##### IMPORTS #####
###################

import os
import sys

main_folder = os.path.dirname(os.path.abspath("..."))
sys.path.append(main_folder)

import json
from enum import IntEnum, StrEnum, auto, unique

from asset_editing.model.model_asset_ids import \
    ModelAssetId
from asset_editing.generic_file import Generic_Bin_File_Class
from asset_editing.model.two_dimensional_model import \
    TwoDimensionalModel
from asset_editing.model.three_dimensional_model import \
    ThreeDimensionalModel
# 2d Model Class

###########################
##### LOCAL CONSTANTS #####
###########################

MODEL_EXT:str = ".bin"

TEST_OUTPUT_DIR:str = 'test_output/'
DECOMPRESSED_DIR:str = f'{TEST_OUTPUT_DIR}decompressed/'
MODEL_LOGGING_DIR:str = "asset_editing/model/model_logging/"

class ModelType(IntEnum):
    TWO_DIMENSIONAL = auto()
    THREE_DIMENSIONAL = auto()

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

class Model(ThreeDimensionalModel, TwoDimensionalModel, Generic_Bin_File_Class):
    def __init__(self, file_dir:str, asset_id:int):
        '''
        PyDoc
        '''
        self._file_dir:str = file_dir
        self._asset_id:int = asset_id
        self._file_type:ModelType = None
        file_path:str = self.create_asset_file_path(file_dir, asset_id, MODEL_EXT)
        Generic_Bin_File_Class.__init__(self, file_path)
    
    def _init_model_as_two_dimensional(self):
        '''
        PyDoc
        '''
        self._model_header_info:dict = {}
        self._frames:dict = {}
        self._vertices:list = []
        self._display_list:list = []

    def _init_model_as_three_dimensional(self):
        '''
        PyDoc
        '''
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
        self._unk_38:dict = {}
        self._vertex_normals:dict = {}
        self._tri_count:int = None
        self._vert_count:int = None

    def _determine_file_type(self):
        '''
        PyDoc
        '''
        first_four_bytes:int = self._read_bytes_as_int(0x0, 4)
        if(first_four_bytes == 0x0000000B):
            self._file_type = ModelType.THREE_DIMENSIONAL
        else:
            # No File Header Indicator
            self._file_type = ModelType.TWO_DIMENSIONAL

    ################
    ##### MAIN #####
    ################

    def _read_file(self):
        '''
        Reads a file as a byte array.
        '''
        with open(self._file_path, "rb+") as bin_file:
            self._file_content:bytearray = bytearray(bin_file.read())
        self._determine_file_type()
        if(self._file_type == ModelType.TWO_DIMENSIONAL):
            self._init_model_as_two_dimensional()
            TwoDimensionalModel._read_file(self)
        elif(self._file_type == ModelType.THREE_DIMENSIONAL):
            self._init_model_as_three_dimensional()
            ThreeDimensionalModel._read_file(self)
        else:
            print("ERROR: Model File is neither 2D nor 3D.")
            exit(1)

if __name__ == '__main__':
    errored_assets:list = []
    create_model_logging_dir()
    for asset_id in ModelAssetId:
        asset_id_name:str = asset_id.name
        asset_id_value:int = asset_id.value
        print(f"{hex(asset_id_value)} - {asset_id_name}")
        try:
            model_obj = Model(DECOMPRESSED_DIR, asset_id)
        except Exception as err:
            errored_assets.append((f"{hex(asset_id_value)} - {asset_id_name}", str(err)))
        # asset_id_str:str = model_obj._convert_int_to_str(asset_id.value, 4)
        # file_path:str = f"{MODEL_LOGGING_DIR}{asset_id_str}-{asset_id_name}.json"
        # model_obj.print_map_setup(file_path)
    print("ERRORED ASSETS:")
    for asset, err in errored_assets:
        print(f"\t{asset} - {err}")