import math

def n64_cic_nus_6105(challenge, length):
    lut0 = [0x4, 0x7, 0xA, 0x7, 0xE, 0x5, 0xE, 0x1,
            0xC, 0xF, 0x8, 0xF, 0x6, 0x3, 0x6, 0x9]

    lut1 = [0x4, 0x1, 0xA, 0x7, 0xE, 0x5, 0xE, 0x1,
            0xC, 0x9, 0x8, 0x5, 0x6, 0x3, 0xC, 0x9]
    response = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    key = 0xB
    lut = lut0
    for i in range(0, length):
        response[i] = (key + 5 * challenge[i]) & 0xF
        key = lut[response[i]]

        if response[i] in (0x0, 0x2, 0x3, 0x5, 0x6, 0x8) or \
          (response[i] in (0xB, 0xE) and lut == lut0) or \
          (response[i] in (0x1, 0x9) and lut == lut1):
            lut = lut1
        else:
            lut = lut0

    return response


def decryptMapSetup(index, encryptedBytes, size):
    decryptedBytes = []
    inputKey = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    cicValue = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    inputKeyNibbles = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    key = index - 0x955

    for i in range(0, 0xE, 2):
        key_entry = (key >> i) | (key << (0x10 - i))

        inputKey[i] = key_entry & 0xFF
        inputKey[i+1] = (key_entry & 0xFF00) & 0xFF

    inputKey[0xE] = 0x0
    inputKey[0xF] = 0x2

    for x in range(0,0x20):
        if x % 2 == 0:
            inputKeyNibbles[x] = (inputKey[math.floor(x/2)] >> 4) & 0xF
        else:
            inputKeyNibbles[x] = inputKey[math.floor(x/2)] & 0xF
        #print(math.floor(x/2), hex(inputKey[math.floor(x/2)]), hex(inputKeyNibbles[x]))

    rsp = n64_cic_nus_6105(inputKeyNibbles, 0x1E)
    rsp[0x1E] = rsp[0x1F] = 0

    for x in range(0, 0x20, 2):
        cicValue[math.floor(x/2)] = (rsp[(x)] << 4) | rsp[(x+1)]
        #print(x, bin(cicValue[math.floor(x/2)]), bin(rsp[x] << 4), bin(rsp[x+1]))

    for i in range(size):
        decryptedBytes.append(encryptedBytes[i] ^ cicValue[i % 0xE])

=======
import math

def n64_cic_nus_6105(challenge, length):
    lut0 = [0x4, 0x7, 0xA, 0x7, 0xE, 0x5, 0xE, 0x1,
            0xC, 0xF, 0x8, 0xF, 0x6, 0x3, 0x6, 0x9]

    lut1 = [0x4, 0x1, 0xA, 0x7, 0xE, 0x5, 0xE, 0x1,
            0xC, 0x9, 0x8, 0x5, 0x6, 0x3, 0xC, 0x9]
    response = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    key = 0xB
    lut = lut0
    for i in range(0, length):
        response[i] = (key + 5 * challenge[i]) & 0xF
        key = lut[response[i]]

        if response[i] in (0x0, 0x2, 0x3, 0x5, 0x6, 0x8) or \
          (response[i] in (0xB, 0xE) and lut == lut0) or \
          (response[i] in (0x1, 0x9) and lut == lut1):
            lut = lut1
        else:
            lut = lut0

    return response


def decryptMapSetup(index, encryptedBytes, size):
    decryptedBytes = []
    inputKey = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    cicValue = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    inputKeyNibbles = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    key = index - 0x955

    for i in range(0, 0xE, 2):
        key_entry = (key >> i) | (key << (0x10 - i))

        inputKey[i] = key_entry & 0xFF
        inputKey[i+1] = (key_entry & 0xFF00) & 0xFF

    inputKey[0xE] = 0x0
    inputKey[0xF] = 0x2

    for x in range(0,0x20):
        if x % 2 == 0:
            inputKeyNibbles[x] = (inputKey[math.floor(x/2)] >> 4) & 0xF
        else:
            inputKeyNibbles[x] = inputKey[math.floor(x/2)] & 0xF
        #print(math.floor(x/2), hex(inputKey[math.floor(x/2)]), hex(inputKeyNibbles[x]))

    rsp = n64_cic_nus_6105(inputKeyNibbles, 0x1E)
    rsp[0x1E] = rsp[0x1F] = 0

    for x in range(0, 0x20, 2):
        cicValue[math.floor(x/2)] = (rsp[(x)] << 4) | rsp[(x+1)]
        #print(x, bin(cicValue[math.floor(x/2)]), bin(rsp[x] << 4), bin(rsp[x+1]))

    for i in range(size):
        decryptedBytes.append(encryptedBytes[i] ^ cicValue[i % 0xE])

    return bytes(decryptedBytes)