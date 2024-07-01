from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror
from mysql.connector import Error
from datetime import date
import utils as ut
import mysql.connector as connector
import database as db
from chooseFrame import ChooseFrame
from searchFrame import SearchFrame

class CreateOrders(ttk.Frame):
    def __init__(self, window, *args, **kwargs):
        super().__init__(window, *args, **kwargs)
        self.on_create = None
        self.window = window
        self.costumer_frame = ttk.Frame(self, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.costumer_frame.columnconfigure(0, weight=0)
        self.costumer_frame.columnconfigure(1, weight=0)
        self.costumer_frame.columnconfigure(2, weight=1)
        self.costumer_frame.pack(expand=True, fill=BOTH)
        self.costumer_label = ttk.Label(self.costumer_frame, text="Выберите клиента")
        self.costumer_label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.costumer_entry = ttk.Entry(self.costumer_frame, state="readonly")
        self.costumer_entry.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.costumer_button = ttk.Button(self.costumer_frame, text="Выбрать", command=self.choose_costumers)
        self.costumer_button.grid(row=0, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        
        self.medication_frame = ttk.Frame(self, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.medication_frame.columnconfigure(0, weight=0)
        self.medication_frame.columnconfigure(1, weight=1)
        self.medication_frame.columnconfigure(2, weight=0)
        self.medication_frame.columnconfigure(3, weight=1)
        self.medication_frame.rowconfigure(0, weight=1)
        self.medication_frame.rowconfigure(1, weight=1)
        self.medication_frame.pack(expand=True, fill=BOTH)
        self.medication_label = ttk.Label(self.medication_frame, text="Медикамент")
        self.medication_label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.medication_entry = ttk.Entry(self.medication_frame, state="readonly")
        self.medication_entry.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.medication_button = ttk.Button(self.medication_frame, text="Выбрать", command=self.choose_medication)
        self.medication_button.grid(row=0, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=E, columnspan=2)
        self.quantity_label = ttk.Label(self.medication_frame, text="Количество")
        self.quantity_label.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.quantity_var = IntVar(self.medication_frame)
        self.quantity_entry = ttk.Entry(self.medication_frame, textvariable=self.quantity_var)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.instruction_label = ttk.Label(self.medication_frame, text="Инструкция")
        self.instruction_label.grid(row=1, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.instruction_combobox = ttk.Combobox(self.medication_frame, state="readonly")
        self.instruction_combobox.grid(row=1, column=3, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        
        self.patient_frame = ttk.Frame(self, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.patient_frame.columnconfigure(0, weight=0)
        self.patient_frame.columnconfigure(1, weight=1)
        self.patient_frame.columnconfigure(2, weight=0)
        self.patient_frame.columnconfigure(3, weight=1)
        self.patient_frame.rowconfigure(0, weight=1)
        self.patient_frame.rowconfigure(1, weight=1)
        self.patient_frame.rowconfigure(2, weight=1)
        self.patient_frame.pack(expand=True, fill=BOTH)
        self.doctor_name_label = ttk.Label(self.patient_frame, text="Врач")
        self.doctor_name_label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.doctor_name_entry = ttk.Entry(self.patient_frame)
        self.doctor_name_entry.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.patient_name_label = ttk.Label(self.patient_frame, text="Пациент")
        self.patient_name_label.grid(row=0, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.patient_name_entry = ttk.Entry(self.patient_frame)
        self.patient_name_entry.grid(row=0, column=3, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.age_label = ttk.Label(self.patient_frame, text="Возраст")
        self.age_label.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.age_var = IntVar(self.patient_frame)
        self.age_entry = ttk.Entry(self.patient_frame, textvariable=self.age_var)
        self.age_entry.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.diagnosis_label = ttk.Label(self.patient_frame, text="Диагноз")
        self.diagnosis_label.grid(row=1, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.diagnosis_entry = ttk.Entry(self.patient_frame)
        self.diagnosis_entry.grid(row=1, column=3, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.receive_date_label = ttk.Label(self.patient_frame, text="Дата получения")
        self.receive_date_label.grid(row=2, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=E, columnspan=2)
        self.receive_date_entry = ttk.Entry(self.patient_frame, state="disabled")
        self.receive_date_entry.grid(row=2, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=W, columnspan=2)
        
        self.create_button = ttk.Button(self, text="Создать", command=self.create)
        self.create_button.pack(padx=5, pady=5, anchor="e", expand=True, fill=NONE)
        
        self.quantity_var.trace_add("write", self.trace_quantity)
        self.costumer = None
        self.medication = None
        self.instructions = dict([(v, k) for k, v in db.get_instructions()])
        self.instruction_combobox["values"] = list(self.instructions.keys())

    
    def set_on_create(self, on_create):
        self.on_create = on_create
        
    def choose_costumers(self, *args):
        window = Tk()
        window.geometry("500x350")
        choose_costumers = ChooseFrame(window, borderwidth=1, relief=SOLID, padding=[8, 10])
        choose_costumers.set_columns(["name", "phone", "address"], ["Имя", "Телефон", "Адрес"])
        choose_costumers.set_search_function(db.get_costumers)
        choose_costumers.set_selectmode("browse")
        choose_costumers.set_search_results()
        choose_costumers.set_on_choose(self.set_costumer)
        choose_costumers.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
        
        
    def set_costumer(self, costumer):
        self.costumer = costumer[0]
        self.costumer_entry.config(state="normal")
        self.costumer_entry.delete(0, END)
        self.costumer_entry.insert(0, self.costumer[1])
        self.costumer_entry.config(state="readonly")
        
    def choose_medication(self, *args):
        window = Tk()
        window.geometry("500x350")
        choose_medication = ChooseFrame(window, borderwidth=1, relief=SOLID, padding=[8, 10])
        choose_medication.set_columns(["name"], ["Название"])
        choose_medication.set_search_function(db.get_medications)
        choose_medication.set_selectmode("browse")
        choose_medication.set_search_results()
        choose_medication.set_on_choose(self.set_medication)
        choose_medication.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
        
        
    def set_medication(self, medication):
        print(medication)
        self.medication = medication[0]
        self.medication_entry.config(state="normal")
        self.medication_entry.delete(0, END)
        self.medication_entry.insert(0, self.medication[1])
        self.medication_entry.config(state="readonly")
        self.ingridients = db.get_ingridients(self.medication[0])
        self.check_med_inventory(self.medication[0])
        self.check_ingridients(self.medication[1])
        
    def check_med_inventory(self, med_id):
        self.medication_in_inventory = db.get_medication_quantity(med_id)
        if self.medication_in_inventory == None:
            self.medication_in_inventory = 0    
        else:
            self.medication_in_inventory = self.medication_in_inventory[0]
                
    def check_ingridients(self, med_name):
        self.medication_manufactured = db.get_medication_by_name(med_name)[0][1]
        self.ingridients_available = True
        if self.medication_manufactured:
            for ingridient, volume in self.ingridients:
                quantity = db.get_medication_quantity(ingridient)[0]
                if quantity < volume * self.quantity_var.get():
                    self.ingridients_available = False
                    self.receive_date_entry.config(state="disabled")
                    
                    break
            else:
                self.receive_date_entry.config(state="normal")
                
    def trace_quantity(self, *args):
        try:
            self.check_quantity(self.quantity_var.get())
        except TclError:
            return 
        
    def check_quantity(self, quantity):
        if quantity > self.medication_in_inventory:
            if not self.medication_manufactured:
                self.receive_date_entry.config(state="disabled")
                self.ingridients_available = False
            else:
                self.check_ingridients(self.medication[1])
        else:
            self.receive_date_entry.config(state="normal")
            self.ingridients_available = True
                
                
    def get_info(self):
        if not self.costumer or not self.medication:
            showerror("Error", "Все поля должны быть заполнены")
            return
        try:
            self.quantity = self.quantity_var.get()
            self.age = self.age_var.get()
        except TclError:
            showerror("Error", "Количество и возсраст должны быть числом")
            return
        try:
            self.instruction = self.instructions[self.instruction_combobox.get()]
            self.doc_name = self.doctor_name_entry.get()
            self.pat_name = self.patient_name_entry.get()
            self.diag = self.diagnosis_entry.get()
        except TclError:
            showerror("Error", "Все поля должны быть заполнены")
            return
        if self.ingridients_available:
            self.receive_date = self.receive_date_entry.get()
            try:
                self.receive_date = ut.str_to_date(self.receive_date)
            except Exception:
                showerror("Error", "Неверный формат даты получения")
        else:
            self.receive_date = None
        self.order_date = date.today()
        if not self.ingridients_available:
            self.status = "waiting for components"
        else:
            self.status = "in production"
        for id, name in db.get_status():
            if name == self.status:
                self.status = id
                break
    def create(self):
        self.get_info()
        try:
            prescription = db.insert_prescription(self.costumer[0], self.doc_name, self.pat_name, self.age, self.diag, self.medication[0], self.quantity, self.instruction)
            print(prescription, self.medication[0], self.order_date, self.status, self.ingridients_available, self.receive_date)
            db.insert_order(prescription, self.medication[0], self.order_date, self.status, self.ingridients_available, self.receive_date)
            self.update_ingridients()
        except connector.Error as err:
            showerror("Error ", err.msg)
        self.on_create()
        self.window.destroy()
    
    def update_ingridients(self):
        if self.medication_manufactured:
            if self.quantity <= self.medication_in_inventory:
                db.decrease_inventory(self.medication[0], self.quantity)
                db.write_statistic(self.medication[0], self.quantity)
            elif self.ingridients_available:
                for ingridient, volume in self.ingridients:
                    db.decrease_inventory(ingridient, volume*self.quantity)
                    db.write_statistic(ingridient, volume*self.quantity)

        
def create_order_window(on_create):
    window = Tk()
    window.geometry("500x350")
    create_order = CreateOrders(window, borderwidth=1, relief=SOLID, padding=[8, 10])
    create_order.set_on_create(on_create)
    create_order.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
    
class OrderSearchFrame(SearchFrame):
    def __init__(self, root, menu, font, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.menu = menu
        self.window = root
        self.set_buttons_frame(["Добавить", "Удалить", "Назад"])
        self.set_search_buttons(["Все", "В производстве"])
        self.set_collumns(["date", "costumer", "med","status","receive_date"], 
        ["Дата", "Пациент", "Медикамент", "Статус", "Дата получения"],
        {"date": 100, "status": 150, "receive_date": 100})
        self.set_font(font)
        self.set_button_onclick("Назад", lambda: ut.show_page(root, menu))
        self.set_button_onclick("Добавить", lambda: create_order_window(self.set_search_results))
        self.set_button_onclick("Все", lambda: self.set_search_results())
        self.set_button_onclick("В производстве", lambda: self.set_rows(db.find_orders_in_production(), True))
        self.set_button_onclick("Удалить", self.delete)
        self.set_search_function(db.get_orders)
        self.set_default_category_name("Все")
        self.set_on_double_click(self.on_double_click)
        
    def delete(self):
        orders = [self.info[self.tree.item(item)["values"][0]] for item in self.tree.selection()]
        for order in orders:
            try:
                db.delete_order(order[0])
            except Error as e:
                showerror("Error", "Не получилось удалить" + e.msg)
        self.set_search_results()
        
    def on_double_click(self, event):
        order = self.info[self.tree.item(self.tree.selection())["values"][0]]
        order = db.find_order_info(order[0])[0]
        window = Tk()
        window.maxsize(400, 250)
        update_order = UpdateOrdersFrame(window)
        update_order.set_on_create(self.set_search_results)
        update_order.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
        update_order.set_info(order)
        
        
class UpdateOrdersFrame(CreateOrders):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.create_button.config(text="Изменить", command=self.save)
        self.medication_frame.destroy()
        self.age_entry.destroy()
        self.age_label.destroy()
        self.patient_name_entry.destroy()
        self.patient_name_label.destroy()
        self.doctor_name_entry.destroy()
        self.doctor_name_label.destroy()
        self.age_entry.destroy()
        self.age_label.destroy()
        self.diagnosis_label.destroy()
        self.diagnosis_entry.destroy()
        self.status_label = ttk.Label(self.patient_frame, text="Статус")
        self.status_label.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=E, columnspan=2)
        self.status = StringVar(self)
        self.status_combobox = ttk.Combobox(self.patient_frame, state="disabled", textvariable=self.status)
        self.status_combobox.grid(row=1, column=3, padx=5, pady=5, ipadx=5, ipady=1, sticky=W, columnspan=2)
        self.statuses = dict([(i[1], i[0]) for i in db.get_status()])
        self.status_combobox["values"] = list(self.statuses.keys())
        self.status.trace_add("write", self.status_changed)
        
    def set_info(self, info):
        print(info)
        self.info = info
        self.id_order = info[0]
        self.costumer_entry.config(state="normal")
        self.costumer_entry.delete(0, END)
        self.costumer_entry.insert(0, info[1])
        self.costumer_entry.config(state="readonly")
        self.ingridients = db.get_ingridients(info[5])
        self.status_id = info[6]
        self.status_combobox.current(self.status_id-1)
        self.costumer = None
        self.quantity = info[4]
        self.check_ingridients(info[3])
        self.check_med_inventory(info[5])
        if info[2]:
            self.receiving_frame_enable()
            self.ingridients_available = True
        else:
            if not self.medication_manufactured:
                self.check_quantity(info[4])
            if self.ingridients_available:
                self.receiving_frame_enable()
                
    def receiving_frame_enable(self):
        self.receive_date_entry.config(state="normal")
        self.status_combobox.config(state="readonly")
        if self.info[2]:
            self.receive_date_entry.delete(0, END)
            self.receive_date_entry.insert(0, self.info[2])
        
    def status_changed(self, *args):
        if self.status.get() == "waiting for components":
            self.receive_date_entry.delete(0, END)
            self.receive_date_entry.config(state="disabled")
        else:
            self.receive_date_entry.config(state="normal")
            
    def get_info(self):
        if not self.costumer and self.costumer is not None:
            showerror("Error", "Все поля должны быть заполнены")
            return
        if self.costumer is not None:
            self.costumer = self.costumer[0]
        self.status_id_new = self.statuses[self.status_combobox.get()]
        
        if self.info[7] == self.ingridients_available:
            self.ingridients_available = None
        if self.status_id == self.status_id_new:
            self.status_id_new = None
        else:
            self.status_id_new = self.status_id_new
        self.receive_date = self.receive_date_entry.get()
        if self.receive_date:
            try:
                self.receive_date = ut.str_to_date(self.receive_date)
            except Exception:
                showerror("Error", "Неверный формат даты получения")
                return
        else:
            if self.receive_date_entry.state() == "normal":
                showerror("Error", "Необходимо указать дату получения")
                return
            self.receive_date = None
            
    def save(self):
        self.get_info()
        try:
            db.update_order(self.id_order, self.costumer, self.receive_date, self.status_id_new, self.ingridients_available)
            if self.status_id == 2 and self.status_id_new != 2:
                self.update_ingridients()
        except Error as e:
            showerror("Error", "Не получилось изменить\n" + e.msg)
            return
        self.on_create()
        self.window.destroy()