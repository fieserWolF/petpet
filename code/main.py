import code.myGlobals as myGlobals
import code.gui as gui
import code.action as action
import code.gui_help as gui_help
import code.gui_about as gui_about
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
    myGlobals.root.bind_all('<F1>', lambda event: gui_help.show_window())
    myGlobals.root.bind_all('<Alt-o>', lambda event: gui.open_petscii_json())
    myGlobals.root.bind_all('<Alt-s>', lambda event: action.save_petscii_json())
    myGlobals.root.bind_all('<Control-s>', lambda event: action.save_petscii_json())
    myGlobals.root.bind_all('<Alt-S>', lambda event: gui.save_as_petscii_json())
    myGlobals.root.bind_all('<Alt-g>', lambda event: action.select_toggle_grid())
    myGlobals.root.bind_all('<Control-z>', lambda event: action.undo_restore())
    myGlobals.root.bind_all('<Control-c>', lambda event: action.copy())
    myGlobals.root.bind_all('<Control-v>', lambda event: action.paste())
    myGlobals.root.bind_all('<Control-x>', lambda event: action.cut())

    myGlobals.root.bind('@', lambda event: action.userwrite_letter('@'))
    myGlobals.root.bind('a', lambda event: action.userwrite_letter('a'))
    myGlobals.root.bind('b', lambda event: action.userwrite_letter('b'))
    myGlobals.root.bind('c', lambda event: action.userwrite_letter('c'))
    myGlobals.root.bind('d', lambda event: action.userwrite_letter('d'))
    myGlobals.root.bind('e', lambda event: action.userwrite_letter('e'))
    myGlobals.root.bind('f', lambda event: action.userwrite_letter('f'))
    myGlobals.root.bind('g', lambda event: action.userwrite_letter('g'))
    myGlobals.root.bind('h', lambda event: action.userwrite_letter('h'))
    myGlobals.root.bind('i', lambda event: action.userwrite_letter('i'))
    myGlobals.root.bind('j', lambda event: action.userwrite_letter('j'))
    myGlobals.root.bind('k', lambda event: action.userwrite_letter('k'))
    myGlobals.root.bind('l', lambda event: action.userwrite_letter('l'))
    myGlobals.root.bind('m', lambda event: action.userwrite_letter('m'))
    myGlobals.root.bind('n', lambda event: action.userwrite_letter('n'))
    myGlobals.root.bind('o', lambda event: action.userwrite_letter('o'))
    myGlobals.root.bind('p', lambda event: action.userwrite_letter('p'))
    myGlobals.root.bind('q', lambda event: action.userwrite_letter('q'))
    myGlobals.root.bind('r', lambda event: action.userwrite_letter('r'))
    myGlobals.root.bind('s', lambda event: action.userwrite_letter('s'))
    myGlobals.root.bind('t', lambda event: action.userwrite_letter('t'))
    myGlobals.root.bind('u', lambda event: action.userwrite_letter('u'))
    myGlobals.root.bind('v', lambda event: action.userwrite_letter('v'))
    myGlobals.root.bind('w', lambda event: action.userwrite_letter('w'))
    myGlobals.root.bind('x', lambda event: action.userwrite_letter('x'))
    myGlobals.root.bind('y', lambda event: action.userwrite_letter('y'))
    myGlobals.root.bind('z', lambda event: action.userwrite_letter('z'))

    myGlobals.root.bind('[', lambda event: action.userwrite_letter('['))
    myGlobals.root.bind(']', lambda event: action.userwrite_letter(']'))
    myGlobals.root.bind('<space>', lambda event: action.userwrite_letter(' '))
    myGlobals.root.bind('!', lambda event: action.userwrite_letter('!'))
    myGlobals.root.bind('"', lambda event: action.userwrite_letter('"'))
    myGlobals.root.bind('#', lambda event: action.userwrite_letter('#'))
    myGlobals.root.bind('$', lambda event: action.userwrite_letter('$'))
    myGlobals.root.bind('%', lambda event: action.userwrite_letter('%'))
    myGlobals.root.bind('&', lambda event: action.userwrite_letter('&'))
    myGlobals.root.bind("'", lambda event: action.userwrite_letter("'"))
    myGlobals.root.bind('(', lambda event: action.userwrite_letter('('))
    myGlobals.root.bind(')', lambda event: action.userwrite_letter(')'))
    myGlobals.root.bind('*', lambda event: action.userwrite_letter('*'))
    myGlobals.root.bind('+', lambda event: action.userwrite_letter('+'))
    myGlobals.root.bind(',', lambda event: action.userwrite_letter(','))
    myGlobals.root.bind('-', lambda event: action.userwrite_letter('-'))
    myGlobals.root.bind('.', lambda event: action.userwrite_letter('.'))
    myGlobals.root.bind('/', lambda event: action.userwrite_letter('/'))
    myGlobals.root.bind('0', lambda event: action.userwrite_letter('0'))
    myGlobals.root.bind('1', lambda event: action.userwrite_letter('1'))
    myGlobals.root.bind('2', lambda event: action.userwrite_letter('2'))
    myGlobals.root.bind('3', lambda event: action.userwrite_letter('3'))
    myGlobals.root.bind('4', lambda event: action.userwrite_letter('4'))
    myGlobals.root.bind('5', lambda event: action.userwrite_letter('5'))
    myGlobals.root.bind('6', lambda event: action.userwrite_letter('6'))
    myGlobals.root.bind('7', lambda event: action.userwrite_letter('7'))
    myGlobals.root.bind('8', lambda event: action.userwrite_letter('8'))
    myGlobals.root.bind('9', lambda event: action.userwrite_letter('9'))
    myGlobals.root.bind(';', lambda event: action.userwrite_letter(';'))
    myGlobals.root.bind(':', lambda event: action.userwrite_letter(':'))
    myGlobals.root.bind('<less>', lambda event: action.userwrite_letter('<'))
    myGlobals.root.bind('=', lambda event: action.userwrite_letter('='))
    myGlobals.root.bind('<greater>', lambda event: action.userwrite_letter('>'))
    myGlobals.root.bind('?', lambda event: action.userwrite_letter('?'))

    myGlobals.root.protocol('WM_DELETE_WINDOW', gui.quit_application)
   
    tk.mainloop()
