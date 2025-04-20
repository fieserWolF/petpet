import code.myGlobals as myGlobals
import code.action as action
import code.gui_info as gui_info
import tkinter as tk
#from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.filedialog as filedialog



def open_petscii_json():    
    ftypes = [('Image Files', '*.json')]
    user_filename_open = filedialog.askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    myGlobals.args.petscii_filename = user_filename_open
    action.load_petscii_json()


def open_font():    
    ftypes = [('Font Files', '*')]
    user_filename_open = filedialog.askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    myGlobals.args.font_filename = user_filename_open
    action.load_charset()


def open_petscii_bin():    
    ftypes = [('Image Files', '*.bin'),('Image Files', '*.pet'),('Image Files', '*.prg')]
    user_filename_open = filedialog.askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    myGlobals.args.petscii_bin_filename = user_filename_open
    action.load_petscii_bin()

def open_petscii_bin_petscii_editor():    
    ftypes = [('PETSCII Editor', '*.prg')]
    user_filename_open = filedialog.askopenfilename(filetypes = ftypes)
    if not user_filename_open : return None
    myGlobals.args.petscii_bin_filename = user_filename_open
    action.load_petscii_bin_petscii_editor()


def save_as_petscii_json():    
    ftypes = [('Image Files', '*.json')]
    user_filename_open = filedialog.asksaveasfilename(filetypes = ftypes)
    if not user_filename_open : return None
    myGlobals.args.petscii_filename = user_filename_open
    action.save_petscii_json()


def save_as_petscii_bin():    
    ftypes = [('Image Files', '*.bin')]
    user_filename_open = filedialog.asksaveasfilename(filetypes = ftypes)
    if not user_filename_open : return None
    myGlobals.petscii_bin_filename = user_filename_open
    action.save_petscii_bin()

def save_as_petscii_bin_petscii_editor():    
    ftypes = [('PETSCII Editor', '*.prg')]
    user_filename_open = filedialog.asksaveasfilename(filetypes = ftypes)
    if not user_filename_open : return None
    myGlobals.petscii_bin_filename = user_filename_open
    action.save_petscii_bin_petscii_editor()


def quit_application():
    if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):

        if (myGlobals.image_is_saved == False) :
            if tk.messagebox.askokcancel("Save", "Do you want to save?"):
                save_as_petscii_json()

        myGlobals.root.quit()



def clear_image_ask_user():
    if tk.messagebox.askokcancel("Are you sure?", "Do you want to clear the PETSCII?"): action.clear_image()


def create_drop_down_menu (
	root
) :
    menu = tk.Menu(root)
    root.config(menu=menu)

    filemenu = tk.Menu(menu)
    editmenu = tk.Menu(menu)
    infomenu = tk.Menu(menu)

    filemenu.add_command(label="open PETSCII", command=open_petscii_json, underline=0, accelerator="Alt+O")
    filemenu.add_command(label="save PETSCII", command=action.save_petscii_json, underline=0, accelerator="Alt+S")
    filemenu.add_command(label="save PETSCII as...", command=save_as_petscii_json, accelerator="Alt+Shift+S")
    filemenu.add_separator()
    filemenu.add_command(label="import PETSCII binary", command=open_petscii_bin)
    filemenu.add_command(label="export PETSCII binary", command=save_as_petscii_bin)
    filemenu.add_separator()
    filemenu.add_command(label="import PETSCII editor", command=open_petscii_bin_petscii_editor)
    filemenu.add_command(label="export PETSCII editor", command=save_as_petscii_bin_petscii_editor)
    filemenu.add_separator()
    filemenu.add_command(label="open font", command=open_font)
    filemenu.add_separator()
    filemenu.add_command(label="save config", command=action.save_config)
    filemenu.add_separator()
    filemenu.add_command(label="quit", command=quit_application, underline=0, accelerator="Alt+Q")

    editmenu.add_command(label="undo", command=action.undo_restore, accelerator="Ctrl+z")
    editmenu.add_separator()
    editmenu.add_command(label="copy", command=action.copy, accelerator="Ctrl+c")
    editmenu.add_command(label="paste", command=action.paste, accelerator="Ctrl+v")
    editmenu.add_command(label="cut", command=action.cut, accelerator="Ctrl+x")
    editmenu.add_separator()
    editmenu.add_command(label="clear PETSCII", command=clear_image_ask_user)
    editmenu.add_separator()
    editmenu.add_command(label="toggle grid", command=action.toggle_grid, underline=7, accelerator="Alt+g")

    infomenu.add_command(label="help", command=gui_info.show_info_window, underline=0, accelerator="f1")

    #add all menus
    menu.add_cascade(label="file", menu=filemenu, underline=0, accelerator="Alt+f")
    menu.add_cascade(label="edit", menu=editmenu, underline=0, accelerator="Alt+e")
    menu.add_cascade(label="info", menu=infomenu, underline=0, accelerator="Alt+i")







