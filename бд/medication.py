from tkinter import *
from tkinter import ttk
from mysql.connector import Error
import database as db
import mysql.connector as connector
from tkinter.messagebox import showerror
from searchFrame import SearchFrame
from chooseFrame import ChooseFrame
import utils as ut


class CreateMedication(ttk.Frame):
    def __init__(self, window, *args, **kwargs):
        super().__init__(window, *args, **kwargs)
        self.window = window
        self.on_save = None
        self.ingridients_values = dict()
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=0)
        self.columnconfigure(0, weight=1)
        self.info_frame = ttk.Frame(self, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.info_frame.rowconfigure(0, weight=0)
        self.info_frame.rowconfigure(1, weight=1)
        self.info_frame.rowconfigure(2, weight=0)
        self.info_frame.rowconfigure(3, weight=1)
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.columnconfigure(1, weight=1)
        self.info_frame.columnconfigure(2, weight=1)
        self.name_label = ttk.Label(self.info_frame, text="Название")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.name_entry = ttk.Entry(self.info_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.manufactured_var = BooleanVar(self.info_frame)
        self.manufactured_check = ttk.Checkbutton(self.info_frame, variable=self.manufactured_var, text="Производится", command=self.on_manufactured_change)
        self.manufactured_check.grid(row=0, column=2, padx=5, pady=5, ipadx=5, ipady=1, columnspan=2)
        self.method_label = ttk.Label(self.info_frame, text="Метод")
        self.method_label.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.method_combo = ttk.Combobox(self.info_frame, state="readonly")
        self.method_combo.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.type_label = ttk.Label(self.info_frame, text="Тип")
        self.type_label.grid(row=1, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.type_combo = ttk.Combobox(self.info_frame, state="readonly")
        self.type_combo.grid(row=1, column=3, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.price_label = ttk.Label(self.info_frame, text="Цена")
        self.price_label.grid(row=2, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.price_entry = ttk.Entry(self.info_frame)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.critical_level_label = ttk.Label(self.info_frame, text="Критический уровень")
        self.critical_level_label.grid(row=2, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.critical_level_entry = ttk.Entry(self.info_frame)
        self.critical_level_entry.grid(row=2, column=3, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        
        self.manufactured_frame = ttk.Frame(self, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.manufactured_frame.rowconfigure(0, weight=1)
        self.manufactured_frame.columnconfigure(0, weight=1)
        self.manufactured_frame.columnconfigure(1, weight=1)
        self.manufactured_frame.columnconfigure(2, weight=1)
        self.manufactured_frame.columnconfigure(3, weight=1)
        self.manufactured_frame.columnconfigure(4, weight=0)
        self.technology_label = ttk.Label(self.manufactured_frame, text="Технология")
        self.technology_label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.technology_combo = ttk.Combobox(self.manufactured_frame, state="disabled")
        self.technology_combo.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.prepare_time_label = ttk.Label(self.manufactured_frame, text="Время приготовления")
        self.prepare_time_label.grid(row=0, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.prepare_time_entry = ttk.Entry(self.manufactured_frame, state="disabled")
        self.prepare_time_entry.grid(row=0, column=3, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.info_frame.grid(row=0, column=0, sticky="nsew")
        self.manufactured_frame.grid(row=1, column=0, sticky="nsew")
        self.choose_ingredient_but = ttk.Button(self.manufactured_frame, text="Выбрать ингредиент", command=self.choose_ingredient, state="disabled")
        self.choose_ingredient_but.grid(row=0, column=4, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        
        self.ingridient_frame = ttk.Frame(self, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.ingridient_frame.rowconfigure(0, weight=1)
        self.ingridient_frame.columnconfigure(0, weight=1)
        self.ingridient_frame.columnconfigure(1, weight=1)
        self.ingridient_frame.grid(row=2, column=0, sticky="nsew")
        
        self.save_but = ttk.Button(self, text="Сохранить", command=self.save)
        self.save_but.grid(row=3, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        
        self.types = dict((v, k) for k, v in db.get_types())
        self.type_combo["values"] = list(self.types.keys())
        self.technologies = dict((name, k) for k, name, prescr in db.get_technologies())
        self.technology_combo["values"] = list(self.technologies.keys())
        self.methods = dict((v, k) for k, v in db.get_methods())
        self.method_combo["values"] = list(self.methods.keys())
        
    def set_on_save(self, on_save):
        self.on_save = on_save
        
    def on_manufactured_change(self):
        if self.manufactured_var.get():
            self.technology_combo["state"] = "readonly"
            self.prepare_time_entry["state"] = "normal"
            self.choose_ingredient_but["state"] = "normal"
        else:
            self.technology_combo["state"] = "disabled"
            self.prepare_time_entry["state"] = "disabled"
            self.choose_ingredient_but["state"] = "disabled"
            self.technology_combo.setvar("")
            self.prepare_time_entry.setvar("")
            for child in self.ingridient_frame.winfo_children():
                child.destroy()
            
    def choose_ingredient(self):
        window = Tk()
        window.geometry("350x350")
        window.maxsize(350, 350)
        choose_ingridient = ChooseFrame(window, borderwidth=1, relief=SOLID, padding=[8, 10])
        choose_ingridient.set_selectmode("extended")
        choose_ingridient.set_columns(["name"], ["Название"])
        choose_ingridient.set_search_function(db.get_medications)
        choose_ingridient.set_search_results()
        choose_ingridient.set_on_choose(self.set_ingridient)
        choose_ingridient.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
        
        
    def set_ingridient(self, ingridients, set_values=False):
        self.ingridients = [(ingridient[0], ingridient[1]) for ingridient in ingridients]
        self.ingridients_values = dict()
        self.ingridients_labels = dict()
        self.ingridients_entries = dict()
        for id, name in self.ingridients:
            self.ingridients_values[id] = IntVar(self.ingridient_frame)
            self.ingridients_labels[id] = ttk.Label(self.ingridient_frame, text=name)
            self.ingridients_entries[id] = ttk.Entry(self.ingridient_frame, textvariable=self.ingridients_values[id])
        for ind, ingridient in enumerate(self.ingridients):
            if set_values:
                self.ingridients_values[ingridients[ind][0]].set(ingridients[ind][2])
            self.ingridient_frame.rowconfigure(ind, weight=1)
            self.ingridients_labels[ingridient[0]].grid(row=ind, column=0, padx=5, pady=2, ipadx=2, ipady=1, sticky=E)
            self.ingridients_entries[ingridient[0]].grid(row=ind, column=1, padx=5, pady=2, ipadx=2, ipady=1, sticky=W)
                
    def get_info(self):
        if not self.method_combo.get():
            showerror("Error", "Метод не может быть пустым")
            return
        self.method = self.methods[self.method_combo.get()]
        if not self.name_entry.get():
            showerror("Error", "Название не может быть пустым")
            return
        self.name = self.name_entry.get()
        if not self.type_combo.get():
            showerror("Error", "Тип не может быть пустым")
            return
        self.type = self.types[self.type_combo.get()]
        if not self.price_entry.get():
            showerror("Error", "Цена не может быть пустым")
            return
        self.price = self.price_entry.get()
        if not self.critical_level_entry.get():
            showerror("Error", "Критический уровень не может быть пустым")
            return
        self.critical_level = self.critical_level_entry.get()
        self.manufactured = self.manufactured_var.get()
        if self.manufactured:
            if not self.prepare_time_entry.get():
                showerror("Error", "Время приготовления не может быть пустым")
                return
            self.prepare_time = self.prepare_time_entry.get()
            if not self.technology_combo.get():
                showerror("Error", "Технология не может быть пустым")
                return
            self.technology = self.technologies[self.technology_combo.get()]
        else:
            self.technology = None
            self.prepare_time = None
        for ingr in self.ingridients_values:
            if not self.ingridients_values[ingr].get():
                showerror("Error", "Ингридиенты не могут быть пустыми")
                return        
    
    def save(self):
        self.get_info()
        try:
            db.insert_medication(self.name, self.type, self.method, self.manufactured, self.technology, self.prepare_time, self.price, self.critical_level)
        except connector.Error as err:
            showerror("Error", err.msg)
            return
        if not self.ingridients_values == dict(): 
            id = db.get_medication_by_name(self.name)[0][0]
            for ingr in self.ingridients_values.keys():
                db.insert_ingredient(id, ingr, self.ingridients_values[ingr].get())
        if self.on_save:
            self.on_save()
        self.window.destroy()
        
def create_medication_window(on_save):
    window = Tk()
    window.geometry("700x450")
    create_medication = CreateMedication(window)
    create_medication.set_on_save(on_save)
    create_medication.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
    
   
   
class MedicationSearchFrame(SearchFrame): 
    def __init__(self, root, menu, font, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.menu = menu
        self.window = root
        self.font = font
        self.set_buttons_frame(["Добавить", "Удалить", "Информация", "Назад"])
        self.set_search_buttons(["Все", "Достигшие критичности", "Нужны для заказов"])
        self.set_collumns(["name", "type", "method", "manufactured", "technology", "prepareTime", "price", "criticalLevel"], 
                                    ["Название", "Тип", "Метод", "Производимый", "Технология", "Время приготовления", "Цена", "Критичность"],
                                    {"prepareTime": 100, "price": 100, "criticalLevel": 100, "type": 60, "method": 60, "manufactured": 50})
        self.set_font(font)
        self.set_button_onclick("Назад", lambda: ut.show_page(root, self.menu))
        self.set_button_onclick("Добавить", lambda: create_medication_window(self.set_search_results))
        self.set_button_onclick("Все", lambda: self.set_search_results())
        self.set_button_onclick("Достигшие критичности", lambda: self.set_rows(db.find_critical_level(), True))
        self.set_button_onclick("Нужны для заказов", lambda: self.set_rows(db.find_med_needed_for_orders(), True))
        self.set_button_onclick("Информация", self.show_info)
        self.set_button_onclick("Удалить", lambda: self.delete())
        self.set_search_function(db.get_medications)
        self.set_default_category_name("Все")
        self.buttons["Информация"].config(state="disabled")
        self.buttons["Удалить"].config(state="disabled")
        self.tree.bind("<<TreeviewSelect>>", self.select)
        self.set_on_double_click(self.on_double_click)
        
    def select(self, event):
        if len(self.tree.selection()) == 1:
            self.buttons["Информация"].config(state="normal")
        else:
            self.buttons["Информация"].config(state="disabled")
        if len(self.tree.selection()) > 0:
            self.buttons["Удалить"].config(state="normal")
        else:
            self.buttons["Удалить"].config(state="disabled")
            
    def show_info(self):
        info = self.info[self.tree.item(self.tree.selection()[0])["values"][0]]
        name = info[1]
        print(info := db.find_medication_info(name))
        window = Tk()
        medication_info = MedicationInfoFrame(window)
        medication_info.set_info(info[0], info[1])
        medication_info.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
        
    
    def delete(self):
        id = self.info[self.tree.item(self.tree.selection()[0])["values"][0]][0]
        try:
            db.delete_medication(id)
        except Error as e:
            showerror("Error", "Не получилось удалить" + e.msg)
        self.set_search_results()
        
    def on_double_click(self, event):
        window = Tk()
        update_frame = MedicationUpdateFrame(window)
        info = self.info[self.tree.item(self.tree.selection()[0])["values"][0]]
        ingrs = db.find_ingridients_by_medication(info[0])
        update_frame.set_info(info, ingrs)
        update_frame.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
        update_frame.set_on_save(self.set_search_results)
    
        
class MedicationInfoFrame(ttk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.window = root
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=1)
        self.name_label = ttk.Label(self, text="Название")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.name_entry = ttk.Entry(self, state="readonly")
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.type_label = ttk.Label(self, text="Тип")
        self.type_label.grid(row=0, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.type_entry = ttk.Entry(self, state="readonly")
        self.type_entry.grid(row=0, column=3, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.quantity_label = ttk.Label(self, text="Количество")
        self.quantity_label.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.quantity_entry = ttk.Entry(self, state="readonly")
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.price_label = ttk.Label(self, text="Цена")
        self.price_label.grid(row=1, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.price_entry = ttk.Entry(self, state="readonly")
        self.price_entry.grid(row=1, column=3, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.technology_label = ttk.Label(self, text="Технология")
        self.technology_label.grid(row=2, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.technology_entry = ttk.Entry(self, state="readonly")
        self.technology_entry.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W, columnspan=3)
        self.ingridients_label = ttk.Label(self, text="Ингридиенты")
        self.ingridients_label.grid(row=3, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky="wsne", columnspan=4)
        self.columns =("name", "quantity", "price")
        self.headings = ("Название", "Количество", "Цена")
        self.ingridients_tree = ttk.Treeview(self, columns=self.columns, show="headings")
        for col, head in zip(self.columns, self.headings):
            self.ingridients_tree.heading(col, text=head)
        self.ingridients_tree.grid(row=4, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky="nsew", columnspan=4)
    
    def set_info(self, info, ingr):
        print(info, ingr)
        self.name_entry.configure(state="normal")
        self.name_entry.delete(0, END)
        self.name_entry.insert(0, info[1])
        self.name_entry.configure(state="readonly")
        self.type_entry.configure(state="normal")
        self.type_entry.delete(0, END)
        self.type_entry.insert(0, info[2])
        self.type_entry.configure(state="readonly")
        if info[3] is not None:
            self.quantity_entry.configure(state="normal")
            self.quantity_entry.delete(0, END)
            self.quantity_entry.insert(0, info[3])
            self.quantity_entry.configure(state="readonly")
        self.price_entry.configure(state="normal")
        self.price_entry.delete(0, END)
        self.price_entry.insert(0, info[4])
        self.price_entry.configure(state="readonly")
        if info[5] is not None:
            self.technology_entry.configure(state="normal")
            self.technology_entry.delete(0, END)
            self.technology_entry.insert(0, info[5])
            self.technology_entry.configure(state="readonly")
        self.ingridients_tree.delete(*self.ingridients_tree.get_children())
        for ingridient in ingr:
            self.ingridients_tree.insert("", END, values=ingridient)
            
class MedicationUpdateFrame(CreateMedication):
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.window = parent
        
    def set_info(self, info, ingr):
        print(info, ingr)
        self.id = info[0]
        self.name_entry.delete(0, END)
        self.name_entry.insert(0, info[1])
        self.type_combo.set(info[2])
        self.method_combo.set(info[3])
        self.manufactured_var.set(info[4])
        self.on_manufactured_change()
        if info[5] is not None:
            self.technology_combo.set(info[5])
        if info[6] is not None:
            self.prepare_time_entry.delete(0, END)
            self.prepare_time_entry.insert(0, info[6])
        self.price_entry.delete(0, END)
        self.price_entry.insert(0, info[7])
        self.critical_level_entry.delete(0, END)
        self.critical_level_entry.insert(0, info[8])
        self.set_ingridient(ingr, set_values=True)
        self.save_but.configure(command=self.change, text="Изменить")
        
    def change(self):
        self.get_info()
        try:
            db.update_medication(self.id, self.name, self.type, self.method, self.manufactured, self.price, self.critical_level, self.technology, self.prepare_time)
        except connector.Error as err:
            showerror("Error", err.msg)
            return
        if not self.ingridients_values == dict(): 
            ing_ids = self.ingridients_values.keys()
            voluems = [self.ingridients_values[ingridient].get() for ingridient in ing_ids]
            db.update_ingridients(self.id, ing_ids, voluems)
        if self.on_save:
            self.on_save()
        self.window.destroy()
            
        
        
        