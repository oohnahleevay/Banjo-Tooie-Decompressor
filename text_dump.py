import os

character_heads = {
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

special_characters = {
    2: '<Open Yes/No Prompt>',
    3: '<Unknown 3>',
    4: '<Wait Button Press>',
    5: '<Close Dialogue>',
    7: '<Switch To Upper/Lower Text>',
    8: '<Unknown 8>',
    9: '<Switch Camera>',
    11: '<Unknown 11>'
}

def replaceFormatting(text):
    old_char = 'oops'
    new_char = 'oops'
    for character in text:
        if character == 0:
            old_char = '\x00'
            new_char = '\n'
        elif character == 0x7e:
            old_char = '~'
            new_char = '<var>'
        elif character == 0x81:
            old_char = '\x81'
            new_char = '<Z>'

        text = str(text).replace(old_char, new_char)
    return text

def dumpTextFile(index):
    try:
        with open("test_output/decompressed/{}.bin".format(hex(index)[2:]), "rb") as text_bin:
            with open('test_output/decompressed/text/{}.txt'.format(hex(index)[2:]), 'w') as text_file:
                text_header = int.from_bytes(text_bin.read(3), "big")
                if text_header != 0x010300:
                    text_file.close()
                    os.remove('test_output/decompressed/text/{}.txt'.format(hex(index)[2:]))
                    return
                upper_dialog_count = int.from_bytes(text_bin.read(1), "big")
                text_out = '{}\n{}\n'.format(hex(text_header), upper_dialog_count)
                for dialog in range(upper_dialog_count):
                    character_head = int.from_bytes(text_bin.read(1), "big")
                    if character_head <= 0x11:
                        try:
                            character_head = special_characters[character_head]
                        except KeyError:
                            character_head = character_head
                        special_character = "Special Character: {}".format(character_head)
                        if character_head == '<Unknown 3>':
                            special_character = special_character + '\nCharacter Head: {}'.format(character_heads[int.from_bytes(text_bin.read(1), 'big')])
                    else:
                        try:
                            character_head = character_heads[character_head]
                        except KeyError:
                            character_head = character_head
                        special_character = "Character Head: {}".format(character_head)
                    string_length = int.from_bytes(text_bin.read(1), "big")
                    raw_text_bytes = text_bin.read(string_length)
                    formatted_text_bytes = replaceFormatting(raw_text_bytes)
                    text_out = text_out + special_character + '\n\t' + formatted_text_bytes + '\n'
                lower_dialog_count = int.from_bytes(text_bin.read(1), "big")
                text_out = text_out + "\n\n{}\n".format(lower_dialog_count)
                if lower_dialog_count != 0 or lower_dialog_count is not None:
                    for dialog in range(lower_dialog_count):
                        character_head = int.from_bytes(text_bin.read(1), "big")
                        if character_head <= 0x11:
                            try:
                                character_head = special_characters[character_head]
                            except KeyError:
                                character_head = character_head
                            special_character = "Special Character: {}".format(character_head)
                            if character_head == '<Unknown 3>':
                                character_head = int.from_bytes(text_bin.read(1), 'big')
                                try:
                                    character_head = character_heads[character_head]
                                except KeyError:
                                    try:
                                        character_head = special_characters[character_head]
                                    except KeyError:
                                        character_head = character_head
                                special_character = special_character + '\nCharacter Head: {}'.format(character_head)
                        else:
                            try:
                                character_head = character_heads[character_head]
                            except KeyError:
                                character_head = character_head
                            special_character = "Character Head: {}".format(character_head)
                        string_length = int.from_bytes(text_bin.read(1), "big")
                        text_out = text_out + special_character + '\n\t' + str(text_bin.read(string_length)) + '\n'
                text_file.write(text_out)
    except UnicodeEncodeError:
        os.remove('test_output/decompressed/text/{}.txt'.format(hex(index)[2:]))
        return