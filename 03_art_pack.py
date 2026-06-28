#!/usr/bin/env python3

from pathlib import Path
from ipodhax.silverdb import pack_silverdb

script_dir = Path(__file__).parent
input_path = script_dir / "body"
output_path = script_dir / "SilverImagesDB.LE.bin2"

with open(output_path, "wb") as silver_stream:
  pack_silverdb(silver_stream, input_path)
