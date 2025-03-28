###################
##### IMPORTS #####
###################

import os

#####################
##### CONSTANTS #####
#####################

TEST_OUTPUT_DIR:str = 'test_output/'
DECOMPRESSED_DIR:str = f'{TEST_OUTPUT_DIR}decompressed/'
TEXT_DIR:str = f'{DECOMPRESSED_DIR}text/'

TEXT_FILE_HEADER:int = 0x010300

CHARACTER_HEADS:dict = {
    13: 'Clean Skivvy',
    14: 'Dirty Skivvy',
    21: 'Unga Bunga',
    22: 'Jiggywiggy',
    23: 'Jiggywiggy Disciple',
    24: 'Zubba',
    25: 'Jiggywiggy',
    26: 'Honey B.',
    29: 'Angel Bottles',
    31: 'Pool Pig',
    33: 'Oogle Boogle',
    34: 'Speaker',
    35: 'Dingpot',
    36: 'Zombie Jingaling',
    37: 'Rocknuts',
    38: 'Mildred',
    39: 'Biggafoot',
    40: 'George',
    41: 'Sabreman',
    42: 'Klungo',
    43: 'Dippy',
    44: 'Loggo',
    45: 'Jingaling',
    46: 'Mrs. Bottles',
    47: 'Bottles Child #1',
    48: 'Bottles Child #2',
    49: 'Targitzan',
    50: 'Chompa',
    51: 'Woo Fak Fak',
    52: 'Weldar',
    54: 'Alien Child #1',
    58: 'Devil Bottles',
    69: 'Alien Child #2',
    70: 'Alien Child #3',
    71: 'Scrat',
    72: 'Scrit Small',
    73: 'Scrit Big',
    74: 'Heggy',
    128: 'Banjo',
    129: 'Kazooie',
    131: 'Bottles',
    132: 'Mumbo',
    150: 'Grunty',
    156: 'Jamjars',
    158: 'Bovina',
    164: 'Unogopaz',
    165: 'Bloatazin',
    166: 'Dilberta',
    167: 'Stony - Kickball Entry',
    168: 'Stony - Coach',
    169: 'Stony - Outdoor',
    170: 'Canary Mary',
    171: 'Cheato',
    172: 'Gobi',
    173: 'Scrut',
    174: 'Mr. Patch',
    175: 'Moggy',
    176: 'Soggy',
    177: 'Groggy',
    178: 'Mrs. Boggy',
    179: 'Bullion Bill',
    180: 'Humba',
    181: 'Saucer of Peril',
    182: 'Old King Coal',
    183: 'Madame Grunty',
    186: 'Ssslumber',
    187: 'Boggy',
    193: 'Grunty',
    196: 'Big Al',
    197: 'Salty Joe',
    198: 'Conga',
    199: 'Pawno',
    200: 'Tiptup',
    201: 'Jolly',
    202: 'Maggie',
    203: 'Terry',
    204: 'Stegosaurus',
    209: 'Jinjo?',
    212: 'Stony Kickballer',
    214: 'Alien',
    215: 'Chris P. Bacon',
    217: 'Scrotty',
    219: 'Roysten',
    221: 'Superstash',
    222: 'Guffo',
    223: 'Mr. Fit',
    226: 'Captain Blackeye',
    227: 'Jamjars',
    233: 'Chilly Willy',
    234: 'Chili Billi',
    235: 'Mingy Jongo',
    236: 'Dodgems Enemy',
    237: 'Mumbo',
    238: 'Banjo',
    239: 'Kazooie',
    240: 'Bottles',
    241: 'Mingella',
    242: 'Blobbelda',
    243: 'Klungo',
    244: 'Grunty',
}

SPECIAL_CHARACTERS:dict = {
    2: '<Open Yes/No Prompt>',
    3: '<Unknown 3>',
    4: '<Wait Button Press>',
    5: '<Close Dialogue>',
    7: '<Switch To Upper/Lower Text>',
    8: '<Unknown 8>',
    9: '<Switch Camera>',
    11: '<Unknown 11>'
}

