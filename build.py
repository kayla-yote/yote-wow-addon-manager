#! /usr/bin/env python3

assert __name__ == '__main__'

import os
from pathlib import *
import shutil
import zipfile

SRC = Path(__file__).parent
OUT = SRC / 'dist'
PRODUCT = 'yote-wow-addon-manager'

try:
    shutil.rmtree(SRC / OUT)
except FileNotFoundError:
    pass
os.mkdir(SRC / OUT)

def best_zip(*args, **kwargs):
    for compression in [zipfile.ZIP_LZMA, zipfile.ZIP_BZIP2, zipfile.ZIP_DEFLATED]:
        try:
            return zipfile.ZipFile(*args, compression=compression, **kwargs)
        except RuntimeError:
            pass
    return zipfile.ZipFile(*args, **kwargs)

zip_path = OUT / f'{PRODUCT}.zip'
rel_zip_path = zip_path.relative_to(SRC)
print(f'> {rel_zip_path}')
with best_zip(zip_path, mode='w') as z:
    z.mkdir(PRODUCT)

    def add(path):
        src = SRC / path
        dst = f'{PRODUCT}/{path}'
        print(f'> {rel_zip_path}/{dst}')
        z.write(src, arcname=dst)

    add('LICENSE')
    add('README.md')
    add('manager.py')
    add('update-addons.bat')
    
print('Done!')
