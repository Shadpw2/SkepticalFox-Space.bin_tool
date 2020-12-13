import os
import multiprocessing
from glob import glob
from compiled_space import CompiledSpace
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def operation_wrap(arg):
	space_path, wot_version = arg

	for handler in logger.handlers:
		handler.stream.close()
		logger.removeHandler(handler)
	fh = logging.FileHandler(os.path.join(space_path, 'testing.log'), 'w')
	fh.setFormatter(logging.Formatter(fmt='%(message)s'))
	logger.addHandler(fh)

	logging.info('*** orig ***')
	print('orig: %s' % space_path)
	bin_file_name_in = os.path.join(space_path, 'space.bin')
	with open(bin_file_name_in, 'rb') as fr:
		space1 = CompiledSpace(fr, wot_version)

	unp_dir = os.path.join(space_path, 'unpacked')
	if not os.path.exists(unp_dir):
		os.mkdir(unp_dir)
	space1.unp_to_dir(unp_dir)

	space1.unp_for_world_editor(space_path)

	# TODO:
	return

	pck_dir = os.path.join(space_path, 'packed')
	if not os.path.exists(pck_dir):
		os.mkdir(pck_dir)
	space2 = CompiledSpace()
	space2.from_dir(unp_dir)
	space2.save_to_bin(os.path.join(pck_dir, 'space.bin'))

	logging.info('*** new ***')
	bin_file_name_in = os.path.join(pck_dir, 'space.bin')
	with open(bin_file_name_in, 'rb') as fr:
		space3 = CompiledSpace(fr, wot_version)



def main():
	args = []
	for vpath in glob('.\\tests\\*'):
		if not os.path.isdir(vpath):
			continue
		wot_version = os.path.basename(vpath)
		for space_path in glob('.\\tests\\%s\\spaces\\*' % wot_version):
			args.append([space_path, wot_version])


	job_total = multiprocessing.cpu_count()
	pool = multiprocessing.Pool(processes=job_total * 2)
	pool.map(operation_wrap, args)



if __name__ == "__main__":
	main()