def create_image_draw (
	root,
    _row,
    _column
) :
    #writes label_background_image
    
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals.FRAME_BORDER,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )

    myGlobals.canvas_draw = tk.Canvas(root, width=myGlobals.FULL_SCREEN_WIDTH, height=myGlobals.FULL_SCREEN_HEIGHT, background="#000000")

    myGlobals.canvas_draw.delete("all")
    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_rectangle.html
    myGlobals.canvas_draw.create_rectangle(0, 0, myGlobals.FULL_SCREEN_WIDTH, myGlobals.FULL_SCREEN_HEIGHT, fill='#000000', tags='border')
    
    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_image.html
    myGlobals.canvas_draw.create_image(myGlobals.BORDER_WIDTH, myGlobals.BORDER_WIDTH, image=myGlobals.my_photo_draw, anchor=tk.NW, tags='petscii_image')

    action.create_draw_canvas_elements()

    myGlobals.canvas_draw.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E
    )
    
    myGlobals.canvas_draw.bind('<Motion>', action.mouse_draw_Motion)
    myGlobals.canvas_draw.bind('<Button-1>', action.mouse_draw_Button1)
    myGlobals.canvas_draw.bind('<B1-Motion>', action.mouse_draw_Button1Motion)
    #myGlobals.canvas_draw.bind('<Button>', action.mouse_draw_Button1)
    myGlobals.canvas_draw.bind('<ButtonPress-3>', action.mouse_draw_Button3)
    myGlobals.canvas_draw.bind('<ButtonRelease-3>', action.mouse_draw_Release3)




def create_image_chars (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals.FRAME_BORDER,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    
    myGlobals.canvas_chars = tk.Canvas(frame_border, width=myGlobals.CHARS_IMAGE_WIDTH*myGlobals.IMAGE_SCALE, height=myGlobals.CHARS_IMAGE_HEIGHT*myGlobals.IMAGE_SCALE, background="#000000")

    #myGlobals.canvas_chars.delete("all")
    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_image.html
    #myGlobals.canvas_chars.create_image(1, 1, image=myGlobals.my_photo_chars, anchor=tk.NW, tags='my_chars')

    action.create_chars_canvas_elements()

    myGlobals.canvas_chars.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E
    )
    
    #myGlobals.canvas_chars.bind('<Motion>', action.mouseMotion_charpicker)
    myGlobals.canvas_chars.bind('<Button-1>', action.mouse_charpicker_Button1)
    #myGlobals.canvas_chars.bind('<Button-3>', mouseButton3_chars)




