from pathlib import Path

from _base_section import *



class Base_Binary_Section(Base_Section):
    def unp_to_dir(self, unp_dir):
        unp_dir = Path(unp_dir)
        with open(unp_dir.joinpath(f'{self.header}.bin'), 'wb') as fw:
            fw.write(self._data)

    def from_dir(self, unp_dir):
        unp_dir = Path(unp_dir)
        binary_file = unp_dir.joinpath(f'{self.header}.bin')
        self._exist = binary_file.is_file()
        if not self._exist:
            return
        with open(binary_file, 'rb') as fr:
            self._data = fr.read()
