import logging
logging.basicConfig(filename='testing.log',  filemode='w', level=logging.INFO)

from pathlib import Path
from compiled_space import CompiledSpace



def unpack_from_space_bin(space_path, unp_dir, filepath, ver):
    try:
        with open(bin_file_name_in, 'rb') as fr:
            space1 = CompiledSpace(fr, ver)

        unp_dir.mkdir(exist_ok=True)
        space1.unp_to_dir(unp_dir)

        space1.unp_for_world_editor(space_path)

    except:
        import traceback
        traceback.print_exc()



def pack_from_dir(unp_dir, dirpath, ver):
    try:
        space2 = CompiledSpace()
        space2.from_dir(unp_dir)
        space2.save_to_bin(pck_dir.joinpath('space.bin'))

        bin_file_name_in = pck_dir.joinpath('space.bin')
        with open(bin_file_name_in, 'rb') as fr:
            space3 = CompiledSpace(fr, ver)

    except:
        import traceback
        traceback.print_exc()



for vpath in Path('tests').iterdir():
    if not vpath.is_dir():
        continue
    ver = vpath.name
    for space_path in vpath.joinpath('spaces').iterdir():
        unp_dir = space_path.joinpath('unpacked')
        bin_file_name_in = space_path.joinpath('space.bin')
        if bin_file_name_in.is_file():
            logging.info(f'orig: {space_path}')
            print(f'orig: {space_path}')
            unpack_from_space_bin(space_path,
                                  unp_dir,
                                  bin_file_name_in,
                                  ver)

        if unp_dir.is_dir():
            pck_dir = space_path.joinpath('packed')
            pck_dir.mkdir(exist_ok=True)

            logging.info(f'new: {pck_dir}')
            print(f'new: {pck_dir}')
            pack_from_dir(unp_dir, pck_dir, ver)
