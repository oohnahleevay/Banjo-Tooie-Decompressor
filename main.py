import struct
import zlib
from text_dump import *
from cic_decrypt import *

typeDefs = {
    0: "Model",
    1: 1,
    2: 2,
    3: "Text",
    4: "Blank",
    5: 5,
    6: "Animation",
    7: "Sprite",
    8: 8,
    9: "Music",
    0xA: "Map Setup",
    0xB: "B",
    0xC: "C",
    0xD: "D",
    0xE: "E",
    0xF: "F"
}
assets = []

transformation_type_index = {
        0: "X Rot",
        1: "Y Rot",
        2: "Z Rot",
        3: "X Scale",
        4: "Y Scale",
        5: "Z Scale",
        6: "X Trans",
        7: "Y Trans",
        8: "Z Trans",
        9: "Unk 0x9",
        0xA: "Unk 0xA",
        0xB: "Unk 0xB"
    }


def checkHeader(filename):
    with open(filename, "rb") as file:
        startFrame = int.from_bytes(file.read(2), "big")
        endFrame = int.from_bytes(file.read(2), "big")
        elementCount = int.from_bytes(file.read(2), "big")
        file.seek(2, 1)
        return startFrame, endFrame, elementCount


class Asset:
    def __init__(self, offset, compressed, type, index):
        self.address = 0x12B24 + offset
        self.compressed = compressed
        self.type = typeDefs[type]
        self.index = index


if not os.path.isdir('test_output'):
    os.mkdir('test_output')
    os.mkdir('test_output/compressed')
    os.mkdir('test_output/decompressed')
    os.mkdir('test_output/decompressed/assemblies')
    os.mkdir('test_output/decompressed/text')

with open("Banjo-Tooie (USA).z64", "rb") as file:
    n = 0
    file.seek(0x5180)
    entries = int.from_bytes(file.read(4), "big")
    file.seek(4,1)
    for entry in range(entries):
        asset = struct.unpack(">3sB", file.read(4))
        assets.append(Asset(int.from_bytes(asset[0], "big") * 4, (asset[1] >> 4) & 0xF, asset[1] & 0xF, n))
        n += 1

    for i, asset in enumerate(assets):
        if asset.type != "Blank":
            print(hex(asset.index), hex(asset.address), asset.type)
            size = assets[i+1].address - assets[i].address
            chopped_bytes = 2 if (asset.compressed and asset.type != 'Map Setup') else 0
            file.seek(asset.address + chopped_bytes)
            if asset.type != "Map Setup":
                compressed_bytes = file.read(size - chopped_bytes)
            else:
                compressed_bytes = decryptMapSetup(asset.index, file.read(size), size)
            with open("test_output/compressed/{}.bin".format(hex(asset.address)), "wb") as output_bin:
                output_bin.write(compressed_bytes)
            with open("test_output/decompressed/{}.bin".format(hex(asset.index)[2:]), "wb") as output_bin:
                try:
                    if not asset.compressed:
                        print("{} is uncompressed\n".format(hex(asset.address)))
                        output_bin.write(compressed_bytes)
                        continue
                    if asset.type == 'Map Setup':
                        compressed_bytes = compressed_bytes[2:]
                    decompressed_bytes = zlib.decompress(compressed_bytes, -15, 100)
                    print("decompressing {}\n".format(hex(asset.address)))
                    output_bin.write(decompressed_bytes)
                except zlib.error:
                    print("failed to decompress {}\n".format(hex(asset.address)))
                    output_bin.write(b'\x00')
                    continue

    file.seek(0x1E899B0, 0)
    first_offset = int.from_bytes(file.read(4), 'big')
    offsets = [first_offset,]
    prev_offset = first_offset
    while file.tell() != first_offset + 0x1E899B0:
        next_offset = int.from_bytes(file.read(4), 'big')
        if next_offset != prev_offset:
            offsets.append(next_offset)
            prev_offset = next_offset
    for i, offset in enumerate(offsets):
        if offset == first_offset or (offset != first_offset and offset != offsets[i - 1]):
            address = 0x1E899B0 + offset + 16
            print(hex(offset), hex(address))
            file.seek(address + 2, 0)
            try:
                size = offsets[i+1] - offsets[i]
            except IndexError:
                break
            compressed_bytes = file.read(size - 2)
            with open("test_output/compressed/{}.bin".format(hex(address)), "wb") as output_bin:
                output_bin.write(compressed_bytes)
            with open("test_output/decompressed/assemblies/{}_{}.bin".format(i, hex(address)[2:]), "wb") as output_bin:
                try:
                    decompressed_bytes = zlib.decompress(compressed_bytes, -15, 100)
                    print("decompressing #{}\n".format(i))
                    output_bin.write(decompressed_bytes)
                except zlib.error:
                    print("failed to decompress #{}\n".format(i))
                    output_bin.write(b'\x00')
                    continue

print("dumping text...")
for asset in assets:
    if asset.type == "Text":
        dumpTextFile(asset.index)

print("complete.")


# with open('test.bin', 'rb') as test:
#     test.seek(2)
#     decompressed_bytes = zlib.decompress(test.read(), -15)
#     with open('test_decompressed.bin', 'wb') as output_bin:
#         output_bin.write(decompressed_bytes)

# for anim_filename in os.listdir("testing_bins"):
#     startFrame, endFrame, elementCount = checkHeader("testing_bins/{}".format(anim_filename))
#     animation = Animation(startFrame, endFrame, elementCount)
#     string = "Start Frame: {}\nEnd Frame: {}\nElement Count: {}".format(startFrame, endFrame, elementCount)
#     with open("testing_bins/{}".format(anim_filename), "rb") as file:
#         file.seek(8)
#         for element in range(elementCount):
#             elementInfo = int.from_bytes(file.read(2), "big")
#             bone_id = (elementInfo & 0xFFF0) >> 4
#             transformation_type = transformation_type_index[elementInfo & 0xF]
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
#     startFrame, endFrame, elementCount = checkHeader("testing_bins/04572C.bin")
#     animation = Animation(startFrame, endFrame, elementCount)
#     file.seek(8)
#     for element in range(elementCount):
#         elementInfo = int.from_bytes(file.read(2), "big")
#         bone_id = (elementInfo & 0xFFF0) >> 4
#         transformation_type = transformation_type_index[elementInfo & 0xF]
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
