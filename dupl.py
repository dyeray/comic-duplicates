import argparse
import glob
import itertools
import os
from collections import defaultdict
from io import BytesIO
from pprint import pprint
from zipfile import ZipFile

import imagehash
from PIL import Image


def find_duplicates(directory: str):
    patterns = (
        os.path.join(directory, '**', '*.cbz'),
        os.path.join(directory, '*.cbz')
    )
    documents = itertools.chain.from_iterable(glob.iglob(pattern) for pattern in patterns)
    signatures = defaultdict(list)
    for document in documents:
        hash_value = hash_document(document)
        signatures[hash_value].append(document)
    return [value for key, value in signatures.items() if len(value) > 1]


def hash_document(document, hashfunc=imagehash.dhash):
    archive = ZipFile(document)
    cover = archive.namelist()[0]
    img = BytesIO(archive.read(cover))
    hash_value = hashfunc(Image.open(img))
    return str(hash_value)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="Directory to search for comics")
    args = parser.parse_args()
    duplicates = find_duplicates(args.dir)
    pprint(duplicates)
