import tkinter as tk
from tkinter import ttk, messagebox

# === Product & CartItem Classes ===
class Product:
    def __init__(self, pid, name, price):
        self.pid = pid
        self.name = name
        self.price = price

class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def subtotal(self):
        return self.product.price * self.quantity

# === Shopping Cart Class ===
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        for item in self.items:
            if item.product.pid == product.pid:
                item.quantity += quantity
                return
        self.items.append(CartItem(product, quantity))

    def remove_item(self, pid):
        self.items = [item for item in self.items if item.product.pid != pid]

    def total(self):
        return sum(item.subtotal() for item in self.items)

# === GUI Application ===
class ShoppingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shopping Cart - GUI Version (No JSON)")

        # Hardcoded products
        self.products = [
            Product(1, "Book", 100),
            Product(2, "Pen", 10),
            Product(3, "Notebook", 50)
        ]
        self.cart = ShoppingCart()

        # === Product List Frame ===
        self.product_frame = ttk.LabelFrame(root, text="Available Products")
        self.product_frame.grid(row=0, column=0, padx=10, pady=10)

        self.product_tree = ttk.Treeview(self.product_frame, columns=("Name", "Price"), show="headings", height=5)
        self.product_tree.heading("Name", text="Product")
        self.product_tree.heading("Price", text="Price")
        self.product_tree.pack()

        for p in self.products:
            self.product_tree.insert("", "end", iid=p.pid, values=(p.name, f"₹{p.price}"))

        # === Add to Cart Section ===
        add_frame = ttk.Frame(root)
        add_frame.grid(row=1, column=0, pady=5)

        ttk.Label(add_frame, text="Quantity:").grid(row=0, column=0)
        self.qty_var = tk.IntVar(value=1)
        qty_entry = ttk.Entry(add_frame, textvariable=self.qty_var, width=5)
        qty_entry.grid(row=0, column=1)

        ttk.Button(add_frame, text="Add to Cart", command=self.add_to_cart).grid(row=0, column=2, padx=10)

        # === Cart Display ===
        self.cart_frame = ttk.LabelFrame(root, text="Your Cart")
        self.cart_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

        self.cart_tree = ttk.Treeview(self.cart_frame, columns=("Item", "Qty", "Subtotal"), show="headings", height=5)
        self.cart_tree.heading("Item", text="Item")
        self.cart_tree.heading("Qty", text="Qty")
        self.cart_tree.heading("Subtotal", text="Subtotal")
        self.cart_tree.pack()

        ttk.Button(self.cart_frame, text="Remove Selected", command=self.remove_from_cart).pack(pady=5)
        self.total_label = ttk.Label(self.cart_frame, text="Total: ₹0")
        self.total_label.pack()

        # === Exit Button ===
        ttk.Button(root, text="Exit", command=self.root.quit).grid(row=2, column=0, columnspan=2, pady=10)

        self.refresh_cart()

    def add_to_cart(self):
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showwarning("Please select a product", "No product selected.")
            return
        pid = int(selected[0])
        qty = self.qty_var.get()
        if qty <= 0:
            messagebox.showerror("Invalid quantity", "Quantity must be greater than zero.")
            return

        product = next((p for p in self.products if p.pid == pid), None)
        if product:
            self.cart.add_item(product, qty)
            self.refresh_cart()

    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning("Select item", "No item selected.")
            return
        pid = int(selected[0])
        self.cart.remove_item(pid)
        self.refresh_cart()

    def refresh_cart(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        for item in self.cart.items:
            self.cart_tree.insert("", "end", iid=item.product.pid,
                                  values=(item.product.name, item.quantity, f"₹{item.subtotal()}"))
        self.total_label.config(text=f"Total: ₹{self.cart.total()}")

# === Run App ===
if __name__ == "__main__":
    root = tk.Tk()
    app = ShoppingApp(root)
    root.mainloop()
