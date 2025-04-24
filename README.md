# PetPet

PetPet is a PETSCII editor for Commodore 64 computers.
As it is written entirely in Python, it runs on any platform supported by Python (Windows, MacOS, Linux and others).

![screenshot](./screenshot.png)


# Why PetPet?

reason | description
---|---
script | no compiling, easy to modify import and export to your needs
portable | available on Linux, MacOS, Windows and any other system supported by Python3

# Using PetPet

## drawing modes

Use left mouse-button to draw. These are the drawing modes:

mode | description
---|---
pen | draw characters and colors
brush | draw only colors
pencil | draw only characters
writemode | type characters on your keyboard directly at mouse position
set bg | choose a color, then click into the picture to change the background color (\$d021)
set border | choose a color, then click into the picture to change the border color (\$d020)


## cut, copy and paste

Use right mouse-button to select an area. Then, use the usual hotkeys (STRG+X, STRG+C, STRG+V) to cut, copy and paste.


## How to change the layout

You can change the layout of the available characters in your own configuration-file.
In this JSON file you can edit the "layout" array.

Example layouts:

![layout1](./layout1.png)

![layout2](./layout2.png)


# Commandline options

	PetPet v1.00 REVISION PARTY 2025 [19.04.2025] *** by fieserWolF
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



# File Formats

The PETSCII image is natively stored as a json file. There is also a binary import and export.

## PetPet JSON format

object | key | type | value
---|---|---|---
info | program | string | "PetPet"
info | version | string | e.g. "1.0"
settings | background | number | color 0-15
settings | border | number | color 0-15
settings | font | string | filename of font
settings | grid | boolean | True or False
. | char | array of 1000 numbers | characters (0-255)
. | color | array of 1000 numbers | colors (0-15)


## binary format

offset | size in bytes | value
---|---|---
0 | 1000 | characters
1000 | 1000 | colors
1001 | 1 | background color
1002 | 1 | border color


## PETSCII-EDITOR binary format

offset | size in bytes | value
---|---|---
0 | 2 | start address $3000 (low, high)
2 | 1000 | characters
1002 | 1 | border color
1003 | 1 | background color
1004 | 1 | $d018 value ($14 or $16)
1029 | 1000 | colors


## PetPet JSON configuration format

object | key | type | value
---|---|---|---
info | program | string | "PetPet"
info | version | string | e.g. "1.0"
settings | background | number | color 0-15
settings | border | number | color 0-15
settings | font | string | filename of font
settings | grid | boolean | True or False
. | palette | array of 16*3 numbers | red, green, blue value for each C64 color (default: PEPTO colors) (0-255)
. | layout | array of 256 numbers | characters (0-255)



# Author

* fieserWolF/Abyss-Connection - *initial work* - [https://github.com/fieserWolF](https://github.com/fieserWolF) [https://csdb.dk/scener/?id=3623](https://csdb.dk/scener/?id=3623)

# Acknowledgements

* Logiker for testing and feature ideas
* Mermaid for the still wonderful PETSCII entitled "Gary"
# Getting Started

## Install Python

### Prerequisites

At least this is needed to run the script directly:

- python 3
- python tkinter module
- python json module
- python "argparse" library


### Install Python on Linux

On my Debian GNU/Linux machine I use apt-get to install everything needed:
```
apt update
apt install python3 python3-tk
```

Alternatively, you can use pip to install missing modules:
```
pip3 install tk argparse json
```


### Install Python on Windows or Mac

* Download Python from [https://www.python.org](https://www.python.org).
* Install Python on your computer.


## Download PetPet

* Go to [https://github.com/fieserWolF/petpet](https://github.com/fieserWolF/petpet).
* Click on the green "Code" button and "Download ZIP"
* Extract the downloaded ZIP-file to any folder.
# Changelog

## Future plans

Any help and support in any form is highly appreciated.

If you have a feature request, a bug report or if you want to offer help, please, contact me:


[http://csdb.dk/scener/?id=3623](http://csdb.dk/scener/?id=3623)
or
[wolf@abyss-connection.de](wolf@abyss-connection.de)



## Changes in 1.01

* improved selection box
* added write-mode
* gui improvements
* export to C64 executable
* improved documentation


## Changes in 1.0

released on REVISION PARTY 2025

- initial release
# License

_PetPet is a PETSCII editor for Commodore 64 computers._

_Copyright (C) 2025 fieserWolF / Abyss-Connection_

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).

See the [LICENSE](LICENSE) file for details.

For further questions, please contact me at
[http://csdb.dk/scener/?id=3623](http://csdb.dk/scener/?id=3623)
or
[wolf@abyss-connection.de](wolf@abyss-connection.de)

For Python3, The Python Imaging Library (PIL), Tcl/Tk and other used source licenses see file [LICENSE_OTHERS](LICENSE_OTHERS).


