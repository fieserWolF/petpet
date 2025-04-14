import code.myGlobals as myGlobals
import tkinter as tk


def show_info_window (
) :
    message = \
        'main control\n' \
        '------------\n' \
        'Left-mousebutton: draw\n' \
        '<Alt-q>: quit\n' \
        '<Alt-o>: open PETSCII (json)\n' \
        '<Alt-s>: save PETSCII (json)\n' \
        '<Alt-e>: export PETSCII (bin)\n' \
        '<Alt-g>: toggle grid\n' \
        '\n' \
        'export binary format\n' \
        '------------\n' \
        '1000 bytes characters\n' \
        '1000 bytes colors\n' \
        '1 byte background color\n' \
        '\n' \
    
    
    TEXT_HEIGHT=20
    TEXT_WIDTH=40

    def close_window():
        global info_window
        global info_window_open
        
        if (info_window_open == True) :
            info_window.destroy()
            info_window_open = False

    def close_window_key(self):
        close_window()

    def keyboard_up(event):
        msg.yview_scroll(-1,'units')

    def keyboard_down(event):
        msg.yview_scroll(1,'units')

    def keyboard_pageup(event):
        msg.yview_scroll(TEXT_HEIGHT,'units')

    def keyboard_pagedown(event):
        msg.yview_scroll(TEXT_HEIGHT*-1,'units')


    
	#http://effbot.org/tkinterbook/toplevel.htm
    info_window = tk.Toplevel(
        bd=10
    )
    info_window.title('Help')
    info_window.configure(background=myGlobals.BGCOLOR)

    frame_left = tk.Frame( info_window)
    frame_right = tk.Frame( info_window)

    #http://effbot.org/tkinterbook/message.htm
    #text
    msg = tk.Text(
        frame_right,
#        bd=10,
        relief=tk.FLAT,
        width=TEXT_WIDTH,
        height=TEXT_HEIGHT
    )

    #scrollbar
    msg_scrollBar = tk.Scrollbar(
        frame_right,
        bg=myGlobals.BGCOLOR
    )
    msg_scrollBar.config(command=msg.yview)
    msg.insert(tk.END, message)
    msg.config(yscrollcommand=msg_scrollBar.set)
    msg.config(state=tk.DISABLED)

    FRAME_PADX = 10
    FRAME_PADY = 10

    #button
    button = tk.Button(
        frame_left,
        bg=myGlobals.BGCOLOR,
        text='OK',
        command=info_window.destroy,
        padx=FRAME_PADX,
        pady=FRAME_PADY
    )




    #placement in grid
    frame_left.grid(
        row=0,
        column=0,
        sticky=tk.W
    )
    frame_right.grid(
        row=0,
        column=1,
        sticky=tk.W
    )
    
    button.grid(
        row=1,
        column=0,
        sticky=tk.W+tk.E
    )

    msg.grid(
        row=0,
        column=0,
        sticky=tk.W
    )
    msg_scrollBar.grid(
        row=0,
        column=1,
        sticky=tk.N+tk.S
    )

    info_window.bind('<Up>', keyboard_up) 
    info_window.bind('<Down>', keyboard_down) 
    info_window.bind('<Next>', keyboard_pageup) 
    info_window.bind('<Prior>', keyboard_pagedown) 


