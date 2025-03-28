###################
##### IMPORTS #####
###################

import os
import sys

main_folder = os.path.dirname(os.path.abspath("..."))
sys.path.append(main_folder)

import struct
import zlib
from typing import BinaryIO

from asset_editing.map_setup.map_setup_asset_ids import \
    MapSetupAssetId
from text_dump import dump_text_file
from cic_decrypt import decryptMapSetup

#####################
##### CONSTANTS #####
#####################

BANJO_TOOIE_ROM_FILE_NAME:str = "Banjo-Tooie (USA).z64"

TEST_OUTPUT_DIR:str = 'test_output/'
COMPRESSED_DIR:str = f'{TEST_OUTPUT_DIR}compressed/'
DECOMPRESSED_DIR:str = f'{TEST_OUTPUT_DIR}decompressed/'
ASSEMBLIES_DIR:str = f'{DECOMPRESSED_DIR}assemblies/'
TEXT_DIR:str = f'{DECOMPRESSED_DIR}text/'
BIN_EXT:str = ".bin"

MODEL:str = "Model"
TEXT:str = "Text"
BLANK:str = "Blank"
ANIMATION:str = "Animation"
SPRITE:str = "Sprite"
MUSIC:str = "Music"
MAP_SETUP:str = "Map Setup"

ASSET_TABLE_START_INDEX:int = 0x5180
ASSETS_START_ADDRESS:int = 0x12B24
ASSEMBLY_START_INDEX:int = 0x1E899B0

TYPE_DEFS:tuple = (
    MODEL, "UNK_1", "UNK_2",
    TEXT, BLANK, "UNK_5",
    ANIMATION, SPRITE, "UNK_8",
    MUSIC, MAP_SETUP, "UNK_B",
    "UNK_C", "UNK_D", "UNK_E",
    "UNK_F",
)

TRANSFORMATION_TYPE_INDEX:tuple = (
    "X Rotation", "Y Rotation", "Z Rotation",
    "X Scale", "Y Scale", "Z Scale",
    "X Trans", "Y Trans", "Z Trans",
    "Unk 0x9", "Unk 0xA", "Unk 0xB",
)

###########################
##### LOCAL VARIABLES #####
###########################

asset_list:list = []

###################
##### CLASSES #####
###################

class AssetClass:
    def __init__(self, offset:int, compressed:int, type:str, index:int):
        self.address:int = ASSETS_START_ADDRESS + offset
        self.compressed:int = compressed
        self.type:str = type
        self.index:int = index
        if(index < 0xA00 and index > 0x9F5):
            print(self.type)

#####################
##### FUNCTIONS #####
#####################

### SETUP

def create_directories():
    '''
    PyDoc
    '''
    if not os.path.isdir(TEST_OUTPUT_DIR):
        os.mkdir(TEST_OUTPUT_DIR)
    if not os.path.isdir(COMPRESSED_DIR):
        os.mkdir(COMPRESSED_DIR)
    if not os.path.isdir(DECOMPRESSED_DIR):
        os.mkdir(DECOMPRESSED_DIR)
    if not os.path.isdir(ASSEMBLIES_DIR):
        os.mkdir(ASSEMBLIES_DIR)
    if not os.path.isdir(TEXT_DIR):
        os.mkdir(TEXT_DIR)

### GENERIC FILES

def check_header(filename):
    '''
    PyDoc
    '''
    with open(filename, "rb") as file:
        startFrame = int.from_bytes(file.read(2), "big")
        endFrame = int.from_bytes(file.read(2), "big")
        elementCount = int.from_bytes(file.read(2), "big")
        file.seek(2, 1)
        return startFrame, endFrame, elementCount

def convert_int_to_str(int_val:int, leading_zero_count:int):
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

def write_compressed_file(file_path:str, file_name:str, compressed_bytes:bytes):
    '''
    PyDoc
    '''
    with open(f"{file_path}{file_name}{BIN_EXT}", "wb") as output_bin:
        output_bin.write(compressed_bytes)

### ASSETS

def obtain_asset_list(banjo_tooie_rom_file:BinaryIO):
    '''
    PyDoc
    '''
    banjo_tooie_rom_file.seek(ASSET_TABLE_START_INDEX)
    total_entry_count:int = int.from_bytes(banjo_tooie_rom_file.read(4), "big")
    banjo_tooie_rom_file.seek(4, 1)
    for index in range(total_entry_count):
        asset_info = struct.unpack(">3sB", banjo_tooie_rom_file.read(4))
        address:int = int.from_bytes(asset_info[0], "big") * 4
        compression_flag:int = (asset_info[1] >> 4) & 0xF
        asset_type:int = TYPE_DEFS[asset_info[1] & 0xF]
        asset_obj = AssetClass(address, compression_flag, asset_type, index)
        asset_list.append(asset_obj)

