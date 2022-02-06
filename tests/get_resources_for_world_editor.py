from pathlib import Path
from zipfile import ZipFile
from struct import unpack, calcsize
from functools import cache
import xml.etree.ElementTree as ET
import argparse
import sys
import os
sys.path.insert(0, str(Path(__file__).parent.parent))
from compiled_space import CompiledSpace


parser = argparse.ArgumentParser()
parser.add_argument('--wotpath', type=Path, required=True)
parser.add_argument('--wotver', type=str, required=True)
parser.add_argument('--mapname', type=str, required=True)
parser.add_argument('--unpackhd', action='store_true')
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()

# debug info
print('wotpath:', args.wotpath)
print('wotver:', args.wotver)
print('mapname:', args.mapname)
print('unpackhd:', args.unpackhd)
print('debug:', args.debug)


outdir = Path('./out')


packages = {}
filepath2pkg = {}
for pkg_path in (args.wotpath / 'res' / 'packages').glob('*.pkg'):
    if not args.unpackhd:
        if pkg_path.name.endswith(('_hd.pkg', '_hd-part1.pkg', '_hd-part2.pkg')):
            continue
    zfile = ZipFile(pkg_path, 'r')
    packages[pkg_path.name] = zfile
    for _file in zfile.infolist():
        filepath2pkg[_file.filename.lower()] = (zfile, _file.filename)


print('# unpack stage')
packages[f'{args.mapname}.pkg'].extractall(outdir)
if args.unpackhd:
    packages[f'{args.mapname}_hd.pkg'].extractall(outdir)


@cache
def attempt_to_unpack(string):
    if string.lower() in filepath2pkg:
        zfile, fname = filepath2pkg[string.lower()]
        zfile.extract(fname, outdir)
    elif args.debug:
        print(f'-> FAILED: {string}')


def unpack_packed_xml(path):
    from xml.etree import ElementTree as ET
    from xml.dom import minidom
    from xml_utils.XmlUnpacker import XmlUnpacker
    with path.open('rb') as f:
        unpacked = XmlUnpacker().read(f)
    with path.open('w') as f:
        reparsed = minidom.parseString(ET.tostring(unpacked))
        f.write(reparsed.toprettyxml())


def unpack_blend_textures(fr):
    header = fr.read(4)
    assert header == b'bwb\x00', header
    section_count = unpack('<I', fr.read(4))[0]
    section_sizes = unpack(f'<4I', fr.read(4*4))
    for i in range(section_count):
        header = fr.read(4)
        assert header == b'bwt\x00', header
        version, xsize, ysize, always19, tex_cnt, padding = unpack('<IHHHHQ', fr.read(calcsize('<IHHHHQ')))
        assert version == 2
        assert always19 == 19
        assert padding == 0
        for j in range(tex_cnt):
            name_size = unpack('<I', fr.read(4))[0]
            name = fr.read(name_size).decode('utf-8')
            attempt_to_unpack(name)
            attempt_to_unpack(name[:-7] + '_NM.dds')
            attempt_to_unpack(name[:-7] + '_macro_AM.dds')
            attempt_to_unpack(name[:-7] + '_macro_NM.dds')
        fr.seek(xsize * ysize, os.SEEK_CUR)


def unpack_atlas(fr):
    fr.seek(-1, os.SEEK_END)
    eof = fr.tell()
    fr.seek(0, os.SEEK_SET)

    version, atlas_width, atlas_height, unused1 = unpack('<4I', fr.read(calcsize('<4I')))
    assert version == 1, version
    assert unused1 in [0, 1], unused1
    magic = fr.read(4)
    assert magic == b'BCVT', magic
    unused2, dds_chunk_size = unpack('<IQ', fr.read(calcsize('<IQ')))
    assert unused2 == 1, unused2
    fr.seek(dds_chunk_size, os.SEEK_CUR)
    while fr.tell() < eof:
        x0, x1, y0, y1 = unpack('<4I', fr.read(calcsize('<4I')))
        filepath = ''
        while True:
            c = fr.read(1)
            if c == b'\x00': break
            filepath += c.decode('utf-8')
        attempt_to_unpack(filepath)
        attempt_to_unpack(filepath[:-4] + '.dds')


for path in (outdir / 'spaces' / args.mapname).glob('*.cdata_processed'):
    with ZipFile(path) as cdata:
        with cdata.open('terrain2/blend_textures') as f:
            unpack_blend_textures(f)


spacebin = packages[f'{args.mapname}.pkg'].open(f'spaces/{args.mapname}/space.bin')
space = CompiledSpace(spacebin, args.wotver)
space.unp_for_world_editor(outdir / 'spaces' / args.mapname)


settings_tree = ET.parse((outdir / 'spaces' / args.mapname / 'unpacked_for_world_editor' / 'space.settings'))
for it in settings_tree.findall('.//tile'):
    attempt_to_unpack(it.text)


strings = space.sections['BWST']._data.values()
for string in strings:
    if string.endswith('.cdata_processed/terrain2'):
        continue
    if '.' not in string:
        continue
    if '/' not in string:
        continue
    if '.primitives/' in string:
        new_string = string.split('.primitives/')[0]
        attempt_to_unpack(f'{new_string}.primitives_processed')
        attempt_to_unpack(f'{new_string}.visual_processed')
        continue
    if string.endswith('.primitives'):
        new_string = string.split('.primitives')[0]
        attempt_to_unpack(f'{new_string}.primitives_processed')
        attempt_to_unpack(f'{new_string}.visual_processed')
        continue
    if string.endswith('.atlas'):
        new_string = string.split('.atlas')[0]
        attempt_to_unpack(f'{new_string}.atlas_processed')
        continue
    if string.endswith('.png'):
        new_string = string.split('.png')[0]
        attempt_to_unpack(string)
        attempt_to_unpack(f'{new_string}.dds')
        continue
    attempt_to_unpack(string)


print('# rename stage')
for path in outdir.rglob('*_processed'):
    path.replace(str(path)[:-10])


print('# unpack atlas stage')
for path in outdir.rglob('*.atlas'):
    unpack_atlas(path.open('rb'))


print('# unpack packed xml stage')
for path in outdir.rglob('*.visual'):
    unpack_packed_xml(path)

for path in outdir.rglob('*.model'):
    unpack_packed_xml(path)


print('# replace stage')
for path in (outdir / 'spaces' / args.mapname / 'unpacked_for_world_editor').glob('*'):
    path.replace(path.parent.parent / path.name)


print('# remove extra stage')
(outdir / 'spaces' / args.mapname / 'unpacked_for_world_editor').rmdir()
(outdir / 'spaces' / args.mapname / 'space.bin').unlink()
