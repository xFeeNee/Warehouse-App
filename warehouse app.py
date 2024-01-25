import tkinter as tk
from tkinter import ttk
import json

def save_inventory_to_file(inventory, filename="inventory.json"):
    with open(filename, "w") as file:
        json.dump(inventory, file)

def load_inventory_from_file(filename="inventory.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

class Warehouse:
    def __init__(self, predefined_items):
        self.predefined_items = predefined_items
        loaded_inventory = load_inventory_from_file()
        if loaded_inventory:
            self.inventory = loaded_inventory
        else:
            self.inventory = {category: {item: 0 for item in items} for category, items in predefined_items.items()}

    def add_item(self, category, item_name, quantity):
        if category in self.inventory and item_name in self.inventory[category]:
            self.inventory[category][item_name] += quantity
            save_inventory_to_file(self.inventory)
            return True
        return False

    def remove_item(self, category, item_name, quantity):
        if category in self.inventory and item_name in self.inventory[category] and self.inventory[category][item_name] >= quantity:
            self.inventory[category][item_name] -= quantity
            save_inventory_to_file(self.inventory)
            return True
        return False

    def get_inventory_list(self):
        inventory_list = ""
        for category, items in self.inventory.items():
            inventory_list += f"{category}:\n"
            inventory_list += "\n".join([f"  {item}: {quantity}" for item, quantity in items.items()])
            inventory_list += "\n\n"
        return inventory_list

class WarehouseApp:
    def __init__(self, root, predefined_items):
        self.warehouse = Warehouse(predefined_items)
        self.root = root
        root.title("Warehouse Management")

        self.tab_control = ttk.Notebook(root)

        # Zakładka zarządzania magazynem
        self.management_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.management_tab, text='Manage Inventory')

        # Zakładka wyświetlania stanu magazynu
        self.inventory_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.inventory_tab, text='Current Inventory')
        self.tab_control.pack(expand=1, fill="both")

        # Elementy interfejsu zakładki zarządzania
        self.category_label = tk.Label(self.management_tab, text="Select Category")
        self.category_label.pack()

        self.selected_category = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.management_tab, textvariable=self.selected_category, values=list(predefined_items.keys()))
        self.category_dropdown.pack()
        self.category_dropdown.bind("<<ComboboxSelected>>", self.update_item_dropdown)

        self.item_label = tk.Label(self.management_tab, text="Select Item")
        self.item_label.pack()

        self.selected_item = tk.StringVar()
        self.item_dropdown = ttk.Combobox(self.management_tab, textvariable=self.selected_item)
        self.item_dropdown.pack()

        self.quantity_entry = tk.Entry(self.management_tab)
        self.quantity_entry.pack()

        self.add_button = tk.Button(self.management_tab, text="Add Item", command=self.add_item)
        self.add_button.pack()

        self.remove_button = tk.Button(self.management_tab, text="Remove Item", command=self.remove_item)
        self.remove_button.pack()

        self.show_button = tk.Button(self.management_tab, text="Update Inventory Tab", command=self.update_inventory_tab)
        self.show_button.pack()

        # Tekst wyświetlający stan magazynu
        self.inventory_text = tk.Text(self.inventory_tab, height=10, width=50)
        self.inventory_text.pack()
        self.inventory_text.config(state=tk.DISABLED)

    def update_inventory_tab(self):
        self.inventory_text.config(state=tk.NORMAL)
        self.inventory_text.delete('1.0', tk.END)
        self.inventory_text.insert(tk.END, self.warehouse.get_inventory_list())
        self.inventory_text.config(state=tk.DISABLED)

    def update_item_dropdown(self, event):
        category = self.selected_category.get()
        self.item_dropdown['values'] = list(predefined_items[category].keys())

    def add_item(self):
        category = self.selected_category.get()
        item = self.selected_item.get()
        try:
            quantity = int(self.quantity_entry.get())
            if self.warehouse.add_item(category, item, quantity):
                self.update_inventory_tab()
        except ValueError:
            pass  # Tutaj możesz dodać obsługę błędów

    def remove_item(self):
        category = self.selected_category.get()
        item = self.selected_item.get()
        try:
            quantity = int(self.quantity_entry.get())
            if self.warehouse.remove_item(category, item, quantity):
                self.update_inventory_tab()
        except ValueError:
            pass  # Tutaj możesz dodać obsługę błędów

    def update_inventory_tab(self):
        self.inventory_text.config(state=tk.NORMAL)
        self.inventory_text.delete('1.0', tk.END)
        self.inventory_text.insert(tk.END, self.warehouse.get_inventory_list())
        self.inventory_text.config(state=tk.DISABLED)




# Lista predefiniowanych części z podkategorią
predefined_items = {
    "Vasco Translator M3": {"Dolna Obudowa (White)": 0, "Górna Obudowa (Black)": 0},
    "Vasco Translator V4": {"Bateria (Model X)": 0, "Ekran (Model Y)": 0}
}

root = tk.Tk()
app = WarehouseApp(root, predefined_items)
root.mainloop()
