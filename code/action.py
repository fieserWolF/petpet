import code.myGlobals as myGlobals
import os
import struct
import tkinter as tk
import json
#import time


    
def load_json(
    filename
) :
    print ("    Opening json file \"%s\" for reading..." % filename)
    try:
        file = open(filename , "r")
    except IOError as err:
        print("I/O error: {0}".format(err))
        return 1

    my_data = json.load(file)
    file.close()
    return my_data
    


def load_config() :
    data = load_json(myGlobals.args.config_filename)
    myGlobals.palette = data['palette']
    myGlobals.chars_layout = data['layout']
    myGlobals.show_grid = data['settings']['grid']
    myGlobals.data_bg = data['settings']['background']
    myGlobals.data_border = data['settings']['border']


def load_petscii_json() :
    data = load_json(myGlobals.args.petscii_filename)
    myGlobals.show_grid = data['settings']['grid']
    myGlobals.data_bg = data['settings']['background']
    myGlobals.data_border = data['settings']['border']
    myGlobals.data_char = data['char']
    myGlobals.data_color = data['color']
    myGlobals.args.font_filename =  data['settings']['font']
    load_charset()
    myGlobals.textvariable_filename.set(myGlobals.args.petscii_filename)
    #myGlobals.user_drawcolor.set(myGlobals.data_color)
    draw_petscii_image_full()
    refresh_draw_image(draw_border=True)
    update_info()


def load_petscii_bin() :
    START_CHARS = 0
    START_COLOR = 1000
    START_BG = 2000
    START_BORDER = 2001
    SIZE_CHARS = myGlobals.CHAR_HEIGHT*myGlobals.CHAR_WIDTH
    SIZE_COLORS = myGlobals.CHAR_HEIGHT*myGlobals.CHAR_WIDTH

    data = load_some_data(myGlobals.args.petscii_bin_filename)
    myGlobals.show_grid = True
    myGlobals.data_char = data[START_CHARS:START_CHARS+SIZE_CHARS]
    myGlobals.data_color = data[START_COLOR:START_COLOR+SIZE_COLORS]
    myGlobals.data_bg = data[START_BG] & 0b00001111
    myGlobals.data_border = data[START_BORDER] & 0b00001111
    
    for i in range(0,len(myGlobals.data_color)):
         myGlobals.data_color[i] = myGlobals.data_color[i] & 0b00001111
   
    myGlobals.textvariable_filename.set(myGlobals.args.petscii_bin_filename)
    draw_petscii_image_full()
    refresh_draw_image(draw_border=True)
    update_info()


def load_petscii_bin_petscii_editor() :
    """
    PETSCII-Editor Format
    $3000-$33e7 chars
    $33e8 border color
    $33e9 bg color
    $33ea $d018 ($14 or $16)
    $3400-$37e7 colors
    """

    START_OFFSET = 2
    START_CHARS = START_OFFSET+0x0000
    START_BORDER = START_OFFSET+0x03e8
    START_BG = START_OFFSET+0x03e9
    START_COLOR = START_OFFSET+0x0400
    SIZE_CHARS = myGlobals.CHAR_HEIGHT*myGlobals.CHAR_WIDTH
    SIZE_COLORS = myGlobals.CHAR_HEIGHT*myGlobals.CHAR_WIDTH

    data = load_some_data(myGlobals.args.petscii_bin_filename)
    myGlobals.show_grid = True
    myGlobals.data_char = data[START_CHARS:START_CHARS+SIZE_CHARS]
    myGlobals.data_color = data[START_COLOR:START_COLOR+SIZE_COLORS]
    myGlobals.data_bg = data[START_BG] & 0b00001111
    myGlobals.data_border = data[START_BORDER] & 0b00001111
    
    for i in range(0,len(myGlobals.data_color)):
         myGlobals.data_color[i] = myGlobals.data_color[i] & 0b00001111
   
    myGlobals.textvariable_filename.set(myGlobals.args.petscii_bin_filename)
    draw_petscii_image_full()
    refresh_draw_image(draw_border=True)
    update_info()

"""
def load_petscii_bin_editor() :
    START_CHARS = 2
    START_COLOR = 1024+2
    START_BG = 2002
    START_BORDER = 2003
    SIZE_CHARS = myGlobals.CHAR_HEIGHT*myGlobals.CHAR_WIDTH
    SIZE_COLORS = myGlobals.CHAR_HEIGHT*myGlobals.CHAR_WIDTH

    data = load_some_data(myGlobals.args.petscii_bin_filename)
    myGlobals.show_grid = True
    myGlobals.data_char = data[START_CHARS:START_CHARS+SIZE_CHARS]
    myGlobals.data_color = data[START_COLOR:START_COLOR+SIZE_COLORS]
    myGlobals.data_bg = data[START_BG] & 0b00001111
    myGlobals.data_border = data[START_BORDER] & 0b00001111
    
    for i in range(0,len(myGlobals.data_color)):
         myGlobals.data_color[i] = myGlobals.data_color[i] & 0b00001111
   
    myGlobals.textvariable_filename.set(myGlobals.args.petscii_bin_filename)
    draw_petscii_image_full()
    refresh_draw_image(draw_border=True)
    update_info()
"""


