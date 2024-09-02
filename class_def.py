

class Animation:
    def __init__(self, start, end, elementCount):
        self.start_frame = start
        self.end_frame = end
        self.elementCount = elementCount
        self.elements = []

class Element:
    def __init__(self, bone_id, transform_type, dataCount):
        self.bone_id = bone_id
        self.transformation_type = transform_type
        self.dataCount = dataCount
        self.data = []


class Data:
    def __init__(self, unk, frame, factor):
        self.unk = unk
        self.frame = frame
        self.transform_factor = factor
