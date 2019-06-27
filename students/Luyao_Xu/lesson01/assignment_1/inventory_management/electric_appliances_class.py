"""
This module contains definitions of Electric appliances.
"""
from .inventory_class import Inventory


class ElectricAppliances(Inventory):
    """
    Define Electric Appliances class
    """

    def __init__(self, product_code, description, market_price, rental_price,
                 brand, voltage):
        """
        Initialize the class
        :param product_code:
        :param description:
        :param market_price:
        :param rental_price:
        :param brand:
        :param voltage:
        """
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)

        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """
        Return class's metadata
        :return:
        """
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage
        return output_dict
