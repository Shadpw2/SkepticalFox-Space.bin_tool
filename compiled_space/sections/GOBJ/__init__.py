""" GOBJ (?) """

from _base_json_section import *



__all__ = ('GOBJ_Section_1_12_1',)



class GOBJ_Section_1_12_1(Base_JSON_Section):
	header = 'GOBJ'
	int1 = 2

	_fields_ = [
		(list, '1', '<22I' ),
		(list, '2', '<20I' ),
		]
