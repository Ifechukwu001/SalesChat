#!/usr/bin/env python3
"""Module containing Cmd Workflow"""
import cmd
import models
from models.user import User
from models.product import Product


class SalesChatCLI(cmd.Cmd):
    """SalesChatCLI class"""

    intro = "SalesChat CLI Interface"
    prompt = "(SalesChat)$ "
    current_user = None

    def do_create(self, arg):
        """Creates a User - With params: email, password, phone"""
        args = arg.split()
        if len(args) < 4:
            print("Incomplete parameters")
            return
        if args[0] == "User":
            email, password, phone = args[1:4]
            if "@" not in email or not email.endswith(".com"):
                print("Invalid Email")
                return
            if len(models.storage.search("User", email=email)) > 0:
                print("Email already exists")
                return
            user = User(email, password, phone)
            models.storage.save()
            print("User has been created")
        else:
            print("Can only create Users")
    
    def do_login(self, arg):
        """Login as a user - With params: email, password"""
        args = arg.split()
        if len(args) < 2:
            print("Incomplete parameters")
            return
        email, password = args[:2]
        users = models.storage.search("User", email=email)
        if users and users[0].password == password:
            self.current_user = users[0]
            self.prompt = f"(SalesChat -> {email})$ "
        else:
            print("Invalid Email or Password")

    def do_logout(self, arg):
        """Logs out of SalesChat"""
        if self.current_user:
            self.current_user = None
            self.prompt = "(SalesChat)$ "

    def do_update_bank(self, arg):
        """Update the bank info - With params: acc_no, bank_name, sort_code"""
        args = arg.split()
        if len(args) < 3:
            print("Incomplete parameters")
            return
        account, bank, sort = args[:3]
        if self.current_user:
            self.current_user.update_bank_info(account, bank, sort)
            models.storage.save()
            print("User Bank info has been updated")
        else:
            print("Login first")

    def do_sell(self, arg):
        """Creates a product to sell -
        With params: name, desc, price, qty, category
        """
        args = arg.split()
        if len(args) < 5:
            print("Incomplete parameters")
            return
        name, desc, price, qty, category = args[:5]

        if self.current_user:
            if self.current_user.bank_id:
                desc = desc.replace("_", " ")
                if not price.isdigit() and not qty.isdigit():
                    print("Price and Qty must be numbers")
                    return
                price = int(price)
                qty = int(qty)

                if price <= 0:
                    print("Price should be greater than 0")
                    return
                if qty < 0:
                    qty = 0

                self.current_user.create_product(name, desc, price, qty, category)
                models.storage.save()
                print(f"Product '{name}' has been created")
            else:
                print("Add Bank information")
        else:
            print("Login First")

    def do_search(self, arg):
        """Searches for a product - With params: product_name"""
        args = arg.split()
        if len(args) < 1:
            print("Incomplete Parameters")
            return
        search_query = args[0]
        search_query = search_query.replace("_", " ")

        products = models.storage.search("Product", Product.name.contains(search_query))
        other_products = models.storage.search("Product", Product.description.contains(search_query))
        products.extend(other_products)
        products = list(set(products))
        i = 0
        p_no = -1
        while i < len(products):
            product = products[i]
            print(f"PRODUCT {i+1}")
            print("Name:", product.name)
            print("Price:", product.price)
            print()

            if (i and i % 3 == 0) or i == len(products) - 1:
                response = input("Enter Product number (nothing to continue search): ")
                if response.isdigit() and int(response) <= i + 1:
                    p_no = int(response) - 1
                    break
            i += 1
        if p_no >= 0:
            print(f"Here is the product ID - {products[p_no].id}")
        else:
            print("There is no more")

    def do_add_cart(self, arg):
        """Adds a product to the cart- With params: product_id qty"""
        args = arg.split()
        if len(args) < 2:
            print("Incomplete Parameters")
            return
        product_id, qty = args[:2]
        if self.current_user:
            qty = int(qty) if qty.isdigit() else 9999999
            product = models.storage.get("Product", product_id)
            if product:
                if product.is_available(qty):
                    cart_item = self.current_user.add_to_cart(product_id)
                    cart_item.quantity = qty
                    models.storage.save()
                    print(f"Product '{product.name}' ({qty}) "
                          "has been added to cart")
                else:
                    print(f"Product '{product.name} "
                          f"is only remaining {product.quantity}")
            else:
                print("Product ID is incorrect")
        else:
            print("Login First")

    def do_cart(self, arg):
        """Shows all the items in the cart"""
        if self.current_user:
            print("Cart Items:\n")
            for item in self.current_user.cart:
                product = models.storage.get("Product", item.product_id)
                print(f"Name: {product.name} (QTY: {item.quantity})")
        else:
            print("Login First")

    def do_checkout(self, arg):
        """Checks Out the cart"""
        if self.current_user:
            link = self.current_user.checkout()
            models.storage.save()
            if link:
                print(f"Proceed to this link for pay - {link}")
            else:
                print("No Items in the Cart")
        else:
            print("Login First")

    def do_EOF(self, arg):
        """Quits the program"""
        print("Quiting Program...")
        models.storage.save()
        return True

            
            



if __name__ == "__main__":
    SalesChatCLI().cmdloop()