def create_toolbox (
	root,
    _row,
    _column
) :
    #writes button_play, button_forward, button_backward

    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals.FRAME_BORDER,
    )
    frame_border.grid(
        row=_row,
        column=_column,
        sticky=tk.W
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR_LIGHT,
        bd=1,
        padx = myGlobals.FRAME,
        pady = myGlobals.FRAME_PADY,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
 
    
    MODES = [
            ('pen', myGlobals.GFX_DRAW, 0, 0,0, action.draw),
            ('brush', myGlobals.GFX_BRUSH, 0, 1,0, action.brush),
            ('pencil', myGlobals.GFX_PENCIL, 0, 2,0, action.pencil),
            ('bg', myGlobals.GFX_BG, 0, 3,0, action.change_bg),
            ('border', myGlobals.GFX_BORDER, 0, 4,0, action.change_border),
    ]
    
    for text, my_image, my_underline, my_row, my_column, my_command in MODES:
        my_button = tk.Button(
            frame_inner,
            bitmap='@'+my_image,
            bg = myGlobals.BGCOLOR_LIGHT,
            text = text,
            command = my_command,
            cursor = myGlobals.MOUSEPOINTER_HAND,
            underline = my_underline,
            relief=tk.RAISED
        )
        if (text == 'pen') : myGlobals.button_pen = my_button
        if (text == 'brush') : myGlobals.button_brush = my_button
        if (text == 'pencil') : myGlobals.button_pencil = my_button
        if (text == 'bg') : myGlobals.button_bg = my_button
        if (text == 'border') : myGlobals.button_border = my_button

        myGlobals.button_pen.configure(relief=tk.SUNKEN)

        #placement in grid layout
        my_button.grid(
            row= my_row,
            column= my_column,
            sticky=tk.W
        )



def create_infobox (
    root,
    my_row,
    my_column,
    my_text,
    my_textvariable,
    my_width
) :
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals.FRAME,
        pady = myGlobals.FRAME_PADY
        )

    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR_LIGHT,
        bd=1,
        padx = myGlobals.FRAME,
        pady = myGlobals.FRAME_PADY,
        relief=tk.RAISED
        )

    label_info = tk.Label(
		frame_inner,
        bg=myGlobals.BGCOLOR2,
		text = my_text,
        bd=1,
        fg="#000000"
	)

    label_content = tk.Label(
		frame_inner,
        bg=myGlobals.BGCOLOR_LIGHT,
		textvariable = my_textvariable,
        bd=1,
        width=my_width,
        fg="#000000"
	)


    # layout
    frame_border.grid(
        row=my_row,
        column=my_column,
        sticky=tk.W
    )

    frame_inner.grid(
        row=0,
        column=0,
        sticky=tk.W
    )

    label_info.grid(
        row=0,
        column=0,
        sticky=tk.W
    )

    label_content.grid(
        row=0,
        column=1,
        sticky=tk.W
    )



def create_top (
        root,
        _row,
        _column
) :    
    #frame border
    frame_border = tk.Frame(
        root,
        bd=1,
        bg=myGlobals.BGCOLOR,
    )
    frame_border.grid(
        row=_row,
        column=_column,
        sticky=tk.W+tk.E
    )
    frame_border.grid_columnconfigure(0, weight=1)
    frame_border.grid_rowconfigure(0, weight=1)


    #frame left
    frame_left = tk.Frame(
        frame_border,
        bd=1,
        bg=myGlobals.BGCOLOR,
    )
    frame_left.grid(
        row=0,
        column=0,
        sticky=tk.W
    )
    frame_left.grid_columnconfigure(0, weight=1)
    frame_left.grid_rowconfigure(0, weight=1)


    #frame right
    frame_right = tk.Frame(
        frame_border,
        bd=1,
        bg=myGlobals.BGCOLOR,
    )
    frame_right.grid(
        row=0,
        column=1,
        sticky=tk.W
    )
    frame_right.grid_columnconfigure(0, weight=1)
    frame_right.grid_rowconfigure(0, weight=1)

    #create elements
    create_infobox (
        frame_left,   #root frame
        0,  #row
        0,  #column
        'file:',    #text
        myGlobals.textvariable_filename,   #textvariable
        0   #text width
    )



def create_middle (
        root,
        _row,
        _column
) :    
    #frame border
    frame_border = tk.Frame(
        root,
        bd=1,
        bg=myGlobals.BGCOLOR,
    )
    frame_border.grid(
        row=_row,
        column=_column,
        sticky=tk.W+tk.E
    )
    frame_border.grid_columnconfigure(0, weight=1)
    frame_border.grid_rowconfigure(0, weight=1)


    #frame left
    frame_left = tk.Frame(
        frame_border,
        bd=1,
        bg=myGlobals.BGCOLOR,
    )
    frame_left.grid(
        row=0,
        column=0,
        sticky=tk.W
    )
    frame_left.grid_columnconfigure(0, weight=1)
    frame_left.grid_rowconfigure(0, weight=1)


    #frame middle
    frame_middle = tk.Frame(
        frame_border,
        bd=1,
        bg=myGlobals.BGCOLOR,
    )
    frame_middle.grid(
        row=0,
        column=1,
        sticky=tk.W
    )
    frame_middle.grid_columnconfigure(0, weight=1)
    frame_middle.grid_rowconfigure(0, weight=1)


    #frame right
    frame_right = tk.Frame(
        frame_border,
        bd=1,
        bg=myGlobals.BGCOLOR,
    )
    frame_right.grid(
        row=0,
        column=2,
        sticky=tk.W
    )
    frame_right.grid_columnconfigure(0, weight=1)
    frame_right.grid_rowconfigure(0, weight=1)



    #create elements
    create_toolbox(
        frame_left,
        0,  #row
        0   #column
    )

    create_image_draw(
        frame_middle,
        0,  #row
        0   #column
    )

    create_colorpicker(
        frame_right,
        0,  #row
        0   #column
    )

    create_image_chars(
        frame_right,
        1,  #row
        0   #column
    )
    