def save_config() :
    my_data = {
        'info' : {
            'program' : myGlobals.PROGNAME,
            'version' : myGlobals.VERSION
        },
        'settings' : {
            'grid' : myGlobals.show_grid,
            'background' : myGlobals.data_bg,
            'border' : myGlobals.data_border,
            'font' : myGlobals.args.font_filename
        },
        'palette' : myGlobals.palette,
        'layout' : myGlobals.chars_layout,
    }

    write_json(
        myGlobals.args.config_filename,
        my_data
    )


def save_petscii_json() :
    my_data = {
        'info' : {
            'program' : myGlobals.PROGNAME,
            'version' : myGlobals.VERSION
        },
        'settings' : {
            'grid' : myGlobals.show_grid,
            'background' : myGlobals.data_bg,
            'border' : myGlobals.data_border,
            'font' : myGlobals.args.font_filename
        },
        'char' : myGlobals.data_char,
        'color' : myGlobals.data_color
    }

    write_json(
        myGlobals.args.petscii_filename,
        my_data
    )
    myGlobals.textvariable_filename.set(myGlobals.args.petscii_filename)
    myGlobals.image_is_saved = True


def write_json(
    filename,
    my_data
) :    
    if ( len(my_data) == 0 ) :
        return None
        
    # write file
    print ('    Opening json file "%s" for writing...' % filename, end='')
    try:
        file_out = open(filename , "w", encoding='utf8')
    except IOError as err:
        print("I/O error: {0}".format(err))
        sys.exit(1)

    #write to file
    json.dump(my_data, file_out,indent=4, ensure_ascii=False)
    file_out.close()
    print("done.")

    return None



def convert_to_photo_image(
    my_width,
    my_height,
    my_data
) :
    #https://en.wikipedia.org/wiki/Netpbm#Description
    #"PPM" portable pixmap
    #header
    #picture data (an array of bytes)
    
    #https://www.programiz.com/python-programming/methods/string/encode
    #https://www.programiz.com/python-programming/methods/built-in/bytearray
    #data = ('P6 '+str(my_width)+' '+str(my_height)+' 255 ').encode() +bytearray(my_data)
    data = ('P6 '+str(my_width)+' '+str(my_height)+' 255 ').encode(encoding='UTF-8',errors='strict') + bytearray(my_data)
    #print(data)

    return tk.PhotoImage(width=my_width, height=my_height, data=data, format='PPM')



def create_draw_canvas_grid() :
    #print("create_draw_canvas_grid()")
    GRID_COLOR = '#aaaaaa'
    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_line.html
    for y in range(0,int(myGlobals.IMAGE_HEIGHT/8)) :
        myGlobals.canvas_draw.create_line(
            myGlobals.BORDER_WIDTH, #x0
            myGlobals.BORDER_WIDTH+y*8*myGlobals.IMAGE_SCALE,     #y0
            myGlobals.BORDER_WIDTH+myGlobals.IMAGE_WIDTH*myGlobals.IMAGE_SCALE,    #x1
            myGlobals.BORDER_WIDTH+y*8*myGlobals.IMAGE_SCALE, #y1
            fill=GRID_COLOR,
            tags='grid')
    for x in range(0,int(myGlobals.IMAGE_WIDTH/8)) :
        myGlobals.canvas_draw.create_line(
            myGlobals.BORDER_WIDTH+x*8*myGlobals.IMAGE_SCALE, #x0
            myGlobals.BORDER_WIDTH,     #y0
            myGlobals.BORDER_WIDTH+x*8*myGlobals.IMAGE_SCALE,    #x1
            myGlobals.BORDER_WIDTH+myGlobals.IMAGE_HEIGHT*myGlobals.IMAGE_SCALE, #y1
            fill=GRID_COLOR,
            tags='grid')


def draw_charset_image_single(
    char_number,
    color,
    bg_color
) :
    SCALE = 2
    CHAR_WIDTH = 8*SCALE
    CHAR_HEIGHT = 8*SCALE
   
    data = [myGlobals.palette[bg_color]] * CHAR_HEIGHT * CHAR_WIDTH

    #draw charset
    for y in range(0,8) :
        for x in range(0,8) :
            value = myGlobals.data_charset[char_number][y][x]

            if (value != 0) :
                rgb = myGlobals.palette[color]
            
                xx = x*SCALE
                yy = y*SCALE

                pos1 = ((yy+0)*CHAR_WIDTH) +xx+0
                pos2 = ((yy+0)*CHAR_WIDTH) +xx+1
                pos3 = ((yy+1)*CHAR_WIDTH) +xx+0
                pos4 = ((yy+1)*CHAR_WIDTH) +xx+1
                data[pos1] = rgb
                data[pos2] = rgb
                data[pos3] = rgb
                data[pos4] = rgb
            
    return data


