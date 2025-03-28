from enum import IntEnum, auto, unique

@unique
class SpeechBubbleAssetId(IntEnum):

    @classmethod
    def name_for_value(cls, value):
        if value in cls._value2member_map_:
            return cls(value).name
        return None
    
    C72 = 0x0C72
    C73 = auto()
    C74 = auto()