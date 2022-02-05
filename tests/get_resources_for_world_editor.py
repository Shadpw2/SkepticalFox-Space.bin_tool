from pathlib import Path
from zipfile import ZipFile
import argparse
import sys
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


packages = {}
for pkg_path in (args.wotpath / 'res' / 'packages').glob('*.pkg'):
    packages[pkg_path.name] = ZipFile(pkg_path, 'r')


spacebin = packages[f'{args.mapname}.pkg'].open(f'spaces/{args.mapname}/space.bin')
space = CompiledSpace(spacebin, args.wotver)


def attempt_to_unpack(string):
    for pkg in packages.values():
        try:
            pkg.extract(string, './out')
            return
        except Exception:
            pass


strings = space.sections['BWST']._data.values()
for string in strings:
    if '.primitives/' in string:
        new_string = string.split('.primitives/')[0]
        attempt_to_unpack(f'{new_string}.primitives_processed')
        attempt_to_unpack(f'{new_string}.visual_processed')
        continue
    attempt_to_unpack(string)