def draw_petscii_image_single(x,y,char,color) :
    #debug_time('draw_petscii_image_single()')
    
    CHAR_WIDTH = 8 * myGlobals.IMAGE_SCALE
    CHAR_HEIGHT = 8 * myGlobals.IMAGE_SCALE
    PANEL_WIDTH = myGlobals.CHAR_WIDTH * 8 * myGlobals.IMAGE_SCALE
    PANEL_HEIGHT = myGlobals.CHAR_HEIGHT * 8 * myGlobals.IMAGE_SCALE
    my_bytes = [255,100,100] * CHAR_WIDTH * CHAR_HEIGHT
    #my_data = [0] * CHAR_WIDTH * CHAR_HEIGHT

    my_data = draw_charset_image_single(char, color, myGlobals.data_bg)
        
    pos = (y*CHAR_HEIGHT*PANEL_WIDTH) + x*CHAR_WIDTH

    for yy in range(0,CHAR_HEIGHT) :
        for xx in range(0,CHAR_WIDTH) :
            pos_src = ( (yy*CHAR_WIDTH)+xx )*1
            pos_dst = (pos + (yy*PANEL_WIDTH) + xx)*3
           
            myGlobals.PETSCII_image_data[pos_dst+0] = my_data[pos_src][0]
            myGlobals.PETSCII_image_data[pos_dst+1] = my_data[pos_src][1]
            myGlobals.PETSCII_image_data[pos_dst+2] = my_data[pos_src][2]

    myGlobals.my_photo_draw = convert_to_photo_image(PANEL_WIDTH, PANEL_HEIGHT, myGlobals.PETSCII_image_data)
    myGlobals.image_is_saved = False    

    
def draw_petscii_image_full() :
    #debug_time('draw_petscii_image_full()')
    #https://dafarry.github.io/tkinterbook/photoimage.htm
    #https://inf-schule.de/software/gui/entwicklung_tkinter/bilder
    #my_photo = tk.PhotoImage(file="image.ppm")
    
    CHAR_WIDTH = 8*myGlobals.IMAGE_SCALE
    CHAR_HEIGHT = 8*myGlobals.IMAGE_SCALE
    PANEL_WIDTH=myGlobals.CHAR_WIDTH*8*myGlobals.IMAGE_SCALE
    PANEL_HEIGHT=myGlobals.CHAR_HEIGHT*8*myGlobals.IMAGE_SCALE

    #background
    myGlobals.PETSCII_image_data = [255,100,100] * PANEL_HEIGHT * PANEL_WIDTH

    #draw chars
    my_data = [0] * CHAR_HEIGHT * CHAR_WIDTH
    char_number=0
    for y in range(0,myGlobals.CHAR_HEIGHT) :
        for x in range(0,myGlobals.CHAR_WIDTH) :
            my_data = draw_charset_image_single(myGlobals.data_char[char_number],myGlobals.data_color[char_number],myGlobals.data_bg)

            pos = (y*CHAR_HEIGHT*PANEL_WIDTH) + x*CHAR_WIDTH

            for yy in range(0,CHAR_HEIGHT) :
                for xx in range(0,CHAR_WIDTH) :
                    
                    pos_src = ( (yy*CHAR_WIDTH)+xx )*1
                    pos_dst = (pos + (yy*PANEL_WIDTH) + xx)*3
                   
                    myGlobals.PETSCII_image_data[pos_dst+0] = my_data[pos_src][0]
                    myGlobals.PETSCII_image_data[pos_dst+1] = my_data[pos_src][1]
                    myGlobals.PETSCII_image_data[pos_dst+2] = my_data[pos_src][2]
                    
            char_number+=1
    
    myGlobals.my_photo_draw = convert_to_photo_image(PANEL_WIDTH, PANEL_HEIGHT, myGlobals.PETSCII_image_data)



def draw_charset_image() :
    #https://dafarry.github.io/tkinterbook/photoimage.htm
    #https://inf-schule.de/software/gui/entwicklung_tkinter/bilder
    #my_photo = tk.PhotoImage(file="image.ppm")

    my_bytes = []
    #SCALE = myGlobals.IMAGE_SCALE
    CHAR_WIDTH = 8*myGlobals.IMAGE_SCALE
    CHAR_HEIGHT = 8*myGlobals.IMAGE_SCALE
    PANEL_WIDTH=myGlobals.CHARPICKER_LAYOUT_WIDTH*CHAR_WIDTH
    PANEL_HEIGHT=myGlobals.CHARPICKER_LAYOUT_HEIGHT*CHAR_HEIGHT

    #clear bg
    my_bytes = [255,100,100] * PANEL_HEIGHT * PANEL_WIDTH

    #draw charset
    char_number=0
    for y in range(0,myGlobals.CHARPICKER_LAYOUT_HEIGHT) :
        for x in range(0,myGlobals.CHARPICKER_LAYOUT_WIDTH) :
            my_data = draw_charset_image_single(myGlobals.chars_layout[char_number],1,0)

            pos = (y*CHAR_HEIGHT*PANEL_WIDTH) + x*CHAR_WIDTH

            for yy in range(0,CHAR_HEIGHT) :
                for xx in range(0,CHAR_WIDTH) :
                    
                    pos_src = ( (yy*CHAR_WIDTH)+xx )*1
                    pos_dst = (pos + (yy*PANEL_WIDTH) + xx)*3
                    
                    my_bytes[pos_dst+0] = my_data[pos_src][0]
                    my_bytes[pos_dst+1] = my_data[pos_src][1]
                    my_bytes[pos_dst+2] = my_data[pos_src][2]
            
            char_number+=1

    myGlobals.my_photo_chars = convert_to_photo_image(PANEL_WIDTH,PANEL_HEIGHT, my_bytes)