def write_decompressed_asset_file(asset_obj:AssetClass, compressed_bytes:bytes):
    '''
    PyDoc
    '''
    asset_index_hex_str:str = convert_int_to_str(asset_obj.index, 4)
    with open(f"{DECOMPRESSED_DIR}{asset_index_hex_str}{BIN_EXT}", "wb") as output_bin:
        try:
            if not asset_obj.compressed:
                print(f"INFO: Asset Index '{asset_index_hex_str}' Is Uncompressed")
                output_bin.write(compressed_bytes)
                return
            if asset_obj.type == MAP_SETUP:
                compressed_bytes = compressed_bytes[2:]
            decompressed_bytes = zlib.decompress(compressed_bytes, -15, 100)
            print(f"INFO: Decompressing Asset Index '{asset_index_hex_str}'")
            output_bin.write(decompressed_bytes)
        except zlib.error:
            print(f"ERROR: Failed To Decompress Asset Index '{asset_index_hex_str}'")
            output_bin.write(b'\x00')

def extract_asset_files(banjo_tooie_rom_file:BinaryIO):
    '''
    PyDoc
    '''
    for asset_count, asset_obj in enumerate(asset_list):
        if asset_obj.type == BLANK:
            continue
        print(f"DEBUG: INDEX {hex(asset_obj.index)} / ADDRESS {hex(asset_obj.address)} / TYPE {asset_obj.type}")
        size:int = asset_list[asset_count + 1].address - asset_list[asset_count].address
        chopped_bytes = 2 if (asset_obj.compressed and asset_obj.type != MAP_SETUP) else 0
        banjo_tooie_rom_file.seek(asset_obj.address + chopped_bytes)
        if asset_obj.type != MAP_SETUP:
            compressed_bytes:bytes = banjo_tooie_rom_file.read(size - chopped_bytes)
        else:
            compressed_bytes:bytes = decryptMapSetup(asset_obj.index, banjo_tooie_rom_file.read(size), size)
        asset_address_hex_str:str = convert_int_to_str(asset_obj.address, 7)
        write_compressed_file(COMPRESSED_DIR, asset_address_hex_str, compressed_bytes)
        write_decompressed_asset_file(asset_obj, compressed_bytes)

### ASSEMBLY

def obtain_assembly_offsets(banjo_tooie_rom_file:BinaryIO, first_offset:int):
    '''
    PyDoc
    '''
    assembly_offsets:list = [first_offset,]
    prev_offset:int = first_offset
    while banjo_tooie_rom_file.tell() != first_offset + ASSEMBLY_START_INDEX:
        next_offset = int.from_bytes(banjo_tooie_rom_file.read(4), 'big')
        if next_offset != prev_offset:
            assembly_offsets.append(next_offset)
            prev_offset = next_offset
    return assembly_offsets

def write_decompressed_assembly_file(offset_count:int, assembly_address_hex_str:str, compressed_bytes:bytes):
    '''
    PyDoc
    '''
    with open(f"{ASSEMBLIES_DIR}{offset_count}_{assembly_address_hex_str}{BIN_EXT}", "wb") as output_bin:
        try:
            decompressed_bytes = zlib.decompress(compressed_bytes, -15, 100)
            print(f"INFO: Decompressing #{offset_count}")
            output_bin.write(decompressed_bytes)
        except zlib.error:
            print(f"ERROR: Failed to decompress #{offset_count}")
            output_bin.write(b'\x00')

def extract_assembly_files(banjo_tooie_rom_file:BinaryIO):
    '''
    PyDoc
    '''
    banjo_tooie_rom_file.seek(ASSEMBLY_START_INDEX, 0)
    first_offset:int = int.from_bytes(banjo_tooie_rom_file.read(4), 'big')
    assembly_offsets:list = obtain_assembly_offsets(banjo_tooie_rom_file, first_offset)
    for offset_count, offset in enumerate(assembly_offsets):
        if offset == first_offset or (offset != first_offset and offset != assembly_offsets[offset_count - 1]):
            address = ASSEMBLY_START_INDEX + offset + 16
            print(f"DEBUG: OFFSET {hex(offset)} / ADDRESS: {hex(address)}")
            banjo_tooie_rom_file.seek(address + 2, 0)
            try:
                size = assembly_offsets[offset_count + 1] - assembly_offsets[offset_count]
            except IndexError:
                break
            compressed_bytes = banjo_tooie_rom_file.read(size - 2)
            assembly_address_hex_str:str = convert_int_to_str(address, 7)
            write_compressed_file(COMPRESSED_DIR, assembly_address_hex_str, compressed_bytes)
            write_decompressed_assembly_file(offset_count, assembly_address_hex_str, compressed_bytes)

