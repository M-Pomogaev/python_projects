from tkinter import *
import tkinter.ttk as ttk
from tkinter import font

class InfoPage(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=2)
        self.rowconfigure(1, weight=1)
        
        self.label = ttk.Label(self, text="Информация")
        self.text_frame = ttk.Frame(self, borderwidth=3, relief=SOLID, padding=[20, 15])
        self.text_frame.grid(row=1, column=1, sticky="nsew", columnspan=3)
        self.text_frame.rowconfigure(0, weight=1)
        self.text_frame.columnconfigure(0, weight=1)
        self.text = Text(self.text_frame, state="disabled", wrap="word")
        self.scrollbar = Scrollbar(self.text_frame, command=self.text.yview)
        
        self.label.grid(row=0, column=2, sticky="nsew", pady=10)
        self.text.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="nsew")
        
    def set_label_font(self, font):
        self.label.configure(font=font)
        
    def set_paragraph_font(self, font):
        self.text.tag_config("paragraph", font=font)
        
    def set_main_text_font(self, font):
        self.text.tag_config("main_text", font=font)
        
    def add_paragraph(self, text):
        self.text.configure(state="normal")
        self.text.insert(END, text + "\n", "paragraph")
        self.text.configure(state="disabled")
        self.text.see(END)
    
    def add_main_text(self, text):
        self.text.configure(state="normal")
        self.text.insert(END, text + "\n", "main_text")
        self.text.configure(state="disabled")
        self.text.see(END)

if __name__ == "__main__":
    window = Tk()
    window.title("Page")
    window.geometry("900x600")
    page = InfoPage(window, borderwidth=3, relief=SOLID, padding=[20, 15])
    page.set_label_font(font.Font(family="Arial", size=20))
    page.set_paragraph_font(font.Font(family="Arial", size=16, weight="bold"))
    page.set_main_text_font(font.Font(family="Arial", size=12))
    for i in range(20):
        page.add_paragraph("Текст")
        page.add_main_text("Текст")
    page.pack(expand=True, fill=BOTH)
    window.mainloop()