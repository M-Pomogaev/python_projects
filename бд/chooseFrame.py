from tkinter import *
from tkinter import ttk

class ChooseFrame(ttk.Frame):
    def __init__(self, window, *args, **kwargs):
        super().__init__(window, *args, **kwargs)
        self.on_choose = None
        self.window = window
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(0, weight=1)
        self.tree_frame = ttk.Frame(self, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.tree = ttk.Treeview(self.tree_frame, show="headings",)
        self.tree.pack(expand=True, fill=BOTH)
        self.tree_frame.grid(row=0, column=0, sticky="nsew")
        self.choose_button = ttk.Button(self, text="Выбрать", command=self.choose)
        self.choose_button.grid(row=1, column=0, sticky="e")
        
    def set_columns(self, columns, headings, widths: dict = dict()):
        self.columns = ["№", *columns]
        self.headings = ["№", *headings]
        self.tree["columns"] = self.columns
        for col, head in zip(self.columns, self.headings):
            self.tree.heading(col, text=head, anchor="s")
        self.tree.column("№", width=40, stretch=False)
        for col, width in widths.items():
            self.tree.column(col, width=width, stretch=False)
        
    def set_on_choose(self, on_choose):
        self.on_choose = on_choose
    
    def set_selectmode(self, mode):
        self.tree.configure(selectmode=mode)
        
    def choose(self):
        selection = []
        for item in self.tree.selection():
            selection.append(self.info[self.tree.item(item)["values"][0]])
        self.window.destroy()
        if self.on_choose:
            self.on_choose(selection)
        
    def set_search_function(self, function, skip_first = True):
        self.skip_first = skip_first
        self.search_function = function
        
    def set_search_results(self):
        self.tree.delete(*self.tree.get_children())
        self.info = dict([(ind+1, info) for ind, info in enumerate(self.search_function())])
        if self.skip_first:
            first_position = 1
        else:
            first_position = 0
        for ind, order in self.info.items():
            self.tree.insert("", END, values=(ind, *order[first_position:]))