def change_bg(
):
    myGlobals.mode = 'set bg'
    myGlobals.button_pen.configure(relief=tk.RAISED)
    myGlobals.button_brush.configure(relief=tk.RAISED)
    myGlobals.button_pencil.configure(relief=tk.RAISED)
    myGlobals.button_bg.configure(relief=tk.SUNKEN)
    myGlobals.button_border.configure(relief=tk.RAISED)
    myGlobals.button_writemode.configure(relief=tk.RAISED)
    myGlobals.button_grid.configure(relief=tk.RAISED)
    update_info()

def change_border(
):
    myGlobals.mode = 'set border'
    myGlobals.button_pen.configure(relief=tk.RAISED)
    myGlobals.button_brush.configure(relief=tk.RAISED)
    myGlobals.button_pencil.configure(relief=tk.RAISED)
    myGlobals.button_bg.configure(relief=tk.RAISED)
    myGlobals.button_border.configure(relief=tk.SUNKEN)
    myGlobals.button_writemode.configure(relief=tk.RAISED)
    myGlobals.button_grid.configure(relief=tk.RAISED)
    update_info()
    
def draw(
):
    myGlobals.mode = 'pen'
    myGlobals.button_pen.configure(relief=tk.SUNKEN)
    myGlobals.button_brush.configure(relief=tk.RAISED)
    myGlobals.button_pencil.configure(relief=tk.RAISED)
    myGlobals.button_bg.configure(relief=tk.RAISED)
    myGlobals.button_border.configure(relief=tk.RAISED)
    myGlobals.button_writemode.configure(relief=tk.RAISED)
    myGlobals.button_grid.configure(relief=tk.RAISED)
    update_info()


def toggle_grid(
):
    if (myGlobals.show_grid) :
        myGlobals.show_grid = False
    else :
        myGlobals.show_grid = True
    
    refresh_draw_image()


def writemode(
):
    myGlobals.mode = 'writemode'
    myGlobals.button_pen.configure(relief=tk.RAISED)
    myGlobals.button_brush.configure(relief=tk.RAISED)
    myGlobals.button_pencil.configure(relief=tk.RAISED)
    myGlobals.button_bg.configure(relief=tk.RAISED)
    myGlobals.button_border.configure(relief=tk.RAISED)
    myGlobals.button_writemode.configure(relief=tk.SUNKEN)
    myGlobals.button_grid.configure(relief=tk.RAISED)
    update_info()


def brush(
):
    myGlobals.mode = 'brush'
    myGlobals.button_pen.configure(relief=tk.RAISED)
    myGlobals.button_brush.configure(relief=tk.SUNKEN)
    myGlobals.button_pencil.configure(relief=tk.RAISED)
    myGlobals.button_bg.configure(relief=tk.RAISED)
    myGlobals.button_border.configure(relief=tk.RAISED)
    myGlobals.button_writemode.configure(relief=tk.RAISED)
    myGlobals.button_grid.configure(relief=tk.RAISED)
    update_info()

def pencil(
):
    myGlobals.mode = 'pencil'
    myGlobals.button_pen.configure(relief=tk.RAISED)
    myGlobals.button_brush.configure(relief=tk.RAISED)
    myGlobals.button_pencil.configure(relief=tk.SUNKEN)
    myGlobals.button_bg.configure(relief=tk.RAISED)
    myGlobals.button_border.configure(relief=tk.RAISED)
    myGlobals.button_writemode.configure(relief=tk.RAISED)
    myGlobals.button_grid.configure(relief=tk.RAISED)
    update_info()


def clear_image():
    myGlobals.data_char = [myGlobals.INIT_CHAR] * myGlobals.CHAR_HEIGHT * myGlobals.CHAR_WIDTH
    myGlobals.data_color = [myGlobals.INIT_COLOR] * myGlobals.CHAR_HEIGHT * myGlobals.CHAR_WIDTH
    myGlobals.data_bg = myGlobals.INIT_BG
    myGlobals.data_border = myGlobals.INIT_BORDER
    myGlobals.user_drawcolor.set(1)
    myGlobals.image_is_saved  = True
    draw_petscii_image_full()
    refresh_draw_image(draw_border=True)



def undo_store():
    data_pos = myGlobals.mouse_posy * myGlobals.CHAR_WIDTH +myGlobals.mouse_posx
    
    #exit if not needed:
    if (
        (myGlobals.data_char[data_pos] == myGlobals.selected_char) &
        (myGlobals.data_color[data_pos] == myGlobals.user_drawcolor.get())
    ) :
        return None
    
    myGlobals.undo_posx.append(myGlobals.mouse_posx)
    myGlobals.undo_posy.append(myGlobals.mouse_posy)
    myGlobals.undo_char.append(myGlobals.data_char[data_pos])
    myGlobals.undo_color.append(myGlobals.data_color[data_pos])
    if (myGlobals.undo_pos < myGlobals.UNDO_POS_MAX) :
        myGlobals.undo_pos += 1
    #print('undo %d'%myGlobals.undo_pos)


