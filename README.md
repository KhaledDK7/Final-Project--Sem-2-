# Small Business Inventory Manager

A simple and intuitive desktop application for managing product inventory, stock levels, suppliers, and sales records.

## Description

The Small Business Inventory Manager is a Python-based GUI application designed to help small business owners track products, manage suppliers, and monitor stock levels. It provides functionality to add, view, and organize products (Perishable, Digital, and Bulk), with automatic low-stock alerts and expiry date tracking. Data is stored in a local SQLite database for reliability and includes JSON backup functionality.

Built with `Tkinter`, this application offers a clean, user-friendly interface and is entirely local—no internet or external cloud services required.

## Getting Started

### Dependencies

- Python 3.7 or later
- Tkinter (comes with Python standard library)
- SQLite3 (comes with Python standard library)
- OS: Windows, macOS, or Linux (with Python GUI support)

## Requirements

This app uses only Python's standard library. No additional packages are required.

### Executing program

1. Open a terminal or command prompt.
2. Initialize the database (first run only): python database.py
3. Run the graphical interface with: python gui_app.py
4. The main window will launch. From there, you can:
- Add new products (Perishable, Digital, or Bulk)
- View current stock and check for low inventory
- Record sales transactions
- Generate JSON backups of your data
- View "Low Stock" or "Expired" status indicators

## Help

If the app window doesn't appear or you receive a `TclError`, make sure your Python installation includes `Tkinter`.

If you see a "Database not found" error, ensure you have run `python database.py` once to initialize the `inventory.db` file in the same folder.

## Authors

Khaled Deek  
[@KhaledDK7](https://github.com/KhaledDK7)

## Version History

* 0.2
    * Added REST-like CLI commands
    * Added JSON backup serialization
    * Implemented Polymorphism for different product types (Perishable, Digital, Bulk)
* 0.1
    * Initial Release with product add/view/update functionality and SQLite integration