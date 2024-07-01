from tkinter import *
from tkinter import ttk
import utils as ut
from tkinter.messagebox import showerror

class ChoosePeriodFrame(ttk.Frame):
    def __init__(self, window, *args, **kwargs):
        super().__init__(window, *args, **kwargs)
        self.on_choose = None
        self.window = window
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.start_label = ttk.Label(self, text="Начало")
        self.start_label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.start_entry = ttk.Entry(self)
        self.start_entry.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.end_label = ttk.Label(self, text="Конец")
        self.end_label.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.end_entry = ttk.Entry(self)
        self.end_entry.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.choose_button = ttk.Button(self, text="Выбрать", command=self.choose)
        self.choose_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        
    def set_on_choose(self, on_choose):
        self.on_choose = on_choose
        
    def choose(self):
        try:
            start = ut.str_to_date(self.start_entry.get())
            end = ut.str_to_date(self.end_entry.get())
        except Exception as e:
            showerror("Error", "Неверный формат даты" + str(e))
            return
        if self.on_choose:
            self.on_choose(start, end)
        self.window.destroy()