###################
##### IMPORTS #####
###################

import os
import sys

main_folder = os.path.dirname(os.path.abspath("..."))
sys.path.append(main_folder)

import json
from enum import StrEnum, auto

from asset_editing.generic_file import Generic_Bin_File_Class
from asset_editing.speech_bubble.speech_bubble_asset_ids import \
    SpeechBubbleAssetId

###########################
##### LOCAL CONSTANTS #####
###########################

LEVEL_SETUP_EXT:str = ".bin"

TEST_OUTPUT_DIR:str = 'test_output/'
DECOMPRESSED_DIR:str = f'{TEST_OUTPUT_DIR}decompressed/'
SPEECH_BUBBLE_LOGGING_DIR:str = "asset_editing/speech_bubble/speech_bubble_logging/"

###########################
##### SETUP FUNCTIONS #####
###########################

def create_speech_bubble_logging_dir():
    '''
    PyDoc
    '''
    if not os.path.exists(SPEECH_BUBBLE_LOGGING_DIR):
        os.makedirs(SPEECH_BUBBLE_LOGGING_DIR)
        print(f"The directory '{SPEECH_BUBBLE_LOGGING_DIR}' has been created.")
    else:
        print(f"The directory '{SPEECH_BUBBLE_LOGGING_DIR}' already exists.")

#########################
##### SPEECH BUBBLE #####
#########################