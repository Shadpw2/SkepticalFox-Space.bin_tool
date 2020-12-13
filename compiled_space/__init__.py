import json
import os
import sys

unpacker_version = '0.5.2'


sys.path.insert(0, os.path.dirname(__file__))

from versioning import get_sections
from space_assembler import space_assembly
from bwtb_section import BWTB_Section



class CompiledSpace:
    __bwtb = None
    __sections = None
    __wot_version = None

    @property
    def sections(self):
        return self.__sections

    def __init__(self, stream=None, wot_version=None):
        if stream is not None:
            if wot_version is not None:
                self.__wot_version = wot_version
            self.from_bin_stream(stream)

    def from_bin_stream(self, stream):
        self.__bwtb = BWTB_Section(stream)
        self.__sections = {}
        secs = get_sections(self.__wot_version)
        for sec_cls in secs:
            row = self.__bwtb.get_row_by_name(sec_cls.header)
            if row is None:
                print(f'Warning: {sec_cls.header} is None')
                continue
            self.__sections[sec_cls.header] = sec_cls(stream, row)

    def from_dir(self, unp_dir):
        with open(os.path.join(unp_dir, 'info.json'), 'r') as fr:
            info = json.load(fr)
        assert info['unpacker_version'] == unpacker_version, (info['unpacker_version'], unpacker_version)
        self.__wot_version = info['wot_version']

        self.__sections = {}
        secs = get_sections(self.__wot_version)
        for sec_cls in secs:
            try:
                sec = sec_cls(unp_dir)
                if sec._exist:
                    self.__sections[sec_cls.header] = sec
            except:
                import traceback
                traceback.print_exc()
                print(sec_cls)

    def unp_to_dir(self, dir):
        out_dict = {
            'wot_version': self.__wot_version,
            'unpacker_version': unpacker_version
        }
        with open(os.path.join(dir, 'info.json'), 'w') as fw:
            json.dump(out_dict, fw, sort_keys=True, indent=4)
        for header, sec in self.__sections.items():
            sec.unp_to_dir(dir)

    def unp_for_world_editor(self, dir):
        from xml.etree import ElementTree as ET
        from xml.dom import minidom
        from xml_utils.XmlUnpacker import XmlUnpacker

        out_dir = os.path.join(dir, 'unpacked_for_world_editor')
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        settings_path = os.path.join(dir, 'space.settings')
        if os.path.exists(settings_path):
            with open(settings_path, 'rb') as f:
                settings = XmlUnpacker().read(f)
        else:
            settings = ET.Element('root')

        gchunk = ET.Element('root')

        bwt2 = self.__sections['BWT2']

        if not hasattr(bwt2, 'prepare_unp_xml'):
            return

        chunks = bwt2.prepare_unp_xml(gchunk, settings, dir, out_dir, self.__sections)

        for header, sec in self.__sections.items():
            if not hasattr(sec, 'to_xml'):
                continue
            sec.to_xml(chunks)

        bwt2.flush_unp_xml(chunks)

        with open(os.path.join(out_dir, 'global.chunk'), 'w') as f:
            reparsed = minidom.parseString(ET.tostring(gchunk))
            f.write(reparsed.toprettyxml())

        with open(os.path.join(out_dir, 'space.settings'), 'w') as f:
            reparsed = minidom.parseString(ET.tostring(settings))
            f.write(reparsed.toprettyxml())

    def save_to_bin(self, bin_path):
        space_assembly(bin_path, self.__sections, self.__wot_version, unpacker_version)