def create_bottom (
        root,
        _row,
        _column
) :    
    #frame border
    frame_border = tk.Frame(
        root,
        bd=1,
        bg=myGlobals.BGCOLOR,
    )
    frame_border.grid(
        row=_row,
        column=_column,
        sticky=tk.W+tk.E
    )
    frame_border.grid_columnconfigure(0, weight=1)
    frame_border.grid_rowconfigure(0, weight=1)

    #frame left
    frame_left = tk.Frame(
        frame_border,
        bd=1,
        bg=myGlobals.BGCOLOR,
    )
    frame_left.grid(
        row=0,
        column=0,
        sticky=tk.W
    )
    frame_left.grid_columnconfigure(0, weight=1)
    frame_left.grid_rowconfigure(0, weight=1)

    #create elements
    create_infobox (
        frame_left,   #root frame
        0,  #row
        0,  #column
        'mode:',    #text
        myGlobals.textvariable_mode,   #textvariable
        0   #text width
    )

    create_infobox (
        frame_left,   #root frame
        0,  #row
        1,  #column
        'info:',    #text
        myGlobals.textvariable_info,   #textvariable
        30   #text width
    )





def create_colorpicker (
	root,
    _row,
    _column
) :
    #frame border
    frame_border = tk.Frame(
        root,
        bd=myGlobals.FRAME_BORDER,
        bg=myGlobals.BGCOLOR
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    
    #frame inner
    frame_inner = tk.Frame(
        frame_border,
        bd=1,
        bg=myGlobals.BGCOLOR,
        padx = myGlobals.FRAME,
        pady = myGlobals.FRAME_PADY,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    #labels
    _row = 0
    label = tk.Label(
        frame_inner,
        text="color",
        anchor="c",
        justify='left',
        bg=myGlobals.BGCOLOR,
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=1,
        sticky=tk.W+tk.E,
        columnspan=8
    )

    MODES = [
            ("black", 		 0, 0,0),	#text,value,row,column
            ("white",		 1, 0,1),
            ("red",			 2, 0,2),
            ("cyan",		 3, 0,3),
            ("purple",		 4, 0,4),
            ("green",		 5, 0,5),
            ("blue",		 6, 0,6),
            ("yellow",		 7, 0,7),
            ("orange",		 8, 1,0),
            ("brown",		 9, 1,1),
            ("light red",	10, 1,2),
            ("dark gray",	11, 1,3),
            ("gray", 		12, 1,4),
            ("light green",	13, 1,5),
            ("light blue",	14, 1,6),
            ("light gray",	15, 1,7),
    ]
    

    for text, value, my_row, my_column in MODES:
        mycolor = '#%02x%02x%02x' % (
            myGlobals.palette[value][0],
            myGlobals.palette[value][1],
            myGlobals.palette[value][2]
        )
        
        radiobutton_user_value = tk.Radiobutton(
            frame_inner,
            value = value,
            width=2,
            indicatoron=0,
            variable=myGlobals.user_drawcolor,
            background=mycolor,
            activebackground=mycolor,
            selectcolor=mycolor,
            cursor=myGlobals.MOUSEPOINTER_HAND,
            bd=4,
            relief=tk.GROOVE,
            offrelief=tk.RAISED,
            #command=action_debug
        )
        radiobutton_user_value.grid(
            row=2+my_row,
            column=my_column,
            sticky=tk.W+tk.E
        )
