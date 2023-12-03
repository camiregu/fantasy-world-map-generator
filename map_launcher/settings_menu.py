# camiregu
# 2023-may-09

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import ImageTk, Image

# functions
def open():

    #terrain count
    global terrain_count
    terrain_count = 0

    # window creation and window settings
    window = tk.Toplevel()
    window.title('Map Settings')
    window.minsize(300, 200)
    window.grab_set()

    # frame creation and frame settings
    global terrain_list
    map_naming = ttk.Frame(window, padding=20)
    terrain_list = ttk.Frame(window, padding=20)
    terrain_buttons = ttk.Frame(window, padding=20)
    adjacency_bonuses = ttk.Frame(window, padding=20)
    map_creation = ttk.Frame(window, padding=20)

    map_naming.grid(row=0, sticky=('n','e','s','w'))
    terrain_list.grid(row=1, sticky=('n','e','s','w'))
    terrain_buttons.grid(row=2, sticky=('n','e','s','w'))
    adjacency_bonuses.grid(row=3, sticky=('n','e','s','w'))

    #terrain_list_scrollbar = ttk.Scrollbar(terrain_list, orient='vertical', command=terrain_list.yview)
    #terrain_list_scrollbar.grid(row=0, column=1, sticky=('n','s'))

    window.rowconfigure(1, weight=1)
    window.rowconfigure(3, weight=1)
    window.columnconfigure(0, weight=1)

    # map name entry box
    map_naming.columnconfigure(1, weight=1)
    ttk.Label(map_naming, text='Map Name:').grid(row=0, column=0)
    map_name = ttk.Entry(map_naming)
    map_name.grid(row=0, column=1)


    """# terrain list setup
    terrain_list.columnconfigure(1,weight=1)

    ttk.Label(terrain_list, text='Image').grid(row=0, column=0)
    ttk.Label(terrain_list, text='Terrain Name').grid(row=0, column=1)

    # add/remove terrain buttons
    add_terrain_button = ttk.Button(terrain_buttons, text='+', command=add_terrain)
    remove_terrain_button = ttk.Button(terrain_buttons, text='-', command=remove_terrain)

    add_terrain_button.grid(row=0, column=0, sticky=('n','e','s','w'))
    remove_terrain_button.grid(row=0, column=1, sticky=('n','e','s','w'))
    
    terrain_buttons.columnconfigure(0, weight=1)
    terrain_buttons.columnconfigure(1, weight=1)

    window.mainloop()"""
    
    #finish button
    map_creation.columnconfigure(0, weight=1)
    create_map_button = ttk.Button(map_creation, text='Create Map', command=create_map)

    try:
        #return necessary stuff
        return
    except:
        #cancel stuff that needs to be canceled
        return
    

def add_terrain():
    global terrain_count
    global terrain_list
    terrain_count += 1
    index = terrain_count

    open_button = ttk.Button(terrain_list, text='Open Image', command=lambda: open_image_file(open_button, index))
    entry_box = ttk.Entry(terrain_list)
    
    open_button.grid(row=terrain_count, column=0)
    entry_box.grid(row=terrain_count, column=1)


def remove_terrain():
    print("remove")


def open_image_file(button: ttk.Button, index: int):
    global terrain_list
    button.grid_forget()
    img_filename = fd.askopenfilename(filetypes=(('png files', '*.png'),))
    img = ImageTk.PhotoImage(Image.open(img_filename).resize((50,50)))
    label = ttk.Label(terrain_list, image=img)
    label.image = img
    label.grid(row=index, column=0)


def  create_map():
    pass