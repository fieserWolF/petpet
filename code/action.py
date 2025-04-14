import code.myGlobals as myGlobals
import os
import struct
import tkinter as tk
import json


    
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


def load_petscii_json() :
    data = load_json(myGlobals.args.petscii_filename)
    myGlobals.show_grid = data['settings']['grid']
    myGlobals.data_bg = data['settings']['background']
    myGlobals.data_char = data['char']
    myGlobals.data_color = data['color']
    myGlobals.args.font_filename =  data['settings']['font']
    load_charset()
    myGlobals.textvariable_filename.set(myGlobals.args.petscii_filename)
    myGlobals.user_drawcolor.set(myGlobals.data_bg)
    draw_petscii_image()
    refresh_draw_image()
    update_info()


def load_petscii_bin() :
    data = load_some_data(myGlobals.args.petscii_bin_filename)
    myGlobals.show_grid = True
    myGlobals.data_char = data[0:1000]
    myGlobals.data_color = data[1000:2000]
    myGlobals.data_bg = data[2000] & 0b00001111
    
    for i in range(0,len(myGlobals.data_color)):
         myGlobals.data_color[i] = myGlobals.data_color[i] & 0b00001111
   
    myGlobals.textvariable_filename.set(myGlobals.args.petscii_bin_filename)
    myGlobals.user_drawcolor.set(myGlobals.data_bg)
    draw_petscii_image()
    refresh_draw_image()
    update_info()