def undo_restore():
    if (myGlobals.undo_pos == 0) :
        return None

    
    if (myGlobals.undo_busy) :
        return None
    
    myGlobals.undo_busy = True

    #print('Undo busy=%s'%myGlobals.undo_busy)

    myGlobals.undo_pos -= 1
        
    posx = myGlobals.undo_posx.pop()
    posy = myGlobals.undo_posy.pop()
    
    restore_char = myGlobals.undo_char.pop()
    restore_color = myGlobals.undo_color.pop()
    
    data_pos = posy * myGlobals.CHAR_WIDTH + posx
    
    #exit if not needed:
    if (
        (myGlobals.data_char[data_pos] == restore_char) &
        (myGlobals.data_color[data_pos] == restore_color)
    ) :
        myGlobals.undo_busy = False
        return None
    
    myGlobals.data_char[data_pos] = restore_char
    myGlobals.data_color[data_pos] = restore_color

    draw_petscii_image_single(
        posx,   #x
        posy,   #y
        restore_char,    #char
        restore_color  #color
    )

    #draw_petscii_image_full()
    refresh_draw_image()
    
    myGlobals.undo_busy = False
    

def userwrite_letter(
    letter
):
    if (myGlobals.mode == 'writemode') :
        myGlobals.selected_char = myGlobals.C64_SCREENCODES[letter]

        myGlobals.last_drawn_posx = myGlobals.mouse_posx
        myGlobals.last_drawn_posy = myGlobals.mouse_posy
        
        undo_store()
        myGlobals.data_char[myGlobals.mouse_posy * myGlobals.CHAR_WIDTH +myGlobals.mouse_posx] = myGlobals.selected_char
        myGlobals.data_color[myGlobals.mouse_posy * myGlobals.CHAR_WIDTH +myGlobals.mouse_posx] = myGlobals.user_drawcolor.get()
        draw_petscii_image_single(
            myGlobals.mouse_posx,   #x
            myGlobals.mouse_posy,   #y
            myGlobals.data_char[myGlobals.mouse_posy * myGlobals.CHAR_WIDTH +myGlobals.mouse_posx],    #char
            myGlobals.data_color[myGlobals.mouse_posy * myGlobals.CHAR_WIDTH +myGlobals.mouse_posx]  #color
        )
        refresh_draw_image()
        

def cut():
    myGlobals.box_visible = False
    copy()
    for y in range(0,myGlobals.box_height) :
        dst = (myGlobals.box_start_y+y) * myGlobals.CHAR_WIDTH + myGlobals.box_start_x
        for x in range(0,myGlobals.box_width) :
            myGlobals.data_char[dst+x] = myGlobals.INIT_CHAR
            myGlobals.data_color[dst+x] = myGlobals.INIT_COLOR
    myGlobals.image_is_saved  = False
    draw_petscii_image_full()
    refresh_draw_image()

    
def copy():
    myGlobals.box_visible = False
    refresh_draw_image()
    myGlobals.box_width = myGlobals.box_end_x-myGlobals.box_start_x
    myGlobals.box_height = myGlobals.box_end_y-myGlobals.box_start_y

    myGlobals.box_char = []
    myGlobals.box_color = []
    for y in range(0,myGlobals.box_height) :
        pos = (myGlobals.box_start_y+y) * myGlobals.CHAR_WIDTH + myGlobals.box_start_x
        myGlobals.box_char.append( myGlobals.data_char[pos:pos+myGlobals.box_width] )
        myGlobals.box_color.append( myGlobals.data_color[pos:pos+myGlobals.box_width] )
            
    
def paste():
    myGlobals.box_visible = False
    
    for y in range(0,myGlobals.box_height) :
        if (myGlobals.mouse_posy+y > myGlobals.CHAR_HEIGHT-1) : break
        src = y * myGlobals.box_width
        dst = (myGlobals.mouse_posy+y) * myGlobals.CHAR_WIDTH + myGlobals.mouse_posx
        for x in range(0,myGlobals.box_width) :
            if (myGlobals.mouse_posx+x > myGlobals.CHAR_WIDTH-1) : continue
            myGlobals.data_char[dst+x] = myGlobals.box_char[y][x]
            myGlobals.data_color[dst+x] = myGlobals.box_color[y][x]

    myGlobals.image_is_saved  = False
    draw_petscii_image_full()
    refresh_draw_image()
    
    

"""
def debug_time(
    message
) :
    duration = round(time.time()*1000-myGlobals.time_last)
    print('%04d "%s"'%(duration,message))
    myGlobals.time_last = time.time()*1000
"""    

