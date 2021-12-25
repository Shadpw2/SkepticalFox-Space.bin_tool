from pathlib import Path
from zipfile import ZipFile



packages = Path('E:/Games/World_of_Tanks_RU/res/packages/').glob('*.pkg')



for pkg_path in packages:
    name = pkg_path.stem
    try:
        with ZipFile(pkg_path, 'r') as zf:
            zf.extract(f'spaces/{name}/space.bin', './1.15.0.0')
            print(pkg_path)
    except:
        pass
