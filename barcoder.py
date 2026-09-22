from io import BytesIO
import barcode
from barcode.writer import ImageWriter
import pandas as pd
import json
import os
# uses the python-barcode library
# code39 definitely works, code128 does not, most others are numeric only so might not work
my_codec = barcode.get_barcode_class("code39")

my_files = input("dirpath to files to draw from: ")

for dirpath, dirnames, filenames in os.walk(my_files):
    for filename in filenames:
        filename = os.path.join(dirpath, filename)
        if filename.endswith(".json"):
            with open(filename, "r") as r:
                data = json.load(r)
                container_name = data["container_name"]
                my_code = my_codec(container_name, writer=ImageWriter())
                fullname = my_code.save(container_name, options={'module_width': 0.3, 'format': "JPEG"})