from tkinter import *
import database as db
from searchFrame import SearchFrame
from chooseFrame import ChooseFrame
from chooseperiodFrame import ChoosePeriodFrame
import utils as ut

class StatisticsFrame(SearchFrame):
    def __init__(self, root, menu, font, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.window = root
        self.menu = menu
        self.set_buttons_frame(["Назад"])
        self.set_search_buttons(["Все", "Частые", "В период"])
        self.set_collumns(["medication", "volume", "date"], ["Медикамент", "Объём", "Дата"])
        self.set_font(font)
        self.set_button_onclick("Назад", lambda: ut.show_page(root, self.menu))
        self.set_button_onclick("Все", lambda: self.set_search_results())
        self.set_button_onclick("Частые", self.choose_type_for_popular_window)
        self.set_button_onclick("В период", self.choose_medication_for_period_window)
        self.set_search_function(db.get_statistics, False)
        self.set_default_category_name("Все")
        
        
    def find_most_popular(self, type):
        if type:
            self.set_rows(db.find_most_popular_medications(type[0][1]), False)
        else:
            return self.set_rows(db.find_most_popular_medications(), False)
    
    def find_in_period(self, start_date, end_date):
        medications = [medication[1] for medication in self.medications_for_period]
        print(medications, start_date, end_date)
        self.set_rows(db.find_values_in_period(medications, start_date, end_date), False)
    
    
    def choose_type_for_popular_window(self):
        window = Tk()
        window.geometry("270x350")
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        choose_med_type = ChooseFrame(window)
        choose_med_type.set_columns(["type"], ["Тип"])
        choose_med_type.set_search_function(db.get_types)
        choose_med_type.set_search_results()
        choose_med_type.set_selectmode("browse")
        choose_med_type.set_on_choose(self.find_most_popular)
        choose_med_type.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
    def choose_medication_for_period_window(self):
        window = Tk()
        window.geometry("270x350")
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        choose_med_type = ChooseFrame(window)
        choose_med_type.set_columns(["name"], ["Название"])
        choose_med_type.set_search_function(db.get_medications)
        choose_med_type.set_search_results()
        choose_med_type.set_selectmode("extended")
        choose_med_type.set_on_choose(self.choose_period_for_period_window)
        choose_med_type.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
    def choose_period_for_period_window(self, medications):
        self.medications_for_period = medications
        window = Tk()
        window.geometry("270x100")
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        choose_period = ChoosePeriodFrame(window)
        choose_period.set_on_choose(self.find_in_period)
        choose_period.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        