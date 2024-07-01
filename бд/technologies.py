from tkinter import *
from tkinter import ttk
import database as db
from searchFrame import SearchFrame
from chooseFrame import ChooseFrame
from mysql.connector import Error
from tkinter.messagebox import showerror
import utils as ut

class TechnologiesSearchFrame(SearchFrame):
    def __init__(self, root, menu, font, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.menu = menu
        self.window = root
        self.set_buttons_frame(["Создать", "Удалить", "Назад"])
        self.set_search_buttons(["Все", "По типу", "Для медикамента", "Используются в производстве"])
        self.set_font(font)
        self.set_collumns(["name","description"], ["Название", "Описание"], {"name": 200})
        self.set_search_function(db.get_technologies, True)
        self.set_button_onclick("Назад", lambda: ut.show_page(root, menu))
        self.set_button_onclick("Все", lambda: self.set_search_results())
        self.set_button_onclick("Создать", self.create)
        self.set_button_onclick("Удалить", lambda: self.delete())
        self.set_button_onclick("По типу", lambda: ut.create_choose_type_window(self.set_type_search))
        self.set_button_onclick("Для медикамента", lambda: ut.create_choose_medication_window(self.set_medication_search))
        self.set_button_onclick("Используются в производстве", lambda: self.set_rows(db.find_technologies_in_production(), False))
        self.set_search_results()
        self.set_default_category_name("Все")
        self.set_on_double_click(self.on_double_click)
        
    def create(self):
        window = Tk()
        frame = CreateTechnologiesFrame(window, borderwidth=1, relief=SOLID, padding=[8, 10])
        frame.set_on_save(self.set_search_results)
        frame.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
        
        
    def set_type_search(self, type):
        self.set_rows(db.find_technologies_by_type(type[0][1]), False)
        
    def set_medication_search(self, medication):
        self.set_rows(db.find_technologies_by_medication(medication[0][1]), False)
        
    def on_double_click(self, event):
        technology = self.info[self.tree.item(self.tree.selection())["values"][0]]
        print(technology)
        window = Tk()
        window.maxsize(350, 350)
        update_technologies = UpdateTechnologiesFrame(window)
        update_technologies.set_on_save(self.set_search_results)
        update_technologies.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
        update_technologies.set_info(technology)
        
        
    def delete(self):
        technologies = [self.info[self.tree.item(item)["values"][0]] for item in self.tree.selection()]
        try :
            for technology in technologies:
                db.delete_technology(technology[0])
        except Error as e:
            showerror("Error", "Не получилось удалить")
        self.set_search_results()
        
        
class CreateTechnologiesFrame(ttk.Frame):
    def __init__(self, window, *args, **kwargs):
        super().__init__(window, *args, **kwargs)
        self.window = window
        self.on_save = None
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.name_label = ttk.Label(self, text="Название")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.description_label = ttk.Label(self, text="Описание")
        self.description_label.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky="wsne", columnspan=2)
        self.description_text = Text(self)
        self.description_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=1, sticky="nsew")
        self.save_button = ttk.Button(self, text="Сохранить", command=self.save)
        self.save_button.grid(row=3, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=E, columnspan=2)
        
    def set_on_save(self, on_save):
        self.on_save = on_save
        
    def save(self):
        name = self.name_entry.get()
        description = self.description_text.get("1.0", "end")
        try:
            db.insert_technology(name, description)
        except Error as e:
            showerror("Error", "Неверный формат даты" + e.msg)
        if self.on_save:
            self.on_save()
        self.window.destroy()
        
class UpdateTechnologiesFrame(CreateTechnologiesFrame):
    def __init__(self, window, *args, **kwargs):
        super().__init__(window, *args, **kwargs)
        self.save_button.config(text="Изменить", command=self.update)
        
    def set_info(self, info):
        self.id = info[0]
        self.name_entry.delete(0, END)
        self.name_entry.insert(0, info[1])
        self.description_text.delete("1.0", "end")
        self.description_text.insert("1.0", info[2])
    
    def update(self):
        name = self.name_entry.get()
        description = self.description_text.get("1.0", "end")
        try:
            db.update_technology(self.id, name, description)
        except Error as e:
            showerror("Error", "Не получилось обновить, есть ошибки")
            return
        if self.on_save:
            self.on_save()
        
        self.window.destroy()
        