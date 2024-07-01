from tkinter import *
import tkinter.ttk as ttk
from tkinter import font

class Page(ttk.Frame):
    def __init__(self, has_group, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_background = "white"
        self.text_width = 12
        self.has_group = has_group
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=2)
        
        self.user_label = ttk.Label(self, text="Пользователь")
        self.user_label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.user_frame = ttk.Frame(self, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.user_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.user_frame.columnconfigure(0, weight=1)
        self.user_frame.columnconfigure(1, weight=1)
        self.user_frame.columnconfigure(2, weight=1)
        self.user_frame.columnconfigure(3, weight=1)
        self.user_frame.rowconfigure(0, weight=1)
        self.user_frame.rowconfigure(1, weight=1)
        if has_group:
            self.user_frame.rowconfigure(2, weight=1)
        self.name_label = ttk.Label(self.user_frame, text="ФИО:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=E, columnspan=2)
        self.name_text = ttk.Label(self.user_frame, background=self.text_background)
        self.name_text.grid(row=0, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=W, columnspan=2)
        self.login_label = ttk.Label(self.user_frame, text="Логин:")
        self.login_label.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        self.login_text = ttk.Label(self.user_frame, background=self.text_background, width=self.text_width)
        self.login_text.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.user_status_label = ttk.Label(self.user_frame, text="Статус:")
        self.user_status_label.grid(row=1, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        self.user_status_text = ttk.Label(self.user_frame, background=self.text_background, width=self.text_width)
        self.user_status_text.grid(row=1, column=3, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        if has_group:
            self.group_label = ttk.Label(self.user_frame, text="Группа:")
            self.group_label.grid(row=2, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
            self.group_text = ttk.Label(self.user_frame, background=self.text_background, width=self.text_width)
            self.group_text.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
            self.cafedra_label = ttk.Label(self.user_frame, text="Кафедра:")
            self.cafedra_label.grid(row=2, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
            self.cafedra_text = ttk.Label(self.user_frame, background=self.text_background, width=self.text_width)
            self.cafedra_text.grid(row=2, column=3, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        
        self.abonement_label = ttk.Label(self, text="Абонемент")
        self.abonement_label.grid(row=2, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.abonement_frame = ttk.Frame(self, borderwidth=1, relief=SOLID, padding=[8, 10])
        self.abonement_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.abonement_frame.columnconfigure(0, weight=1)
        self.abonement_frame.columnconfigure(1, weight=1)
        self.abonement_frame.columnconfigure(2, weight=1)
        self.abonement_frame.columnconfigure(3, weight=1)
        self.abonement_frame.rowconfigure(0, weight=1)
        self.abonement_frame.rowconfigure(1, weight=1)
        self.abonement_frame.rowconfigure(2, weight=1)
        self.abonement_frame.rowconfigure(3, weight=1)
        self.abonement_frame.rowconfigure(4, weight=1)
        self.abonement_name_label = ttk.Label(self.abonement_frame, text="Название:")
        self.abonement_name_label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=E, columnspan=2)
        self.abonement_name_text = ttk.Label(self.abonement_frame, background=self.text_background, width=self.text_width)
        self.abonement_name_text.grid(row=0, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=W, columnspan=2)
        self.available_books_num_label = ttk.Label(self.abonement_frame, text="Кол-во доступных книг:")
        self.available_books_num_label.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        self.available_books_num_text = ttk.Label(self.abonement_frame, background=self.text_background, width=self.text_width)
        self.available_books_num_text.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.receive_date_label = ttk.Label(self.abonement_frame, text="Дата получения:")
        self.receive_date_label.grid(row=1, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        self.receive_date_text = ttk.Label(self.abonement_frame, background=self.text_background, width=self.text_width)
        self.receive_date_text.grid(row=1, column=3, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.taken_books_num_label = ttk.Label(self.abonement_frame, text="Кол-во выданных книг:")
        self.taken_books_num_label.grid(row=2, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        self.taken_books_num_text = ttk.Label(self.abonement_frame, background=self.text_background, width=self.text_width)
        self.taken_books_num_text.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.end_date_label = ttk.Label(self.abonement_frame, text="Дата окончания:")
        self.end_date_label.grid(row=2, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        self.end_date_text = ttk.Label(self.abonement_frame, background=self.text_background, width=self.text_width)
        self.end_date_text.grid(row=2, column=3, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.reading_time_label = ttk.Label(self.abonement_frame, text="Время на прочтения:")
        self.reading_time_label.grid(row=3, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        self.reading_time_text = ttk.Label(self.abonement_frame, background=self.text_background, width=self.text_width)
        self.reading_time_text.grid(row=3, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.abonement_status_label = ttk.Label(self.abonement_frame, text="Статус:")
        self.abonement_status_label.grid(row=3, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        self.abonement_status_text = ttk.Label(self.abonement_frame, background=self.text_background, width=self.text_width)
        self.abonement_status_text.grid(row=3, column=3, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.panelty_num_label = ttk.Label(self.abonement_frame, text="Кол-во штрафов:")
        self.panelty_num_label.grid(row=4, column=0, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        self.panelty_num_text = ttk.Label(self.abonement_frame, background=self.text_background, width=self.text_width)
        self.panelty_num_text.grid(row=4, column=1, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        self.able_get_books_label = ttk.Label(self.abonement_frame, text="Можно получать книги:")
        self.able_get_books_label.grid(row=4, column=2, padx=5, pady=5, ipadx=5, ipady=1, sticky=E)
        self.able_get_books_text = ttk.Label(self.abonement_frame, background=self.text_background, width=self.text_width)
        self.able_get_books_text.grid(row=4, column=3, padx=5, pady=5, ipadx=5, ipady=1, sticky=W)
        
        self.texts_dict = {
            "Время_прочтения": self.reading_time_text,
            "Дата_выдачи": self.receive_date_text,
            "Дата_окончания": self.end_date_text,
            "Книг_выдано": self.taken_books_num_text,
            "Книг_доступно": self.available_books_num_text,
            "Логин": self.login_text,
            "Название_абонемента": self.abonement_name_text,
            "Новые_книги": self.able_get_books_text,
            "Статус": self.user_status_text,
            "Статус_абонемента": self.abonement_status_text,
            "ФИО": self.name_text,
            "Число_штрафов": self.panelty_num_text
        }
        if self.has_group:
            self.texts_dict["Номер_группы"] = self.group_text
            self.texts_dict["Название_кафедры"] = self.cafedra_text
        
        
    def set_info_font(self, font):
        for child in self.user_frame.winfo_children():
            if isinstance(child, ttk.Label):
                child.config(font=font)
        for child in self.abonement_frame.winfo_children():
            if isinstance(child, ttk.Label):
                child.config(font=font)
    
    def set_boxes_font(self, font):
        for child in self.winfo_children():
            if isinstance(child, ttk.Label):
                child.config(font=font)
                
    def set_info(self, info):
        for key, value in info.items():
            self.texts_dict[key].config(text=value)
                
        
if __name__ == "__main__":
    window = Tk()
    window.title("Page")
    window.geometry("800x600")
    page = Page(True, window, borderwidth=3, relief=SOLID, padding=[20, 15])
    page.set_info_font(font.Font(family="Arial", size=12))
    page.set_boxes_font(font.Font(family="Arial", size=16, weight="bold"))
    page.set_info({            
            "Время_прочтения": "5",
            "Дата_выдачи": "2021-01-01",
            "Дата_окончания": "2025-01-01",
            "Книг_выдано": "5",
            "Книг_доступно": "5",
            "Логин": "admin",
            "Название_абонемента": "Абонемент",
            "Новые_книги": "да",
            "Статус": "Активен",
            "Статус_абонемента": "Активен",
            "ФИО": "Иванов И.И.",
            "Число_штрафов": "0",
            "Номер_группы": "1",
            "Название_кафедры": "Кафедра"
            })
    page.pack(expand=True, fill=BOTH)
    window.mainloop()