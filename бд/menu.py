from tkinter import *
from tkinter import ttk

class Menu(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu_frame = ttk.Frame(self, borderwidth=3, relief=SOLID, padding=[8, 10])
        self.menu_buttons = { "Заказы": Button(self.menu_frame, text="Заказы"), 
                        "Медикаменты": Button(self.menu_frame, text="Медикаменты"),
                        "Клиенты": Button(self.menu_frame, text="Клиенты"),
                        "Технологии": Button(self.menu_frame, text="Технологии"),
                        "Склад": Button(self.menu_frame, text="Склад"), 
                        "Статистика": Button(self.menu_frame, text="Статистика")}
        self.menu_frame.pack(expand=True, fill=NONE)
        for button in self.menu_buttons.values():
            button.pack(expand=True, fill=X, pady=3, padx=5, ipadx=5, ipady=1)
        
    
    def set_font(self, font_):
        for button in self.menu_buttons.values():
            button.config(font=font_)
            
    def set_button(self, name, comand):
        if name not in self.menu_buttons:
            return
        self.menu_buttons[name].config(command=comand)
        
        