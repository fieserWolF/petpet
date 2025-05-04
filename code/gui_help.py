import code.myGlobals as myGlobals
import tkinter as tk


def show_window (
) :    
    TEXT_HEIGHT=30
    TEXT_WIDTH=80

    def close_window():
        info_window.destroy()

    def keyboard_up(event):
        msg.yview_scroll(-1,'units')

    def keyboard_down(event):
        msg.yview_scroll(1,'units')

    def keyboard_pageup(event):
        msg.yview_scroll(TEXT_HEIGHT,'units')

    def keyboard_pagedown(event):
        msg.yview_scroll(TEXT_HEIGHT*-1,'units')

    def keyboard_quit(event):
        info_window.destroy()


    
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
    msg.insert(tk.END, open(myGlobals.RES_DOC_HELP, encoding="utf_8").read())
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
    info_window.bind('<Escape>', keyboard_quit) 
    info_window.bind('<Control-q>', keyboard_quit) 
    info_window.bind('<Alt-q>', keyboard_quit) 


