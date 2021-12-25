""" GOBJ (?) """

from _base_binary_section import *



__all__ = ('GOBJ_Section_1_12_1',)



class GOBJ_Section_1_12_1(Base_Binary_Section):
	header = 'GOBJ'
	int1 = 2

	def from_bin_stream(self, stream, row):
		stream.seek(row.position)
		self._data = stream.read(row.length)
		self._exist = True

	def to_bin(self):
		return self._data