def create_draw_canvas_elements(draw_border = False):
    #print('create_draw_canvas_elements()')
    #myGlobals.canvas_draw.delete("all")
    
    mycolor = '#%02x%02x%02x' % (
            myGlobals.palette[myGlobals.data_border][0],
            myGlobals.palette[myGlobals.data_border][1],
            myGlobals.palette[myGlobals.data_border][2]
    )

    myGlobals.canvas_draw.create_rectangle(0, 0, myGlobals.FULL_SCREEN_WIDTH, myGlobals.FULL_SCREEN_HEIGHT, fill=mycolor, tags='border')

    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_rectangle.html
    #if (draw_border) :
    #    myGlobals.canvas_draw.create_rectangle(0, 0, myGlobals.FULL_SCREEN_WIDTH, myGlobals.FULL_SCREEN_HEIGHT, fill=mycolor, tags='border')

    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_image.html
    myGlobals.canvas_draw.create_image(myGlobals.BORDER_WIDTH, myGlobals.BORDER_WIDTH, image=myGlobals.my_photo_draw, anchor=tk.NW, tags='petscii_image')
    
    create_draw_canvas_grid()

    BOX_COLOR = '#00ff00'
    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_rectangle.html
    myGlobals.canvas_draw.create_rectangle(
        myGlobals.box_start_x*8*myGlobals.IMAGE_SCALE+myGlobals.BORDER_WIDTH,
        myGlobals.box_start_y*8*myGlobals.IMAGE_SCALE+myGlobals.BORDER_WIDTH,
        myGlobals.box_end_x*8*myGlobals.IMAGE_SCALE+myGlobals.BORDER_WIDTH,
        myGlobals.box_end_y*8*myGlobals.IMAGE_SCALE+myGlobals.BORDER_WIDTH,
        outline=BOX_COLOR,
        tags='box',
        width=2,
        state='hidden'
    )

    update_info()



def refresh_draw_image(draw_border = False):
    #print('refresh_chars_image()')
    #print('undo steps=%04d draw_border=%s show_grid=%s show_box=%s'%(myGlobals.undo_pos,draw_border,myGlobals.show_grid,myGlobals.box_visible))

    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/canvas-methods.html
    #myGlobals.canvas_draw.delete("all")
    
    mycolor = '#%02x%02x%02x' % (
            myGlobals.palette[myGlobals.data_border][0],
            myGlobals.palette[myGlobals.data_border][1],
            myGlobals.palette[myGlobals.data_border][2]
    )
    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_rectangle.html
    if (draw_border) :
        myGlobals.canvas_draw.itemconfigure('border', fill=mycolor)
    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_image.html    
    myGlobals.canvas_draw.itemconfigure('petscii_image', image=myGlobals.my_photo_draw)
    
    if (myGlobals.show_grid) :
        myGlobals.canvas_draw.itemconfigure("grid", state='normal')
    else :
        myGlobals.canvas_draw.itemconfigure("grid", state='hidden')


    #print(myGlobals.canvas_draw.itemconfigure('box'))

    if (myGlobals.box_visible) :
        #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_rectangle.html
        #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/canvas-methods.html
        myGlobals.canvas_draw.itemconfigure('box',state='normal')

        myGlobals.canvas_draw.coords(
            'box',  #tag
            myGlobals.box_start_x*8*myGlobals.IMAGE_SCALE+myGlobals.BORDER_WIDTH,
            myGlobals.box_start_y*8*myGlobals.IMAGE_SCALE+myGlobals.BORDER_WIDTH,
            myGlobals.box_end_x*8*myGlobals.IMAGE_SCALE+myGlobals.BORDER_WIDTH,
            myGlobals.box_end_y*8*myGlobals.IMAGE_SCALE+myGlobals.BORDER_WIDTH
        )
    else :
        myGlobals.canvas_draw.itemconfigure('box',state='hidden')

        
    update_info()


def refresh_chars_image():
    myGlobals.canvas_chars.itemconfigure('my_chars', image=myGlobals.my_photo_chars)
    
    posx = myGlobals.charpicker_grid_posx*8*myGlobals.IMAGE_SCALE
    posy = myGlobals.charpicker_grid_posy*8*myGlobals.IMAGE_SCALE
    myGlobals.canvas_chars.coords(
        'chars_grid',
        posx, #x0
        posy,     #y0
        posx+8*myGlobals.IMAGE_SCALE,    #x1
        posy+8*myGlobals.IMAGE_SCALE #y1
    )
        

def create_chars_canvas_elements():
    #print('create_chars_canvas_elements()')
    #myGlobals.canvas_chars.delete("all")
    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_image.html
    myGlobals.canvas_chars.create_image(1, 1, image=myGlobals.my_photo_chars, anchor=tk.NW, tags='my_chars')

    #grid
    GRID_COLOR = '#00ff00'
    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_rectangle.html
    posx = myGlobals.charpicker_grid_posx*8*myGlobals.IMAGE_SCALE
    posy = myGlobals.charpicker_grid_posy*8*myGlobals.IMAGE_SCALE
    myGlobals.canvas_chars.create_rectangle(
        posx, #x0
        posy,     #y0
        posx+8*myGlobals.IMAGE_SCALE,    #x1
        posy+8*myGlobals.IMAGE_SCALE, #y1
        outline=GRID_COLOR,
        tags='chars_grid',
        width=2)



