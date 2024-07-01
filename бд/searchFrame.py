from tkinter import *
from tkinter import ttk

class SearchFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.columnconfigure(0, weight=1)
        self.search_frame = ttk.Frame(self, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.search_frame.rowconfigure(0, weight=0)
        self.search_frame.rowconfigure(1, weight=0)
        self.search_frame.columnconfigure(0, weight=0)
        self.search_frame.columnconfigure(1, weight=1)
        self.search_frame.grid(row=0, column=0, sticky="nsew")
        self.count_label = ttk.Label(self.search_frame)
        self.count_label.grid(row=1, column=0, sticky="w")
        self.search_label = ttk.Label(self.search_frame, text="Поиск: ")
        self.search_label.grid(row=0, column=0, sticky="w")
        self.search_str = StringVar(self)
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_str)
        self.search_entry.grid(row=0, column=1, sticky="w")
        self.search_category_label = ttk.Label(self.search_frame)
        self.search_category_label.grid(row=1, column=1, sticky="E", ipadx=10)
        self.search_buttons = dict()
        
        self.tree = ttk.Treeview(self, show="headings", selectmode="extended")
        self.tree.grid(row=1, column=0, sticky="nsew")
        
        self.buttons_frame = ttk.Frame(self, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.buttons_frame.grid(row=2, column=0, sticky="nsew")
        self.buttons = dict()
        
        self.search_func = None
        self.default_category = None
        self.search_str.trace_add("write", self.set_search_results)
            
    def set_font(self, font_):
        for button in self.buttons.values():
            button.config(font=font_)
    
    def search_button_onclick(self, name, comand):
        self.search_category_label.config(text=name)
        comand()
            
    def set_button_onclick(self, name, comand):
        if name in self.buttons:
            self.buttons[name].config(command=comand)
        if name in self.search_buttons:
            self.search_buttons[name].config(command=lambda: self.search_button_onclick(name, comand))
        
    def set_buttons_frame(self, buttons_name_list):
        self.buttons = dict()
        for name in buttons_name_list:
            self.buttons[name] = Button(self.buttons_frame, text=name)
        for ind, button in enumerate(self.buttons.values()):
            self.buttons_frame.columnconfigure(ind, weight=0)
            button.grid(row=0, column=ind, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        last_button_ind = len(buttons_name_list) - 1
        self.buttons_frame.columnconfigure(last_button_ind, weight=1)
        self.buttons[buttons_name_list[last_button_ind]].grid_configure(sticky=E)
        
    def set_search_buttons(self, buttons_name_list):
        self.search_buttons = dict()
        for name in buttons_name_list:
            self.search_buttons[name] = Button(self.search_frame, text=name)
        for ind, button in enumerate(self.search_buttons.values()):
            self.search_frame.columnconfigure(ind+2, weight=0)
            button.grid(row=0, column=ind+2, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        self.search_category_label.grid(row=1, column=1, sticky="E", columnspan=len(buttons_name_list)+1)
        
    def set_collumns(self, collumns, headings, widths: dict = dict()):
        self.columns = ["№", *collumns]
        self.headings = ["№", *headings]
        self.tree["columns"] = self.columns
        for col, head in zip(self.columns, self.headings):
            self.tree.column(col, anchor="w", stretch=True)
            self.tree.heading(col, text=head, anchor="s")
        for col, width in widths.items():
            self.tree.column(col, width=width, stretch=False)
        self.tree.column("№", width=40, stretch=False)
        
    def set_search_function(self, function, skip_first = True):
        self.skip_first = skip_first
        self.search_function = function
    
    def set_search_results(self, *args):
        self.set_rows(self.search_function(self.search_str.get()), self.skip_first)
        self.search_category_label.config(text=self.default_category)
        
    def set_rows(self, rows, skip_first):
        self.info = dict([(ind+1, order) for ind, order in enumerate(rows)])
        self.tree.delete(*self.tree.get_children())
        if skip_first:
            first_position = 1
        else:
            first_position = 0
        for ind, order in self.info.items():
            self.tree.insert("", END, values=(ind, *order[first_position:]))
        self.set_count()
        
    def set_count(self):
        self.count_label.config(text=f"Всего: {len(self.info)}")
        
    def set_default_category_name(self, name):
        self.default_category = name
    
    def set_on_double_click(self, on_double_click):
        self.tree.bind("<Double-1>", on_double_click)
    