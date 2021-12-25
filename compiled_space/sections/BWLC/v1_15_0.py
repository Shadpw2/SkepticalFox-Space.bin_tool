""" BWLC (Lights) """

from _base_json_section import *
from .v1_11_0 import BWLC_Section_1_11_0, PulseSpotLight_v1_11_0



class PulseLight_v1_15_0(CStructure):
    _size_ = 100

    _fields_ = [
        ('position',       c_float * 3  ),
        ('inner_radius',   c_float      ),
        ('outer_radius',   c_float      ),
        ('lod_shift',      c_float      ), # lodShift
        ('colour',         c_float * 4  ),
        ('unknown',        c_uint32     ),
        ('multiplier',     c_float      ),
        ('cast_shadows',   c_uint32, 1  ),
        ('pad',            c_uint32, 31 ),
        ('frame_start_id', c_uint32     ),
        ('frame_num',      c_uint32     ),
        ('unknown_2',      c_float      ), # c_float ?
        ('duration',       c_float      ),
        ('unknown_3',      c_uint32     ),
        ('unknown_4',      c_float      ),
        ('unknown_5',      c_uint32     ),
        ('unknown_6',      c_uint32     ),
        ('unknown_7',      c_uint32     ),
        ('unknown_8',      c_float      ),
        ('unknown_9',      c_float      ),
        ('unknown_10',     c_float      ),
        ]

    _tests_ = {
        # TODO ...
        }


class BWLC_Section_1_15_0(Base_JSON_Section):
    header = 'BWLC'
    int1 = 3

    _fields_ = [
        (list, 'pulse_light_list',      PulseLight_v1_15_0     ),
        (list, 'pulse_spot_light_list', PulseSpotLight_v1_11_0 ),
        (list, 'frames',                '<2f'                 ),
        ]

    def to_xml(self, chunks):
        # TODO (untested):
        BWLC_Section_1_11_0.to_xml(self, chunks)

    @classmethod
    def _omniLight_to_xml(cls, chunk, item):
        # TODO (untested):
        BWLC_Section_1_11_0._omniLight_to_xml(chunk, item)

    @classmethod
    def _pulseLight_to_xml(cls, chunk, item, frames):
        # TODO (untested):
        BWLC_Section_1_11_0._pulseLight_to_xml(chunk, item, frames)

    @classmethod
    def _spotLight_to_xml(cls, chunk, item):
        # TODO (untested):
        BWLC_Section_1_11_0._spotLight_to_xml(chunk, item)

    @classmethod
    def _pulseSpotLight_to_xml(cls, chunk, item, frames):
        # TODO (untested):
        BWLC_Section_1_11_0._pulseSpotLight_to_xml(chunk, item, frames)