def save_some_data(
    filename,
    data
):
    print ('    Opening file "%s" for writing data (%d ($%04x) bytes)...' % (filename, len(data), len(data)))
    try:
        file_out = open(filename , 'wb')
    except IOError as err:
        print('I/O error: {0}'.format(err))
        return None
    file_out.write(bytearray(data))
    file_out.close()



def save_petscii_bin():
    tmp = []
    for i in myGlobals.data_char :
        tmp.append(i & 0b11111111)
    for i in myGlobals.data_color :
        tmp.append(i & 0b11111111)
    tmp.append(myGlobals.data_bg & 0b11111111)
    tmp.append(myGlobals.data_border & 0b11111111)
    save_some_data(myGlobals.petscii_bin_filename, tmp)
    #myGlobals.textvariable_filename.set(myGlobals.petscii_bin_filename)

def save_executable(filename):
    tmp = []
    for i in myGlobals.viewer_data :
        tmp.append(i & 0b11111111)
    for i in myGlobals.data_char :
        tmp.append(i & 0b11111111)
    for i in myGlobals.data_color :
        tmp.append(i & 0b11111111)
    tmp.append(myGlobals.data_bg & 0b11111111)
    tmp.append(myGlobals.data_border & 0b11111111)
    tmp.append(0)   # default: normal uppercase font
    save_some_data(filename, tmp)


def save_petscii_bin_petscii_editor():
    """
    PETSCII-Editor Format
    $3000-$33e7 chars
    $33e8 border color
    $33e9 bg color
    $33ea $d018 ($14 or $16)
    $3400-$37e7 colors
    """

    tmp = []
    tmp.append(0 & 0b11111111)
    tmp.append(0x30 & 0b11111111)
    for i in myGlobals.data_char :
        tmp.append(i & 0b11111111)
    tmp.append(myGlobals.data_border & 0b11111111)
    tmp.append(myGlobals.data_bg & 0b11111111)
    tmp.append(0x14 & 0b11111111)
    for i in range(0,21) :
        tmp.append(0)
    for i in myGlobals.data_color :
        tmp.append(i & 0b11111111)
    save_some_data(myGlobals.petscii_bin_filename, tmp)
    #myGlobals.textvariable_filename.set(myGlobals.petscii_bin_filename)



def load_some_data (
    filename
) :
    buffer=[]

	#open input file
    print ('    Opening file "%s" for reading...' % filename)
    try:
        file_in = open(filename , 'rb')
    except IOError as err:
        print('I/O error: {0}'.format(err))
        return buffer

    while True:
        data = file_in.read(1)  #read 1 byte
        if not data: break
        temp = struct.unpack('B',data)
        buffer.append(temp[0] & 0b11111111)

    return buffer


def bin2dec (
    data_bin
) :
    data_dec = []
    for i in range(7,-1,-1) :
        if (data_bin & (1 << i) > 0) :
            data_dec.append(1)  #white
        else :
            data_dec.append(0)  #black
    return data_dec



def load_charset(
) :    
    data = load_some_data(myGlobals.args.font_filename)
    
    if (len(data) != (256*8)) :
        print('ERROR: charset not 2048 bytes long!')
        return None

    myGlobals.data_charset = []
    for i in range(0,256) :
        c = i*8
        row = data[c:c+8]
        column = []
        for j in row :
            column.append(bin2dec(j))
        myGlobals.data_charset.append(column)

    """
    for i in myGlobals.data_charset[4]: 
        for j in i: 
            print('%s'%j,end='')
        print()
    """

    draw_charset_image()
    refresh_chars_image()

    draw_petscii_image_full()
    refresh_draw_image()



   

def update_info():
    myGlobals.textvariable_mode.set('%s' % myGlobals.mode)

    myGlobals.textvariable_info.set('pos %02d/%02d $%02x/$%02x | char %03d $%02x (%02d/%02d %03d)' % (
        myGlobals.mouse_posx, myGlobals.mouse_posy,
        myGlobals.mouse_posx, myGlobals.mouse_posy,
        myGlobals.selected_char,
        myGlobals.selected_char,
        myGlobals.charpicker_grid_posx,
        myGlobals.charpicker_grid_posy,
        myGlobals.charpicker_grid_posy * myGlobals.CHARPICKER_LAYOUT_HEIGHT + myGlobals.charpicker_grid_posx
    ))



def mouse_draw_Release3(event):
    myGlobals.box_selecting = False

def mouse_draw_Button3(event):
    myGlobals.box_selecting = True
    myGlobals.box_start_x = myGlobals.mouse_posx
    myGlobals.box_start_y = myGlobals.mouse_posy
    myGlobals.box_end_x = myGlobals.box_start_x
    myGlobals.box_end_y = myGlobals.box_start_y
    myGlobals.box_visible = True
    refresh_draw_image()    
    

