import tkinter as tk
from tkinter import ttk, messagebox
from manager import InventoryManager
from models import PerishableProduct, DigitalProduct, BulkProduct

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory System")
        self.root.geometry("900x600")
        self.manager = InventoryManager()

        # UI Layout
        self.create_controls()
        self.create_table()
        self.refresh_table()

    def create_controls(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.X)
        ttk.Button(frame, text="Refresh", command=self.refresh_table).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="+ Add Product", command=self.popup_add).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="$ Record Sale", command=self.popup_sale).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Backup JSON", command=self.backup).pack(side=tk.RIGHT, padx=5)

    def create_table(self):
        cols = ("ID", "Name", "Type", "Price", "Qty", "Status")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings")
        for col in cols: 
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def refresh_table(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        
        for p in self.manager.get_all_products():
            status = []
            if p.is_low_stock(): status.append("LOW STOCK")
            if hasattr(p, "is_expired") and p.is_expired(): status.append("EXPIRED")
            
            self.tree.insert("", tk.END, values=(
                p.id, p.name, p.type, f"${p.price:.2f}", p.quantity, ", ".join(status) or "OK"
            ))

    def backup(self):
        self.manager.backup_to_json()
        messagebox.showinfo("Info", "Backup Successful")

    def popup_sale(self):
        top = tk.Toplevel(self.root)
        top.title("Sale")
        
        tk.Label(top, text="Product ID").pack()
        e_id = tk.Entry(top)
        e_id.pack()
        
        tk.Label(top, text="Quantity").pack()
        e_qty = tk.Entry(top)
        e_qty.pack()

        def save():
            try:
                rev = self.manager.record_sale(int(e_id.get()), int(e_qty.get()))
                self.refresh_table()
                top.destroy()
                messagebox.showinfo("Success", f"Revenue: ${rev:.2f}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(top, text="Submit", command=save).pack(pady=10)

    def popup_add(self):
        top = tk.Toplevel(self.root)
        top.title("Add Product")
        top.geometry("300x400")

        vars = {
            "name": tk.StringVar(), "price": tk.DoubleVar(), "qty": tk.IntVar(),
            "supp": tk.StringVar(), "reorder": tk.IntVar(value=5), "spec": tk.StringVar(),
            "type": tk.StringVar(value="Perishable")
        }

        tk.Label(top, text="Type").pack()
        cb = ttk.Combobox(top, textvariable=vars["type"], values=["Perishable", "Digital", "Bulk"])
        cb.pack()

        fields = [("Name", "name"), ("Price", "price"), ("Qty", "qty"), 
                  ("Supplier", "supp"), ("Reorder Lvl", "reorder"), ("Specific Attr", "spec")]

        for label, key in fields:
            tk.Label(top, text=label).pack()
            tk.Entry(top, textvariable=vars[key]).pack()

        def save():
            try:
                t = vars["type"].get()
                args = (vars["name"].get(), vars["price"].get(), vars["qty"].get(), 
                        vars["supp"].get(), vars["reorder"].get(), vars["spec"].get())
                
                if t == "Perishable": p = PerishableProduct(*args)
                elif t == "Digital": p = DigitalProduct(*args)
                elif t == "Bulk": p = BulkProduct(*args)
                
                self.manager.add_product(p)
                self.refresh_table()
                top.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(top, text="Save", command=save).pack(pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    # Ensure DB is init before GUI starts
    from database import init_db
    init_db()
    app = InventoryApp(root)
    root.mainloop()