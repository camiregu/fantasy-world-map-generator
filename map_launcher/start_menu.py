# camiregu
# 2023-apr-08
import file_manager
import map_launcher.settings_menu as settings

import tkinter as tk
from tkinter import ttk

class StartMenu(tk.Tk):
    def __init__(self) -> str:
        super().__init__()
        self.title('Map Selection')
        self.minsize(500, 300) # CONFIG
        self.frame_padding = 20 # CONFIG

        table_weights = {"columns": {0:1},
                        "rows": {0:5, 1:1}}
        configure_frame_table(self, table_weights)

        self.map_selector = MapSelector(self, padding=self.frame_padding)
        self.map_selector.grid(row=0, sticky='nesw')

        self.toolbar = Toolbar(self, padding=self.frame_padding)
        self.toolbar.grid(row=1, sticky='nesw')


    def refresh_map_list(self):
        self.map_selector.destroy()
        self.map_selector = MapSelector(self, padding=self.frame_padding)
        self.map_selector.grid(row=0, sticky='nesw')
        self.toolbar.set_button_state(False)


    def get_selection(self) -> str:
        return self.map_selector.tree.selection()[0]
    

    def select(self) -> str:
        self.mainloop()
        try:
            selection = self.get_selection()
            self.destroy()
            return selection
        except:
            quit()


class MapSelector(ttk.Frame):
    def __init__(self, master: tk.Tk, padding: int):
        super().__init__(master, padding=padding)

        table_weights = {"columns": {0:1},
                        "rows": {1:1}}
        configure_frame_table(self, table_weights)

        title = ttk.Label(self, text='Map List')
        title.grid(row=0, column=0)

        self.tree = ttk.Treeview(self, columns=[], displaycolumns='#all', height=5, selectmode='browse', show=['tree'])
        self.tree.grid(row=1, column=0, sticky='nesw')

        for row, map in enumerate(file_manager.get_map_names()):
            self.tree.insert('', row, iid=map, text=map)

        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky='ns')

        self.tree.configure(yscrollcommand=scrollbar.set)
        

class Toolbar(ttk.Frame):
    def __init__(self, master: StartMenu, padding: int):
        super().__init__(master, padding=padding)

        table_weights = {"columns": {0:1, 1:1, 2:1},
                        "rows": {0:1, 1:1}}
        configure_frame_table(self, table_weights)

        load_button = ttk.Button(self, text='Load Selected Map', command=self.master.quit, state='disabled')
        load_button.grid(column=0, row=0, columnspan=2, sticky='nesw')

        create_button = ttk.Button(self, text='Create New Map', command=self.create, state='disabled') 
        create_button.grid(column=2, row=0, columnspan=2, sticky='nesw')

        edit_button = ttk.Button(self, text='Edit', command=lambda: self.edit(self.master.get_selection()), state='disabled')
        edit_button.grid(column=0, row=1, sticky='nesw')

        delete_button = ttk.Button(self, text='Delete', command=lambda: self.delete(self.master.get_selection()), state='disabled')
        delete_button.grid(column=1, row=1, sticky='nesw')

        duplicate_button = ttk.Button(self, text='Duplicate Map', command=lambda: self.duplicate(self.master.get_selection()), state='disabled')
        duplicate_button.grid(column=2, row=1, columnspan=2, sticky='nesw')

        self.toggleable_buttons = [load_button, delete_button, duplicate_button]
        master.bind('<<TreeviewSelect>>', lambda _: self.set_button_state(True))
        master.bind('<Return>', lambda _: load_button.invoke())
        

    def set_button_state(self, active: bool):
        state = 'disabled'
        if active:
            state = '!' + state

        for button in self.toggleable_buttons:
            button.configure(state=state)


    def create(self):
        print(f'create new map!') #TODO
        #settings = settings.open()


    def edit(self, map_name: str):
        print(f'edit {map_name}') #TODO


    def delete(self, map_name: str): # TODO add an 'are you sure?'
        file_manager.delete_map(map_name)
        self.master.refresh_map_list()


    def duplicate(self, map_name: str):
        file_manager.duplicate_map(map_name)
        self.master.refresh_map_list()


def configure_frame_table(frame, weights: dict[str, dict]):
    columns, rows = weights.values()
    for column, weight in columns.items():
        frame.columnconfigure(column, weight=weight)
    for row, weight in rows.items():
        frame.rowconfigure(row, weight=weight)