"""
def load_petscii_bin_editor() :
    data = load_some_data(myGlobals.args.petscii_bin_filename)
    myGlobals.show_grid = True
    myGlobals.data_char = data[2:1002]
    myGlobals.data_color = data[1024+2:2024+2]
    myGlobals.data_bg = data[2002] & 0b00001111

    for i in range(0,len(myGlobals.data_color)):
         myGlobals.data_color[i] = myGlobals.data_color[i] & 0b00001111
    
    myGlobals.textvariable_filename.set(myGlobals.args.petscii_bin_filename)
    user_drawcolor.set(myGlobals.data_bg)
    draw_petscii_image()
    refresh_draw_image()
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
            'font' : myGlobals.args.font_filename
        },
        'char' : myGlobals.data_char,
        'color' : myGlobals.data_color
    }

    write_json(
        myGlobals.args.petscii_filename,
        my_data
    )


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
    json.dump(my_data, file_out, indent=4, ensure_ascii=False)
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



def draw_petscii_image_grid() :
    if (myGlobals.show_grid == False) :
        return None

    GRID_COLOR = '#aaaaaa'
    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_line.html
    for y in range(0,int(myGlobals.IMAGE_HEIGHT/8)) :
        myGlobals.canvas_draw.create_line(
            0, #x0
            y*8*myGlobals.IMAGE_SCALE,     #y0
            myGlobals.IMAGE_WIDTH*myGlobals.IMAGE_SCALE,    #x1
            y*8*myGlobals.IMAGE_SCALE, #y1
            fill=GRID_COLOR,
            tags='petscii_grid')
    for x in range(0,int(myGlobals.IMAGE_WIDTH/8)) :
        myGlobals.canvas_draw.create_line(
            x*8*myGlobals.IMAGE_SCALE, #x0
            0,     #y0
            x*8*myGlobals.IMAGE_SCALE,    #x1
            myGlobals.IMAGE_HEIGHT*myGlobals.IMAGE_SCALE, #y1
            fill=GRID_COLOR,
            tags='petscii_grid')


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


def draw_petscii_image() :
    #https://dafarry.github.io/tkinterbook/photoimage.htm
    #https://inf-schule.de/software/gui/entwicklung_tkinter/bilder
    #my_photo = tk.PhotoImage(file="image.ppm")
    
    CHAR_WIDTH = 8*myGlobals.IMAGE_SCALE
    CHAR_HEIGHT = 8*myGlobals.IMAGE_SCALE
    PANEL_WIDTH=myGlobals.CHAR_WIDTH*8*myGlobals.IMAGE_SCALE
    PANEL_HEIGHT=myGlobals.CHAR_HEIGHT*8*myGlobals.IMAGE_SCALE

    #background
    my_bytes = [255,100,100] * PANEL_HEIGHT * PANEL_WIDTH

    #draw chars
    char_number=0
    for y in range(0,myGlobals.CHAR_HEIGHT) :
        for x in range(0,myGlobals.CHAR_WIDTH) :
            my_data = draw_charset_image_single(myGlobals.data_char[char_number],myGlobals.data_color[char_number],myGlobals.data_bg)

            pos = (y*CHAR_HEIGHT*PANEL_WIDTH) + x*CHAR_WIDTH

            for yy in range(0,CHAR_HEIGHT) :
                for xx in range(0,CHAR_WIDTH) :
                    
                    pos_src = ( (yy*CHAR_WIDTH)+xx )*1
                    pos_dst = (pos + (yy*PANEL_WIDTH) + xx)*3
                   
                    my_bytes[pos_dst+0] = my_data[pos_src][0]
                    my_bytes[pos_dst+1] = my_data[pos_src][1]
                    my_bytes[pos_dst+2] = my_data[pos_src][2]
                    
            char_number+=1
    
    myGlobals.my_photo_draw = convert_to_photo_image(PANEL_WIDTH, PANEL_HEIGHT, my_bytes)



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
    update_info()
    
def draw(
):
    myGlobals.mode = 'draw'
    myGlobals.button_pen.configure(relief=tk.SUNKEN)
    myGlobals.button_brush.configure(relief=tk.RAISED)
    myGlobals.button_pencil.configure(relief=tk.RAISED)
    myGlobals.button_bg.configure(relief=tk.RAISED)
    update_info()


def toggle_grid(
):
    if (myGlobals.show_grid) :
        myGlobals.show_grid = False
    else :
        myGlobals.show_grid = True
    draw_petscii_image_grid()
    refresh_draw_image()


def brush(
):
    myGlobals.mode = 'brush'
    myGlobals.button_pen.configure(relief=tk.RAISED)
    myGlobals.button_brush.configure(relief=tk.SUNKEN)
    myGlobals.button_pencil.configure(relief=tk.RAISED)
    myGlobals.button_bg.configure(relief=tk.RAISED)
    update_info()

def pencil(
):
    myGlobals.mode = 'pencil'
    myGlobals.button_pen.configure(relief=tk.RAISED)
    myGlobals.button_brush.configure(relief=tk.RAISED)
    myGlobals.button_pencil.configure(relief=tk.SUNKEN)
    myGlobals.button_bg.configure(relief=tk.RAISED)
    update_info()


def clear_image():
    myGlobals.data_char = [32] * myGlobals.CHAR_HEIGHT * myGlobals.CHAR_WIDTH
    myGlobals.data_color = [1] * myGlobals.CHAR_HEIGHT * myGlobals.CHAR_WIDTH
    myGlobals.data_bg = 0
    myGlobals.user_drawcolor.set(1)
    draw_petscii_image()
    draw_petscii_image_grid()
    refresh_draw_image()
    

def refresh_draw_image():
    #print('refresh_chars_image()')
    #myGlobals.canvas_draw.delete("all")
    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_image.html
    myGlobals.canvas_draw.create_image(1, 1, image=myGlobals.my_photo_draw, anchor=tk.NW, tags='petscii_image')
    draw_petscii_image_grid()
    update_info()


def refresh_chars_image():
    #print('refresh_chars_image()')
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
    save_some_data(myGlobals.petscii_bin_filename, tmp)



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



   

def update_info():
    myGlobals.textvariable_mode.set('%s' % myGlobals.mode)
    
    tmp_posx = int(myGlobals.mouse_posx/myGlobals.IMAGE_SCALE/8)
    tmp_posy = int(myGlobals.mouse_posy/myGlobals.IMAGE_SCALE/8)

    myGlobals.textvariable_info.set('pos %02d/%02d $%02x/$%02x | char %03d $%02x' % (
        tmp_posx, tmp_posy,
        tmp_posx, tmp_posy,
        myGlobals.selected_char,
        myGlobals.selected_char
    ))



def mouseButton1_draw(event):
    if (myGlobals.textvariable_mode.get() == 'draw') :
        myGlobals.data_char[myGlobals.this_char_y * myGlobals.CHAR_WIDTH +myGlobals.this_char_x] = myGlobals.selected_char
        myGlobals.data_color[myGlobals.this_char_y * myGlobals.CHAR_WIDTH +myGlobals.this_char_x] = myGlobals.user_drawcolor.get()
    if (myGlobals.textvariable_mode.get() == 'pencil') :
        myGlobals.data_char[myGlobals.this_char_y * myGlobals.CHAR_WIDTH +myGlobals.this_char_x] = myGlobals.selected_char
    if (myGlobals.textvariable_mode.get() == 'brush') :
        myGlobals.data_color[myGlobals.this_char_y * myGlobals.CHAR_WIDTH +myGlobals.this_char_x] = myGlobals.user_drawcolor.get()
    if (myGlobals.textvariable_mode.get() == 'set bg') :
        myGlobals.data_bg = myGlobals.user_drawcolor.get()
    draw_petscii_image()
    refresh_draw_image()


def mouseMotion_draw(event):
    myGlobals.label_background_image.config(cursor = myGlobals.MOUSEPOINTER_NORMAL)
        
    myGlobals.mouse_posx = event.x
    myGlobals.mouse_posy = event.y
    if (
        (myGlobals.last_posx == myGlobals.mouse_posx) &
        (myGlobals.last_posy == myGlobals.mouse_posy)
    ) :
        return None

    myGlobals.last_posx = myGlobals.mouse_posx
    myGlobals.last_posy = myGlobals.mouse_posy
    update_info()

    myGlobals.this_char_x = int(myGlobals.mouse_posx/(8*myGlobals.IMAGE_SCALE))
    myGlobals.this_char_y = int(myGlobals.mouse_posy/(8*myGlobals.IMAGE_SCALE))
    if (
        (myGlobals.last_char_x == myGlobals.this_char_x) &
        (myGlobals.last_char_y == myGlobals.this_char_y)
    ) :
        return None
    
    myGlobals.last_char_x = myGlobals.this_char_x
    myGlobals.last_char_y = myGlobals.this_char_y
    #draw
    #myGlobals.data_char[myGlobals.this_char_y * myGlobals.CHAR_WIDTH +myGlobals.this_char_x] = myGlobals.selected_char
    #draw_petscii_image()
    #refresh_draw_image()
        

def mouseButton1_move_draw(event):
    mouseMotion_draw(event)
    mouseButton1_draw(event)
        

def mouseButton1_charpicker(event):
    myGlobals.charpicker_grid_posx = int(event.x/myGlobals.IMAGE_SCALE/8)
    myGlobals.charpicker_grid_posy = int(event.y/myGlobals.IMAGE_SCALE/8)

    #print('selecting char at position %d/%d.'%(tmp_posx, tmp_posy))
    myGlobals.selected_char = myGlobals.charpicker_grid_posy * myGlobals.CHARPICKER_LAYOUT_WIDTH + myGlobals.charpicker_grid_posx
    myGlobals.selected_char = myGlobals.chars_layout[myGlobals.selected_char]
    #draw_charset_image()
    update_info()
    refresh_chars_image()
    
