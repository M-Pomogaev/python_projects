from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror
from mysql.connector import Error
import database as db
from searchFrame import SearchFrame
from chooseperiodFrame import ChoosePeriodFrame
import utils as ut


class CreateCostumer(ttk.Frame):
    def __init__(self, window, *args, **kwargs):
        super().__init__(window, *args, **kwargs)
        self.window = window
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=0)
        self.columnconfigure(0, weight=1)
        self.name_frame = ttk.Frame(self, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.name_frame.columnconfigure(0, weight=1)
        self.name_frame.columnconfigure(1, weight=1)
        self.name_frame.grid(row=0, column=0, sticky="nsew")
        self.phone_frame = ttk.Frame(self, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.phone_frame.columnconfigure(0, weight=1)
        self.phone_frame.columnconfigure(1, weight=1)
        self.phone_frame.grid(row=1, column=0, sticky="nsew")
        self.address_frame = ttk.Frame(self, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.address_frame.columnconfigure(0, weight=1)
        self.address_frame.columnconfigure(1, weight=1)
        self.address_frame.grid(row=2, column=0, sticky="nsew")
        self.name_label = ttk.Label(self.name_frame, text="Имя")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.name_entry = ttk.Entry(self.name_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=1)
        self.phone_label = ttk.Label(self.phone_frame, text="Телефон")
        self.phone_label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.phone_entry = ttk.Entry(self.phone_frame)
        self.phone_entry.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=1)
        self.address_label = ttk.Label(self.address_frame, text="Адрес")
        self.address_label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.address_entry = ttk.Entry(self.address_frame)
        self.address_entry.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=1)
        self.buttons_frame = ttk.Frame(self, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.buttons_frame.columnconfigure(0, weight=1)
        self.buttons_frame.columnconfigure(1, weight=1)
        self.buttons_frame.grid(row=3, column=0, sticky="nsew")
        self.save_button = ttk.Button(self.buttons_frame, text="Сохранить", command=self.save_costumer)
        self.save_button.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        self.back_button = ttk.Button(self.buttons_frame, text="Назад", command=self.window.destroy)
        self.back_button.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.on_save = None
        
    def save_costumer(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        db.insert_costumer(name, phone, address)
        if self.on_save:
            self.on_save()
        self.window.destroy()
    
    def set_on_save(self, onsave):
        self.on_save = onsave
        
def create_costumer_window(onsave=None):
    window = Tk()
    window.geometry("500x350")
    create_costumer = CreateCostumer(window, borderwidth=1, relief=SOLID, padding=[8, 10])
    create_costumer.set_on_save(onsave)
    create_costumer.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
    
    
class CostumerSearchFrame(SearchFrame):
    def __init__(self, window, menu, font, *args, **kwargs):
        super().__init__(window, *args, **kwargs)
        self.window = window
        self.menu = menu
        self.font = font
        self.set_buttons_frame(["Добавить", "Удалить", "Назад"])
        self.set_search_buttons(["Все", "Не забрали заказ", "В ожидании", "По лекарству", "Частые по лекарству", "Частые по типу"])
        self.set_collumns(["name", "phone", "address"], ["Имя", "Телефон", "Адрес"])
        self.set_font(self.font)
        self.set_button_onclick("Назад", lambda: ut.show_page(self.window, self.menu))
        self.set_button_onclick("Все", lambda: self.set_search_results())
        self.set_button_onclick("Добавить", lambda: create_costumer_window(self.set_search_results))
        self.set_button_onclick("Не забрали заказ", lambda: self.set_rows(db.find_costumers_not_take_order(), False))
        self.set_button_onclick("В ожидании", lambda: ut.create_choose_type_window(self.find_wait_for_ingrids))
        self.set_button_onclick("По лекарству", lambda: ut.create_choose_medication_window(self.choose_period_window))
        self.set_button_onclick("Частые по лекарству", lambda: ut.create_choose_medication_window(self.set_freaquent_by_med))
        self.set_button_onclick("Частые по типу", lambda: ut.create_choose_type_window(self.set_freaquent_by_type))
        self.set_button_onclick("Удалить", lambda: self.delete())
        self.set_search_function(db.get_costumers)
        self.set_default_category_name("Все")
        self.set_on_double_click(self.on_double_click)
        
    def find_wait_for_ingrids(self, type):
        if type:
            self.set_rows(db.find_costumers_wait_order(type[0][1]), False)
        else:
            return self.set_rows(db.find_costumers_wait_order(), False)
        
    def find_for_med_in_period(self, start, end):
        self.set_rows(db.find_for_med_in_period(self.medication, start, end), False)
        
    def choose_period_window(self, medication):
        self.medication = medication[0][1]
        window = Tk()
        window.geometry("270x150")
        choose_period = ChoosePeriodFrame(window)
        choose_period.set_on_choose(self.find_for_med_in_period)
        choose_period.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
        
        
    def set_freaquent_by_med(self, medications):
        self.set_rows(db.find_most_freaquent_costumers_by_medication(medications[0][1]), False)
    
    def set_freaquent_by_type(self, type):
        self.set_rows(db.find_most_freaquent_costumers_by_type(type[0][1]), False)
        
    def delete(self):
        costumers = [self.info[self.tree.item(item)["values"][0]] for item in self.tree.selection()]
        try :
            for costumer in costumers:
                db.delete_costumer(costumer[0])
        except Error:
            showerror("Error", "Не получилось удалить")
        self.set_search_results()
    
    def on_double_click(self, event):
        costumer = self.info[self.tree.item(self.tree.selection()[0])["values"][0]]
        window = Tk()
        window.maxsize(350, 350)
        update_costumer = UpdateCostumerFrame(window)
        update_costumer.set_on_save(self.set_search_results)
        update_costumer.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
        update_costumer.set_info(costumer)
        
    
        
class UpdateCostumerFrame(CreateCostumer):
    def __init__(self, window, borderwidth=1, relief=SOLID, padding=[8, 10]):
        super().__init__(window, borderwidth=borderwidth, relief=relief, padding=padding)
        self.window = window
        self.save_button.config(text="Изменить", command=self.save)
        
    def set_info(self, info):
        self.id = info[0]
        self.name_entry.delete(0, END)
        self.name_entry.insert(0, info[1])
        self.phone_entry.delete(0, END)
        self.phone_entry.insert(0, info[2])
        self.address_entry.delete(0, END)
        self.address_entry.insert(0, info[3])
        
    def save(self):
        try:
            db.update_costumer(self.id, self.name_entry.get(), self.phone_entry.get(), self.address_entry.get())
        except Error:
            showerror("Error", "Не получилось изменить")
        if self.on_save:
            self.on_save()
        self.window.destroy()
