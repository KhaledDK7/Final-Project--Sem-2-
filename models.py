from abc import ABC, abstractmethod
from datetime import datetime

class Product(ABC):
    def __init__(self, name, price, quantity, supplier, reorder_level, product_id=None):
        self.id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.supplier = supplier
        self.reorder_level = reorder_level
        self.type = "Generic"

    def calculate_value(self):
        return self.price * self.quantity

    def is_low_stock(self):
        return self.quantity <= self.reorder_level

    @abstractmethod
    def get_specific_attr(self):
        pass

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "price": self.price,
            "qty": self.quantity,
            "specific": self.get_specific_attr()
        }

class PerishableProduct(Product):
    def __init__(self, name, price, quantity, supplier, reorder_level, expiry_date, product_id=None):
        super().__init__(name, price, quantity, supplier, reorder_level, product_id)
        self.expiry_date = expiry_date 
        self.type = "Perishable"

    def get_specific_attr(self):
        return self.expiry_date

    def is_expired(self):
        try:
            exp = datetime.strptime(self.expiry_date, "%Y-%m-%d")
            return datetime.now() > exp
        except ValueError:
            return False

    def calculate_value(self):
        if self.is_expired(): return 0.0
        return super().calculate_value()

class DigitalProduct(Product):
    def __init__(self, name, price, quantity, supplier, reorder_level, link, product_id=None):
        super().__init__(name, price, quantity, supplier, reorder_level, product_id)
        self.link = link
        self.type = "Digital"

    def get_specific_attr(self):
        return self.link

class BulkProduct(Product):
    def __init__(self, name, price, quantity, supplier, reorder_level, weight, product_id=None):
        super().__init__(name, price, quantity, supplier, reorder_level, product_id)
        self.weight = weight
        self.type = "Bulk"

    def get_specific_attr(self):
        return self.weight