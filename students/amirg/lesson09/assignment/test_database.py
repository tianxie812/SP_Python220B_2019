"""
Tests the database module
"""
#pylint: disable=invalid-name
from unittest import TestCase
import database

class DatabaseTests(TestCase):
    """
    Tests for the database module
    """

    def setUp(self):
        '''
        Sets up database for each test
        '''
        mongo = database.MongoDBConnection()
        with mongo:
            db = mongo.connection.HPNortonDatabase
            products = db['products']
            customers = db['customers']
            rentals = db['rentals']

        products.drop()
        customers.drop()
        rentals.drop()


    def test_import_data(self):
        """
        Tests the import_data function
        """
        #directory_path = r"C:/Users/Amir G/SP_Python220B_2019/students/amirg/" \
        #                 r"lesson05/assignment/data"
        directory_path = r"data"
        tuple1, tuple2 = database.import_data(directory_path, 'products.csv',
                                              'customers.csv', 'rentals.csv')
        self.assertEqual(tuple1[0], 4)
        self.assertEqual(tuple1[1], 4)
        self.assertEqual(tuple1[2], 4)
        self.assertEqual(tuple2[0], 0)
        self.assertEqual(tuple2[1], 0)
        self.assertEqual(tuple2[2], 0)

        tuple3, tuple4 = database.import_data(directory_path, 'products.csv',
                                              'customers.csv', 'nothing.csv')
        self.assertEqual(tuple3[0], 4)
        self.assertEqual(tuple3[1], 4)
        self.assertEqual(tuple3[2], None)
        self.assertEqual(tuple4[0], 0)
        self.assertEqual(tuple4[1], 0)
        self.assertEqual(tuple4[2], 1)

    def test_show_available_products(self):
        """
        Tests the show_available_products module
        """
        #directory_path = r"C:/Users/Amir G/SP_Python220B_2019/students/amirg/" \
        #                 r"lesson05/assignment/data"
        directory_path = r"data"
        database.import_data(directory_path, 'products.csv', 'customers.csv', 'rentals.csv')

        avail_products = database.show_available_products()
        output_dict = {'prd002':{'description':'L-shaped sofa',
                                 'product_type':'livingroom', 'quantity_available':'1'},
                       'prd003':{'description':'Bicycle',
                                 'product_type':'recreation', 'quantity_available':'4'},
                       'prd004':{'description':'Jacket',
                                 'product_type':'apparrel', 'quantity_available':'2'}}
        self.assertEqual(avail_products, output_dict)

    def test_show_rentals(self):
        """
        Tests the show_rentals module
        """
        #directory_path = r"C:/Users/Amir G/SP_Python220B_2019/students/amirg/" \
        #                 r"lesson05/assignment/data"
        directory_path = r"data"
        database.import_data(directory_path, 'products.csv', 'customers.csv', 'rentals.csv')
        rentals = database.show_rentals('prd002')
        rentals2 = database.show_rentals('prd005')
        rentals_dict = {'user001':{'name':'Elisa Miles', 'address':'4490 Union Street',
                                   'phone_number':'206-922-0882', 'email':'elisa.miles@yahoo.com'},
                        'user002':{'name':'Maya Data', 'address':'4936 Elliot Avenue',
                                   'phone_number':'206-777-1927', 'email':'mdata@uw.edu'}}
        rentals2_dict = {}
        self.assertEqual(rentals, rentals_dict)
        self.assertEqual(rentals2, rentals2_dict)