def mouse_draw_Button1(event):
    """
    #a new position?
    if (
        (myGlobals.last_drawn_posx == myGlobals.mouse_posx) &
        (myGlobals.last_drawn_posy == myGlobals.mouse_posy)
    ) :
        return None
    """
    myGlobals.last_drawn_posx = myGlobals.mouse_posx
    myGlobals.last_drawn_posy = myGlobals.mouse_posy
    
    if (myGlobals.mode == 'pen') :
        undo_store()
        myGlobals.data_char[myGlobals.mouse_posy * myGlobals.CHAR_WIDTH +myGlobals.mouse_posx] = myGlobals.selected_char
        myGlobals.data_color[myGlobals.mouse_posy * myGlobals.CHAR_WIDTH +myGlobals.mouse_posx] = myGlobals.user_drawcolor.get()
        draw_petscii_image_single(
            myGlobals.mouse_posx,   #x
            myGlobals.mouse_posy,   #y
            myGlobals.data_char[myGlobals.mouse_posy * myGlobals.CHAR_WIDTH +myGlobals.mouse_posx],    #char
            myGlobals.data_color[myGlobals.mouse_posy * myGlobals.CHAR_WIDTH +myGlobals.mouse_posx]  #color
        )
        refresh_draw_image()
    if (myGlobals.mode == 'pencil') :
        undo_store()
        myGlobals.data_char[myGlobals.mouse_posy * myGlobals.CHAR_WIDTH +myGlobals.mouse_posx] = myGlobals.selected_char
        draw_petscii_image_single(
            myGlobals.mouse_posx,   #x
            myGlobals.mouse_posy,   #y
            myGlobals.data_char[myGlobals.mouse_posy * myGlobals.CHAR_WIDTH +myGlobals.mouse_posx],    #char
            myGlobals.data_color[myGlobals.mouse_posy * myGlobals.CHAR_WIDTH +myGlobals.mouse_posx]  #color
        )
        refresh_draw_image()
    if (myGlobals.mode == 'brush') :
        undo_store()
        myGlobals.data_color[myGlobals.mouse_posy * myGlobals.CHAR_WIDTH +myGlobals.mouse_posx] = myGlobals.user_drawcolor.get()
        draw_petscii_image_single(
            myGlobals.mouse_posx,   #x
            myGlobals.mouse_posy,   #y
            myGlobals.data_char[myGlobals.mouse_posy * myGlobals.CHAR_WIDTH +myGlobals.mouse_posx],    #char
            myGlobals.data_color[myGlobals.mouse_posy * myGlobals.CHAR_WIDTH +myGlobals.mouse_posx]  #color
        )
        refresh_draw_image()
    if (myGlobals.textvariable_mode.get() == 'set bg') :
        myGlobals.data_bg = myGlobals.user_drawcolor.get()
        myGlobals.image_is_saved = False
        draw_petscii_image_full()
        refresh_draw_image()
    if (myGlobals.textvariable_mode.get() == 'set border') :
        myGlobals.data_border = myGlobals.user_drawcolor.get()
        myGlobals.image_is_saved = False
        draw_petscii_image_full()
        refresh_draw_image(draw_border=True)



def mouse_draw_Motion(event):
    myGlobals.label_background_image.config(cursor = myGlobals.MOUSEPOINTER_NORMAL)
        
    myGlobals.mouse_posx = int(
        (
            (event.x/myGlobals.IMAGE_SCALE)
        )/8
    )-myGlobals.BORDER_SIZE
    myGlobals.mouse_posy = int(
        (
            (event.y/myGlobals.IMAGE_SCALE)
        )/8
    )-myGlobals.BORDER_SIZE
    
    #clip offsets
    if (myGlobals.mouse_posx < 0) : myGlobals.mouse_posx = 0
    if (myGlobals.mouse_posy < 0) : myGlobals.mouse_posy = 0
    if (myGlobals.mouse_posx > myGlobals.CHAR_WIDTH-1) : myGlobals.mouse_posx = myGlobals.CHAR_WIDTH-1
    if (myGlobals.mouse_posy > myGlobals.CHAR_HEIGHT-1) : myGlobals.mouse_posy = myGlobals.CHAR_HEIGHT-1
    
    #a new position?
    if (
        (myGlobals.last_posx == myGlobals.mouse_posx) &
        (myGlobals.last_posy == myGlobals.mouse_posy)
    ) :
        return None
    else :
        myGlobals.refresh_draw = True
        myGlobals.last_posx = myGlobals.mouse_posx
        myGlobals.last_posy = myGlobals.mouse_posy
        update_info()

    #selection box
    if (myGlobals.box_selecting) :
        myGlobals.box_end_x = myGlobals.mouse_posx+1
        myGlobals.box_end_y = myGlobals.mouse_posy+1
        refresh_draw_image()    


        

def mouse_draw_Button1Motion(event):
    mouse_draw_Motion(event)
    mouse_draw_Button1(event)
        

def mouse_charpicker_Button1(event):
    myGlobals.charpicker_grid_posx = int(event.x/myGlobals.IMAGE_SCALE/8)
    myGlobals.charpicker_grid_posy = int(event.y/myGlobals.IMAGE_SCALE/8)

    #print('selecting char at position %d/%d.'%(tmp_posx, tmp_posy))
    pos = myGlobals.charpicker_grid_posy * myGlobals.CHARPICKER_LAYOUT_WIDTH + myGlobals.charpicker_grid_posx
    myGlobals.selected_char = myGlobals.chars_layout[pos]
    
    #draw_charset_image()
    update_info()
    refresh_chars_image()
    
