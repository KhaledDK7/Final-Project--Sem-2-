import json
import sqlite3
from database import get_connection
from models import Product, PerishableProduct, DigitalProduct, BulkProduct

class InventoryManager:
    
    def add_product(self, product: Product):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (name, type, price, quantity, supplier, reorder_level, specific_attr)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (product.name, product.type, product.price, product.quantity, 
              product.supplier, product.reorder_level, product.get_specific_attr()))
        conn.commit()
        conn.close()

    def _row_to_object(self, row):
        if not row: return None
        p_id, name, p_type, price, qty, supp, reorder, specific = row
        
        if p_type == "Perishable":
            return PerishableProduct(name, price, qty, supp, reorder, specific, p_id)
        elif p_type == "Digital":
            return DigitalProduct(name, price, qty, supp, reorder, specific, p_id)
        elif p_type == "Bulk":
            return BulkProduct(name, price, qty, supp, reorder, specific, p_id)
        return None

    def get_all_products(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_object(row) for row in rows]

    def get_product_by_id(self, p_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id=?", (p_id,))
        row = cursor.fetchone()
        conn.close()
        return self._row_to_object(row)

    def record_sale(self, p_id, quantity_sold):
        """Records sale and returns total price. Raises ValueError on failure."""
        product = self.get_product_by_id(p_id)
        if not product:
            raise ValueError("Product not found")
        
        if product.quantity < quantity_sold:
            raise ValueError(f"Insufficient stock. Current: {product.quantity}")

        new_qty = product.quantity - quantity_sold
        total_price = quantity_sold * product.price
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_qty, p_id))
        cursor.execute("INSERT INTO sales (product_id, quantity_sold, total_price) VALUES (?, ?, ?)", 
                       (p_id, quantity_sold, total_price))
        conn.commit()
        conn.close()
        return total_price

    def backup_to_json(self, filename="backup.json"):
        products = self.get_all_products()
        data = [p.to_dict() for p in products]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)