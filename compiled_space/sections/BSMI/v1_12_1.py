﻿""" BSMI (Model Instances) """

from _base_json_section import *
from .v1_0_0 import ChunkModel_v1_0_0
from .v1_5_0 import BSMI_Section_1_5_0


class ModelAnimation_v1_12_1(CStructure):
    _size_ = 36

    _fields_ = [
        ('model_index',   c_uint32     ),
        ('seq_res_fnv',   c_uint32     ),
        ('clip_name_fnv', c_uint32     ), # sequence/clipName
        ('auto_start',    c_uint32, 1  ), # sequence/autoStart
        ('loop',          c_uint32, 1  ), # sequence/loop
        ('pad1',          c_uint32, 14 ),
        ('unknown_1',     c_uint32, 1  ),
        ('unknown_2',     c_uint32, 1  ),
        ('pad2',          c_uint32, 14 ),
        ('loop_count',    c_int32      ), # sequence/loopCount
        ('speed',         c_float      ), # sequence/speed
        ('delay',         c_float      ), # sequence/delay
        ('unknown_3',     c_float      ),
        ('unknown_4',     c_float      ),
        ]

    _tests_ = {
        'clip_name_fnv': {'==': 2216829733},
        'pad1': {'==': 0},
        'pad2': {'==': 0}
    }


class BSMI_Section_1_12_1(Base_JSON_Section):
    header = 'BSMI'
    int1 = 3

    _fields_ = [
        (list, 'transforms',       '<16f'                ),
        (list, 'chunk_models',     ChunkModel_v1_0_0     ),
        (list, 'visibility_masks', '<I'                  ),
        (list, 'bsmo_models_id',   '<2I'                 ),
        (list, 'animations_id',    '<i'                  ),
        (list, 'model_animation',  ModelAnimation_v1_12_1),
        (list, '8_40',             '<10I'                ),
        (list, '9_4',              '<I'                  ),
        (list, '10_12',            '<3I'                 ), # 0.9.12: WSMI['1_12']
        (list, '11_4',             '<I'                  ),
        (list, '12_20',            '<5f'                 ),
        ]

    def to_xml(self, chunks):
        BSMI_Section_1_5_0.to_xml(self, chunks)
