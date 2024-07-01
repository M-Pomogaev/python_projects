import re
from datetime import date
from searchFrame import SearchFrame
from chooseFrame import ChooseFrame
import database as db
from tkinter import *

def str_to_date(date_str):
    date_ = date_str.strip()
    date_ = "-".join(re.split("[^0-9]+", date_))
    date_ = date.fromisoformat(date_)
    return date_

def clear_window(root):
    for widget in root.winfo_children():
        widget.pack_forget()
        
def show_page(root, page):
    clear_window(root)
    page.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
    if issubclass(type(page), SearchFrame):
        page.set_search_results()
        
def create_choose_medication_window(on_choose):
    window = Tk()
    window.geometry("500x350")
    choose_medication = ChooseFrame(window, borderwidth=1, relief=SOLID, padding=[8, 10])
    choose_medication.set_columns(["name"], ["Название"])
    choose_medication.set_search_function(db.get_medications)
    choose_medication.set_selectmode("browse")
    choose_medication.set_search_results()
    choose_medication.set_on_choose(on_choose)
    choose_medication.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)
    
def create_choose_type_window(on_choose):
    window = Tk()
    window.geometry("300x300")
    choose_type = ChooseFrame(window, borderwidth=1, relief=SOLID, padding=[8, 10])
    choose_type.set_columns(["name"], ["Название"])
    choose_type.set_on_choose(on_choose)
    choose_type.set_selectmode("browse")
    choose_type.set_search_function(db.get_types)
    choose_type.set_search_results()
    choose_type.pack(padx=5, pady=5, anchor="center", expand=True, fill=BOTH)