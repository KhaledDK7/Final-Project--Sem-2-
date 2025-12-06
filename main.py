from manager import InventoryManager
from models import PerishableProduct, DigitalProduct, BulkProduct
from database import init_db

def main():
    init_db()
    manager = InventoryManager()
    print("--- CLI Inventory System (Type EXIT to quit) ---")

    while True:
        cmd = input("\nIMS> ").strip().split(" ")
        verb = cmd[0].upper()

        if verb == "EXIT": break
        
        try:
            if verb == "GET" and cmd[1] == "/products":
                for p in manager.get_all_products():
                    print(f"[{p.id}] {p.name} | Qty: {p.quantity} | ${p.price}")

            elif verb == "PUT" and cmd[1] == "/backup":
                manager.backup_to_json()
                print("Backup created.")

            elif verb == "POST" and cmd[1] == "/sale":
                pid = int(input("Product ID: "))
                qty = int(input("Qty: "))
                total = manager.record_sale(pid, qty)
                print(f"Sale recorded. Revenue: ${total:.2f}")

            elif verb == "POST" and cmd[1] == "/product":
                # Simplified CLI input for demonstration
                ptype = input("Type (Perishable/Digital/Bulk): ")
                name = input("Name: ")
                price = float(input("Price: "))
                qty = int(input("Qty: "))
                supp = input("Supplier: ")
                reorder = int(input("Reorder Lvl: "))
                specific = input("Specific Attr (Date/Link/Weight): ")

                if ptype == "Perishable":
                    p = PerishableProduct(name, price, qty, supp, reorder, specific)
                elif ptype == "Digital":
                    p = DigitalProduct(name, price, qty, supp, reorder, specific)
                elif ptype == "Bulk":
                    p = BulkProduct(name, price, qty, supp, reorder, specific)
                
                manager.add_product(p)
                print("Product added.")
            
            else:
                print("Unknown command.")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()