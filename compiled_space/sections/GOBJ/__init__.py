""" GOBJ (?) """

from _base_json_section import *



__all__ = ('GOBJ_Section_1_12_1',)



class GOBJ_Section_1_12_1(Base_JSON_Section):
	header = 'GOBJ'
	int1 = 2

	@row_seek(True)
	def from_bin_stream(self, stream, row):
		''' FIXME! '''
		self._data = {}
		self.read_vector(stream, '1', '<6I16f')
		self.read_vector(stream, '2', '<20I')
		rest_len = row.position + row.length - stream.tell()
		self._data['3'] = stream.read(rest_len).hex()

	def to_bin(self):
		''' FIXME! '''
		res = b''
		res += self.write_vector('1', '<6I16f')
		res += self.write_vector('2', '<20I')
		res += bytes.fromhex(self._data['3'])
		return res