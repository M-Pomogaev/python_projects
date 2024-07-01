from tkinter import *
from tkinter import font
from menu import Menu
from orders import OrderSearchFrame
from costumers import CostumerSearchFrame
from medication import MedicationSearchFrame
from statistc import StatisticsFrame
from inventory import InventorySearchFrame
from technologies import TechnologiesSearchFrame
import utils as ut
    
    
if __name__ == "__main__":
    root = Tk()
    page_font = font.Font(family="Arial", size=11)
    root.geometry("900x500")
    menu_page = Menu(root, borderwidth=1, relief=SOLID, padding=[8, 10])
    menu_page.set_font(page_font)
    medication_frame = MedicationSearchFrame(root, menu_page, page_font, borderwidth=1, relief=SOLID, padding=[8, 10])
    costumers_frame = CostumerSearchFrame(root, menu_page, page_font, borderwidth=1, relief=SOLID, padding=[8, 10])
    statistics_frame = StatisticsFrame(root, menu_page, page_font, borderwidth=1, relief=SOLID, padding=[8, 10])
    inventory_frame = InventorySearchFrame(root, menu_page, page_font, borderwidth=1, relief=SOLID, padding=[8, 10])
    orders_frame = OrderSearchFrame(root, menu_page, page_font, borderwidth=1, relief=SOLID, padding=[8, 10])
    technologies_frame = TechnologiesSearchFrame(root, menu_page, page_font, borderwidth=1, relief=SOLID, padding=[8, 10])
    menu_page.set_button("Клиенты", lambda: ut.show_page(root, costumers_frame))
    menu_page.set_button("Медикаменты", lambda: ut.show_page(root, medication_frame))
    menu_page.set_button("Статистика", lambda: ut.show_page(root, statistics_frame))
    menu_page.set_button("Склад", lambda: ut.show_page(root, inventory_frame))
    menu_page.set_button("Заказы", lambda: ut.show_page(root, orders_frame))
    menu_page.set_button("Технологии", lambda: ut.show_page(root, technologies_frame))
    ut.show_page(root, menu_page)
    root.mainloop()
    