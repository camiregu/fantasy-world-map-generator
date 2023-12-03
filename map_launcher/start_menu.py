# camiregu
# 2023-apr-08
import map_launcher.file_manager as file_manager
import map_launcher.settings_menu as settings

import tkinter as tk
from tkinter import ttk

# functions
def start_menu():
    map_list = file_manager.get_map_names()

    window = tk.Tk()
    window.title('Map Selection')
    window.minsize(500,300)
    window.columnconfigure(0,weight=1)
    window.rowconfigure(0,weight=5)
    window.rowconfigure(1,weight=1)

    tree_frame = ttk.Frame(window, padding=20)
    button_frame = ttk.Frame(window, padding=20)
    
    tree_frame.grid(row=0, sticky=('n','e','s','w'))
    tree_frame.columnconfigure(0, weight=1)
    tree_frame.rowconfigure(1, weight=1)
    button_frame.grid(row=1, sticky=('n','e','s','w'))
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1, pad=10)
    button_frame.columnconfigure(2, weight=1)
    button_frame.rowconfigure(0, weight=1)
    button_frame.rowconfigure(1, weight=1)

    tree_label = ttk.Label(tree_frame, text='Map List')
    tree_label.grid(row=0, column=0)
    tree_view = ttk.Treeview(tree_frame, columns=[], displaycolumns='#all', height=5, selectmode='browse', show=['tree'])
    tree_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree_view.yview)
    tree_scrollbar.grid(row=1, column=1, sticky=('n','s'))
    tree_view.configure(yscrollcommand=tree_scrollbar.set)
    tree_view.grid(row=1, column=0, sticky=('n','e','s','w'))

    load_button = ttk.Button(button_frame, text='Load Selected Map', command=window.quit, state='disabled')
    create_button = ttk.Button(button_frame, text='Create New Map', command=create) 
    edit_button = ttk.Button(button_frame, text='Edit', command=lambda: edit(tree_view.selection()[0]), state='disabled')
    delete_button = ttk.Button(button_frame, text='Delete', command=lambda: delete(tree_view.selection()[0]), state='disabled')
    duplicate_button = ttk.Button(button_frame, text='Duplicate Map', command=lambda: duplicate(tree_view.selection()[0]), state='disabled')
    
    load_button.grid(column=0, row=0, columnspan=2, sticky=('n','e','s','w'))
    create_button.grid(column=2, row=0, columnspan=2, sticky=('n','e','s','w'))
    edit_button.grid(column=0, row=1, sticky=('n','e','s','w'))
    delete_button.grid(column=1, row=1, sticky=('n','e','s','w'))
    duplicate_button.grid(column=2, row=1, columnspan=2, sticky=('n','e','s','w'))

    for index, world in enumerate(map_list):
        tree_view.insert('', index, iid=world, text=world)

    window.bind('<<TreeviewSelect>>', lambda _: activate_buttons([load_button, edit_button, delete_button, duplicate_button]))
    window.bind('<Return>', lambda _: load_button.invoke())

    window.mainloop()
    
    try:
        selected_world = tree_view.selection()[0]
        window.destroy()
        return selected_world
    except:
        quit()


def activate_buttons(buttons: list[ttk.Button]):
    for button in buttons:
        button.configure(state='!disabled')


def create():
    print(f'create new world!')
    #settings = settings.open()


def edit(world: str):
    print(f'edit {world}') #TODO


def delete(world: str):
    print(f'delete {world}') #TODO


def duplicate(world: str):
    print(f'duplicate {world}') #TODO