import os
import sys
import tkinter as tk


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__) ))
    return os.path.join(base_path, '../'+relative_path)



def _global_constants():
        return None

PROGNAME = 'PetPet';
VERSION = '1.00';
LAST_EDITED = '12.04.2025';
    
GFX_DRAW = resource_path('resources/icon_draw.xbm')
GFX_BRUSH = resource_path('resources/icon_colorize.xbm')
GFX_PENCIL = resource_path('resources/icon_brush.xbm')
GFX_BG = resource_path('resources/icon_bg.xbm')

CHARROM_UPPERCASE = resource_path('resources/charrom_uppercase.bin')
CHARROM_LOWERCASE = resource_path('resources/charrom_lowercase.bin')

CHAR_WIDTH = 40
CHAR_HEIGHT = 25

IMAGE_SCALE = 2
IMAGE_WIDTH = CHAR_WIDTH*8
IMAGE_HEIGHT = CHAR_HEIGHT*8
CHARS_IMAGE_WIDTH = 16*8
CHARS_IMAGE_HEIGHT = 16*8

CHARPICKER_LAYOUT_WIDTH = 16
CHARPICKER_LAYOUT_HEIGHT = 16

BGCOLOR='#cccccc'
BGCOLOR_LIGHT='#dddddd'
BGCOLOR2='#ccccff'

FRAME = 2
FRAME_PADY = 2
FRAME_BORDER = 4


MOUSEPOINTER_HAND = 'hand2'
MOUSEPOINTER_NORMAL = 'tcross'
MOUSEPOINTER_NONE = 'X_cursor'




#global variables
def _global_variables():
        return None

root = tk.Tk()
args = None

mousepointer_image = MOUSEPOINTER_NORMAL

data_char = [0] * CHAR_HEIGHT * CHAR_WIDTH
data_color = [0] * CHAR_HEIGHT * CHAR_WIDTH
data_charset = []
data_bg = 0
selected_char = 0

show_grid   = True
charpicker_grid_posx = 0
charpicker_grid_posy = 0

canvas_draw = tk.Canvas()
canvas_chars = tk.Canvas()

my_photo_draw = tk.PhotoImage()
my_photo_chars = tk.PhotoImage()

label_background_image = tk.Label()
label_chars_image = tk.Label()

textvariable_filename   = tk.StringVar()
textvariable_mode   = tk.StringVar()
textvariable_info = tk.StringVar()

mouse_posx = 0
mouse_posy = 0
last_posx = 0
last_posy = 0
this_char_x = 0
this_char_y = 0
last_char_x = 0
last_char_y = 0

mode='draw'

user_drawcolor = tk.IntVar()
user_drawcolor.set(1)


palette = []
chars_layout = []
petscii_bin_filename = ''

button_pen = tk.Button()
button_brush = tk.Button()
button_pencil = tk.Button()
button_bg = tk.Button()
