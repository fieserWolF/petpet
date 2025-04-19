import code.myGlobals as myGlobals
import code.gui as gui
import code.action as action
import code.gui_info as gui_info
import sys

import tkinter as tk
import argparse




def _main_procedure() :
    #writes args
    
    print('%s v%s [%s] *** by fieserWolF' % (myGlobals.PROGNAME, myGlobals.VERSION, myGlobals.LAST_EDITED))

    #https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(
        description='This is a PETSCII editor. Press F1 for help in the program.',
        epilog='Example: '+sys.argv[0]+' -p gfx.json -c config.json -f font.bin'
    )
    parser.add_argument('-p', '--petscii_file', dest='petscii_filename', help='petscii filename (.json)')
    parser.add_argument('-c', '--config_file', dest='config_filename', help='name of configuration file (.json)', default='./resources/config.json')
    parser.add_argument('-f', '--font_file', dest='font_filename', help='name of font (2048 bytes)', default='./resources/charrom_uppercase.bin')
    myGlobals.args = parser.parse_args()

    #action.save_config()
    #return None

    action.load_config()

    action.load_charset()
    if (myGlobals.args.petscii_filename) :
        action.load_petscii_json()
    else :
        myGlobals.args.petscii_filename = 'image.json'
        myGlobals.textvariable_filename.set(myGlobals.args.petscii_filename)
        action.clear_image()


    
    #main procedure
    title_string = myGlobals.PROGNAME+' v'+myGlobals.VERSION+' ['+myGlobals.LAST_EDITED+'] *** by fieserWolF'
    myGlobals.root.title(title_string)
    gui.create_drop_down_menu(myGlobals.root)

    myGlobals.root.configure(
        background=myGlobals.BGCOLOR
    )

    gui.create_top(
        myGlobals.root,
        0,  #row
        0   #column
    )
    gui.create_middle(
        myGlobals.root,
        1,  #row
        0   #column
    )
    gui.create_bottom(
        myGlobals.root,
        2,  #row
        0   #column
    )

    action.draw_charset_image()
    action.refresh_chars_image()
    action.draw_petscii_image_full()
    action.refresh_draw_image(draw_border=True)
    

           
    myGlobals.root.bind_all('<Alt-q>', lambda event: gui.quit_application())
    myGlobals.root.bind_all('<F1>', lambda event: gui_info.show_info_window())
    myGlobals.root.bind_all('<Alt-o>', lambda event: gui.open_petscii_json())
    myGlobals.root.bind_all('<Alt-s>', lambda event: action.save_petscii_json())
    myGlobals.root.bind_all('<Control-s>', lambda event: action.save_petscii_json())
    myGlobals.root.bind_all('<Alt-e>', lambda event: gui.save_as_petscii_bin())
    myGlobals.root.bind_all('<Alt-g>', lambda event: action.toggle_grid())
    myGlobals.root.bind_all('<Control-z>', lambda event: action.undo_restore())
    myGlobals.root.bind_all('<Control-c>', lambda event: action.copy())
    myGlobals.root.bind_all('<Control-v>', lambda event: action.paste())
    myGlobals.root.bind_all('<Control-x>', lambda event: action.cut())

    myGlobals.root.protocol('WM_DELETE_WINDOW', gui.quit_application)
   
    tk.mainloop()
