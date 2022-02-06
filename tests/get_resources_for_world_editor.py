from pathlib import Path
from zipfile import ZipFile
from struct import unpack, calcsize
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

args = parser.parse_args()

# debug info
print('wotpath:', args.wotpath)
print('wotver:', args.wotver)
print('mapname:', args.mapname)


outdir = Path('./out')


packages = {}
for pkg_path in (args.wotpath / 'res' / 'packages').glob('*.pkg'):
    packages[pkg_path.name] = ZipFile(pkg_path, 'r')


print('# unpack stage')
packages[f'{args.mapname}.pkg'].extractall(outdir)


def attempt_to_unpack(string):
    for pkg in packages.values():
        try:
            pkg.extract(string, outdir)
            return True
        except KeyError:
            pass
    return False


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
            if not attempt_to_unpack(name):
                print(f'-> FAILED: {name}')
        fr.seek(xsize * ysize, os.SEEK_CUR)


for path in (outdir / 'spaces' / args.mapname).glob('*.cdata_processed'):
    with ZipFile(path) as cdata:
        with cdata.open('terrain2/blend_textures') as f:
            unpack_blend_textures(f)


spacebin = packages[f'{args.mapname}.pkg'].open(f'spaces/{args.mapname}/space.bin')
space = CompiledSpace(spacebin, args.wotver)
space.unp_for_world_editor(outdir / 'spaces' / args.mapname)


settings_tree = ET.parse((outdir / 'spaces' / args.mapname / 'unpacked_for_world_editor' / 'space.settings'))
for it in settings_tree.findall('.//tile'):
    if not attempt_to_unpack(it.text):
        print(f'-> FAILED: {it.text}')


strings = space.sections['BWST']._data.values()
for string in strings:
    if '.primitives/' in string:
        new_string = string.split('.primitives/')[0]
        attempt_to_unpack(f'{new_string}.primitives_processed')
        attempt_to_unpack(f'{new_string}.visual_processed')
        continue
    attempt_to_unpack(string)


print('# rename stage')
for path in outdir.rglob('*_processed'):
    path.replace(str(path)[:-10])


print('# replace stage')
for path in (outdir / 'spaces' / args.mapname / 'unpacked_for_world_editor').glob('*'):
    path.replace(path.parent.parent / path.name)


print('# remove extra stage')
(outdir / 'spaces' / args.mapname / 'unpacked_for_world_editor').rmdir()
(outdir / 'spaces' / args.mapname / 'space.bin').unlink()
