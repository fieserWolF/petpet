#!/bin/bash -e

#./petpet.py -f resources/charrom_lowercase.bin
#./petpet.py -p layout_new.json
./petpet.py -p gary.json


exit 0


PetPet v1.00 [12.04.2025] *** by fieserWolF
usage: petpet.py [-h] [-p PETSCII_FILENAME] [-c CONFIG_FILENAME] [-f FONT_FILENAME]

This is a PETSCII editor. Press F1 for help in the program.

options:
  -h, --help            show this help message and exit
  -p, --petscii_file PETSCII_FILENAME
                        petscii filename (.json)
  -c, --config_file CONFIG_FILENAME
                        name of configuration file (.json)
  -f, --font_file FONT_FILENAME
                        name of font (2048 bytes)

Example: ./petpet.py -p gfx.json -c config.json -f font.bin
