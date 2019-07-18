"""
The Inventory Module
"""

class Inventory:
    """ The Inventory Class """
    def __init__(self, inventory={}):
        self._inventory = inventory

    def get_inventory(self):
        """ getter for the inventory """
        return self._inventory

    def set_inventory(self, inventory):
        """ setter for the inventory """
        self._inventory = inventory


class InventoryItem:
    """ The InventoryItem Class """
    def __init__(self, product_code, description, market_price, rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """ function to return as a dictionary """
        output = {}
        output['productCode'] = self.product_code
        output['description'] = self.description
        output['marketPrice'] = self.market_price
        output['rentalPrice'] = self.rental_price

        return output
