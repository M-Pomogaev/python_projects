from tkinter import *
from tkinter import ttk
import database as db
import utils as ut
from tkinter.messagebox import showerror
from chooseFrame import ChooseFrame
from searchFrame import SearchFrame


class CreateInventoryFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.window = parent
        self.on_save = None
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.medication_label = ttk.Label(self, text="Медикамент")
        self.medication_label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.medication_entry = ttk.Entry(self, state="readonly")
        self.medication_entry.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.medication_choose_button = ttk.Button(self, text="Выбрать", command=self.choose_medication)
        self.medication_choose_button.grid(row=0, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        self.quantity_label = ttk.Label(self, text="Количество")
        self.quantity_label.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.quantity = IntVar(self)
        self.quantity_entry = ttk.Entry(self, textvariable=self.quantity)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W, columnspan=2)
        self.expiration_label = ttk.Label(self, text="Срок годности")
        self.expiration_label.grid(row=2, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.expiration_entry = ttk.Entry(self)
        self.expiration_entry.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W, columnspan=2)
        self.add_button = ttk.Button(self, text="Добавить", command=self.add)
        self.add_button.grid(row=3, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W, columnspan=3)
        
    def choose_medication(self):
        window = Tk()
        choose_medication = ChooseFrame(window)
        choose_medication.set_columns(["name"], ["Название"])
        choose_medication.set_on_choose(self.set_medication)
        choose_medication.set_selectmode("browse")
        choose_medication.set_search_function(db.get_medications)
        choose_medication.set_search_results()
        choose_medication.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
        
        
    def set_medication(self, medication):
        self.medication_id = medication[0][0]
        medication = medication[0][1]
        self.medication_entry.config(state="normal")
        self.medication_entry.delete(0, END)
        self.medication_entry.insert(0, medication)
        self.medication_entry.config(state="readonly")
    
    def set_on_save(self, on_save):
        self.on_save = on_save
        
    def add(self):
        medication_id = self.medication_id
        expire_date = self.expiration_entry.get()
        if not expire_date:
            expire_date = None
        else:
            try:
                expire_date = ut.str_to_date(expire_date)
            except Exception:
                showerror("Ошибка", "Неверный формат даты")
                return
        try:
            quantity = self.quantity.get()
        except TclError:
            showerror("Ошибка", "Неверный формат количества")
            return
        if not medication_id:
            showerror("Ошибка", "Не выбран медикамент")
            return
        try:
            db.insert_inventory(medication_id, quantity, expire_date)
        except Exception as e:
            showerror("Ошибка", "не получилось добавить запись")
            return
        if self.on_save:
            self.on_save()
        self.window.destroy()
    
def create_inventory_window(on_save):
    window = Tk()
    create_inventory = CreateInventoryFrame(window)
    create_inventory.set_on_save(on_save)
    create_inventory.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
    
    
class InventorySearchFrame(SearchFrame):
    def __init__(self, root, menu, font, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.menu = menu
        self.window = root
        self.set_buttons_frame(["Создать", "Удалить", "Назад"])
        self.set_search_buttons(["Все", "Наименьшее количество"])
        self.set_collumns(["medication", "quantity", "expireDate"], ["Медикамент", "Количество", "Срок годности"])
        self.set_font(font)
        self.set_button_onclick("Назад", lambda: ut.show_page(root, menu))
        self.set_button_onclick("Создать", lambda: create_inventory_window(self.set_search_results))
        self.set_button_onclick("Удалить", self.delete)
        self.set_button_onclick("Все", self.set_search_results)
        self.set_button_onclick("Наименьшее количество", self.choose_type_window)
        self.set_search_function(db.get_medications_in_inventory)
        self.set_default_category_name("Все")
        self.set_on_double_click(self.on_double_click)
        
        
    def find_least_quantity(self, type):
        if type:
            self.set_rows(db.find_med_least_quantity(type[0][1]), False)
        else:
            self.set_rows(db.find_med_least_quantity(), False)
        
    def choose_type_window(self):
        window = Tk()
        choose_type = ChooseFrame(window)
        choose_type.set_columns(["quantity"], ["Количество"])
        choose_type.set_on_choose(self.find_least_quantity)
        choose_type.set_selectmode("browse")
        choose_type.set_search_function(db.get_types)
        choose_type.set_search_results()
        choose_type.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
        
    def delete(self):
        medications = []
        for id in self.tree.selection():
            medications.append(self.info[self.tree.item(id)["values"][0]])
        for medication in medications:
            db.delete_inventory(medication[0])
        self.set_search_results()
        
    def on_double_click(self, event):
        medication = self.info[self.tree.item(self.tree.selection())["values"][0]]
        window = Tk()
        window.maxsize(350, 350)
        update_inventory = UpdateInventoryFrame(window)
        update_inventory.set_on_save(self.set_search_results)
        update_inventory.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
        update_inventory.set_info(medication)
        
        
class UpdateInventoryFrame(CreateInventoryFrame):
    def __init__(self, window, *args, **kwargs):
        super().__init__(window, *args, **kwargs)
        self.add_button.config(text="Изменить", command=self.update)
        
    def set_info(self, info):
        self.medication_id = info[0]
        self.medication_entry.config(state="normal")
        self.medication_entry.delete(0, END)
        self.medication_entry.insert(0, info[1])
        self.medication_entry.config(state="readonly")
        self.quantity.set(info[2])
        self.expiration_entry.delete(0, END)
        self.medication_choose_button.destroy()
        if info[3]:
            self.expiration_entry.insert(0, info[3])
        
    def update(self):
        try:
            quantity = self.quantity.get()
        except TclError:
            showerror("Ошибка", "Неверный формат количества")
            return
        if expire_date := self.expiration_entry.get():
            try:
                expire_date = ut.str_to_date(expire_date)
            except TclError:
                showerror("Ошибка", "Неверный формат даты")
                return
        else:
            expire_date = None
        try:
            db.update_inventory(self.medication_id, quantity, expire_date)
        except Exception:
            showerror("Ошибка", "Не получилось обновить запись")
            return
        if self.on_save:
            self.on_save()
        self.window.destroy()