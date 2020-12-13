from pathlib import Path

from xml.etree import ElementTree as ET
from xml_utils.XmlUnpacker import XmlUnpacker
from xml_utils.XmlPacker import XmlPacker
from _base_section import *



__all__ = ('Base_XML_Section',)



def prettify(elem):
    from xml.dom import minidom
    reparsed = minidom.parseString(ET.tostring(elem))
    return reparsed.toprettyxml()



class Base_XML_Section(Base_Section):
    def from_bin_stream(self, stream, row):
        assert row.header == self.header, row.header
        self._data = XmlUnpacker().read(stream, row.position)
        assert stream.tell() == row.position + row.length, (stream.tell(), row.position + row.length)
        self._exist = True

    def unp_to_dir(self, unp_dir):
        unp_dir = Path(unp_dir)
        with open(unp_dir.joinpath(f'{self.header}.xml'), 'w') as fw:
            fw.write(prettify(self._data))

    def from_dir(self, unp_dir):
        unp_dir = Path(unp_dir)
        try:
            self._data = ET.parse(unp_dir.joinpath(f'{self.header}.xml')).getroot()
            self._exist = True
        except:
            self._exist = False

    def to_bin(self):
        return XmlPacker().pack(self._data)