FORMATTING_DICT:dict = {
    b'\x00': '\n',
    b'\x7e': '<var>',
    b'\x80': '<R>',
    b'\x81': '<Z>',
    b'\x82': '<RIGHT_C>',
    b'\x83': '<UP_C>',
    b'\x84': '<DOWN_C>',
    b'\x85': '<LEFT_C>',
    b'\x86': '<B>',
    b'\x87': '<A>',
}

#####################
##### FUNCTIONS #####
#####################

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

def replace_formatting(text):
    text_out = ''
    for i, character in enumerate(text):
        if character in FORMATTING_DICT:
            new_char = FORMATTING_DICT[character]
        else:
            new_char = text[i].decode('utf8')
        text_out = text_out + new_char
    return text_out

def dump_text_file(index):
    try:
        index_hex_str:str = convert_int_to_str(index, 4)
        with open(f"{DECOMPRESSED_DIR}{index_hex_str}.bin", "rb") as text_bin:
            with open(f"{TEXT_DIR}{index_hex_str}.txt", 'w') as text_file:
                text_header = int.from_bytes(text_bin.read(3), "big")
                if text_header != 0x010300:
                    text_file.close()
                    os.remove(f"{TEXT_DIR}{index_hex_str}.txt")
                    return
                upper_dialog_count = int.from_bytes(text_bin.read(1), "big")
                text_out = '{}\n{}\n'.format(hex(text_header), upper_dialog_count)
                for dialog in range(upper_dialog_count):
                    character_head = int.from_bytes(text_bin.read(1), "big")
                    if character_head <= 0x11:
                        try:
                            character_head = SPECIAL_CHARACTERS[character_head]
                        except KeyError:
                            character_head = character_head
                        special_character = "Special Character: {}".format(character_head)
                        if character_head == '<Unknown 3>':
                            special_character = special_character + '\nCharacter Head: {}'.format(CHARACTER_HEADS[int.from_bytes(text_bin.read(1), 'big')])
                    else:
                        try:
                            character_head = CHARACTER_HEADS[character_head]
                        except KeyError:
                            character_head = character_head
                        special_character = "Character Head: {}".format(character_head)
                    string_length = int.from_bytes(text_bin.read(1), "big")
                    text_buffer = []
                    for i in range(string_length):
                        text_buffer.append(text_bin.read(1))
                    formatted_text = replace_formatting(text_buffer)
                    text_out = text_out + special_character + '\n\t' + formatted_text
                lower_dialog_count = int.from_bytes(text_bin.read(1), "big")
                text_out = text_out + "\n\n{}\n".format(lower_dialog_count)
                if lower_dialog_count != 0 or lower_dialog_count is not None:
                    for dialog in range(lower_dialog_count):
                        character_head = int.from_bytes(text_bin.read(1), "big")
                        if character_head <= 0x11:
                            try:
                                character_head = SPECIAL_CHARACTERS[character_head]
                            except KeyError:
                                character_head = character_head
                            special_character = "Special Character: {}".format(character_head)
                            if character_head == '<Unknown 3>':
                                character_head = int.from_bytes(text_bin.read(1), 'big')
                                try:
                                    character_head = CHARACTER_HEADS[character_head]
                                except KeyError:
                                    try:
                                        character_head = SPECIAL_CHARACTERS[character_head]
                                    except KeyError:
                                        character_head = character_head
                                special_character = special_character + '\nCharacter Head: {}'.format(character_head)
                        else:
                            try:
                                character_head = CHARACTER_HEADS[character_head]
                            except KeyError:
                                character_head = character_head
                            special_character = "Character Head: {}".format(character_head)
                        string_length = int.from_bytes(text_bin.read(1), "big")
                        text_buffer = []
                        for i in range(string_length):
                            text_buffer.append(text_bin.read(1))
                        formatted_text = replace_formatting(text_buffer)
                        text_out = text_out + special_character + '\n\t' + formatted_text
                text_file.write(text_out)
    except UnicodeEncodeError:
        os.remove(f"{TEXT_DIR}{index_hex_str}.txt")
        return