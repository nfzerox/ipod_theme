#!/usr/bin/env python3

from pathlib import Path
from ipodhax.silverdb import unpack_silverdb
import shutil
import os

script_dir = Path(__file__).parent
input_path = script_dir / "SilverImagesDB.LE.bin"
output_dir = script_dir / "body"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

output_dir.mkdir()

with open(input_path, "rb") as silver_stream:
  unpack_silverdb(silver_stream, output_dir)