### TEXT FILES

def dump_text_files():
    '''
    PyDoc
    '''
    print("INFO: Dumping text...")
    for asset in asset_list:
        if asset.type == TEXT:
            print(f"DEBUG: Dumping Asset Index {hex(asset.index)}")
            dump_text_file(asset.index)

################
##### MAIN #####
################

def extract_all_files():
    '''
    PyDoc
    '''
    print("INFO: Starting...")
    create_directories()
    with open(BANJO_TOOIE_ROM_FILE_NAME, "rb") as banjo_tooie_rom_file:
        obtain_asset_list(banjo_tooie_rom_file)
        extract_asset_files(banjo_tooie_rom_file)
        extract_assembly_files(banjo_tooie_rom_file)
    dump_text_files()
    print("INFO: Complete!")

if __name__ == '__main__':
    extract_all_files()


# with open('test.bin', 'rb') as test:
#     test.seek(2)
#     decompressed_bytes = zlib.decompress(test.read(), -15)
#     with open('test_decompressed.bin', 'wb') as output_bin:
#         output_bin.write(decompressed_bytes)

# for anim_filename in os.listdir("testing_bins"):
#     startFrame, endFrame, elementCount = check_header("testing_bins/{}".format(anim_filename))
#     animation = Animation(startFrame, endFrame, elementCount)
#     string = "Start Frame: {}\nEnd Frame: {}\nElement Count: {}".format(startFrame, endFrame, elementCount)
#     with open("testing_bins/{}".format(anim_filename), "rb") as file:
#         file.seek(8)
#         for element in range(elementCount):
#             elementInfo = int.from_bytes(file.read(2), "big")
#             bone_id = (elementInfo & 0xFFF0) >> 4
#             transformation_type = TRANSFORMATION_TYPE_INDEX[elementInfo & 0xF]
#             dataCount = int.from_bytes(file.read(2), "big")
#             string += "\n\nElement {} | Bone {} | Type: {} | Data Count {}".format(element, bone_id,
#                                                                                    transformation_type, dataCount)
#             animation.elements.append(Element(bone_id, transformation_type, dataCount))
#             for data in range(dataCount):
#                 elementData = int.from_bytes(file.read(2), "big")
#                 unknown = (elementData & 0xC000) >> 14
#                 frame = elementData & 0x3FFF
#                 transform_factor = int.from_bytes(file.read(2), "big", signed=True) / 64
#                 string += "\n\tData {} | Unk {} | Frame {} | Factor = {}".format(data, unknown, frame, transform_factor)
#                 animation.elements[element].data.append(Data(unknown, frame, transform_factor))
#
#     output = "output/{}.txt".format(anim_filename.removesuffix('.bin'))
#     with open(output, "w") as file:
#         file.write(string)
#         #print(output)

#################### Playground ################################################

# animation = None
#
# with open("testing_bins/04572C.bin", "rb") as file:
#     startFrame, endFrame, elementCount = check_header("testing_bins/04572C.bin")
#     animation = Animation(startFrame, endFrame, elementCount)
#     file.seek(8)
#     for element in range(elementCount):
#         elementInfo = int.from_bytes(file.read(2), "big")
#         bone_id = (elementInfo & 0xFFF0) >> 4
#         transformation_type = TRANSFORMATION_TYPE_INDEX[elementInfo & 0xF]
#         dataCount = int.from_bytes(file.read(2), "big")
#
#         animation.elements.append(Element(bone_id, transformation_type, dataCount))
#         for data in range(dataCount):
#             elementData = int.from_bytes(file.read(2), "big")
#             unknown = (elementData & 0xC000) >> 14
#             frame = elementData & 0x3FFF
#             transform_factor = int.from_bytes(file.read(2), "big", signed=True) / 64
#             animation.elements[element].data.append(Data(unknown, frame, transform_factor))
#
#
# with open("Path.csv", "w+") as path:
#     path.write("Frame, X, Y, Z")
#     x = 0
#     y = 0
#     z = 0
#     for frame in range(animation.end_frame + 1):
#
#         for data in animation.elements[3].data:
#             if data.frame == frame:
#                 x_trans = data.transform_factor
#         for data in animation.elements[4].data:
#             if data.frame == frame:
#                 y_trans = data.transform_factor
#         for data in animation.elements[5].data:
#             if data.frame == frame:
#                 z_trans = data.transform_factor
#         x += x_trans
#         y += y_trans
#         z += z_trans
#         path.write("\n{}, {}, {}, {}".format(frame, x, y, z))
