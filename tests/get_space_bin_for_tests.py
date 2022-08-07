#!python

from multiprocessing import Pool, cpu_count
from pathlib import Path
from zipfile import ZipFile


def unpack_space_bin(pkg_path):
    name = pkg_path.stem
    try:
        with ZipFile(pkg_path, 'r') as zf:
            # TODO: get version from "version.xml"?
            zf.extract(f'spaces/{name}/space.bin', './1.17.0.0')
            print(pkg_path)
    except Exception:
        pass


def pool_handler():
    packages = Path('E:/WoT Clients/World_of_Tanks_RU/res/packages/').glob('*.pkg')
    with Pool(cpu_count()) as pool:
        pool.map(unpack_space_bin, packages)


if __name__ == '__main__':
    pool_handler()