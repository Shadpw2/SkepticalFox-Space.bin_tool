import os
import multiprocessing
from pathlib import Path
from compiled_space import CompiledSpace
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def operation_wrap(arg):
    space_path, wot_version = arg

    for handler in logger.handlers:
        handler.stream.close()
        logger.removeHandler(handler)
    fh = logging.FileHandler(space_path / 'testing.log', 'w')
    fh.setFormatter(logging.Formatter(fmt='%(message)s'))
    logger.addHandler(fh)

    logging.info('*** orig ***')
    print('orig: %s' % space_path)
    bin_file_name_in = (space_path / 'space.bin')
    with bin_file_name_in.open('rb') as fr:
        space1 = CompiledSpace(fr, wot_version)

    unp_dir = (space_path / 'unpacked')
    unp_dir.mkdir(exist_ok=True)
    space1.unp_to_dir(unp_dir)

    space1.unp_for_world_editor(space_path)

    # TODO:
    return

    pck_dir = (space_path / 'packed')
    pck_dir.mkdir(exist_ok=True)
    space2 = CompiledSpace()
    space2.from_dir(unp_dir)
    space2.save_to_bin(pck_dir / 'space.bin')

    logging.info('*** new ***')
    bin_file_name_in = (pck_dir / 'space.bin')
    with bin_file_name_in.open('rb') as fr:
        space3 = CompiledSpace(fr, wot_version)


def main():
    args = []
    for vpath in Path('tests').iterdir():
        if not vpath.is_dir():
            continue
        wot_version = vpath.name
        for space_path in (vpath / 'spaces').iterdir():
            args.append([space_path, wot_version])

    job_total = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=job_total * 2)
    pool.map(operation_wrap, args)


if __name__ == "__main__":
    main()
