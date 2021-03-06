""" This module imports .csv files and creates a relational database using MongoDB"""
import os
import csv
import time
import threading
import queue
from pymongo import MongoClient

class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

def import_customers(directory_name, customer_file, my_queue):
    """Brings in customer csv files, counts lines and adds to database"""
    local_start_time = time.time()
    customer_count = 0

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.store
        customer = database["customer"]
        customer.drop()

        initial_count = database.customer.count_documents({})

        with open(os.path.join(directory_name, customer_file)) as csvfile:
            customer_reader = csv.reader(csvfile, delimiter=',')
            for row in customer_reader:
                customer_count += 1
                customer_info = {"user_id": row[0], "name": row[1], "address": row[2],
                                 "phone_number": row[3], "email": row[4]}
                customer.insert_one(customer_info)

        final_count = database.customer.count_documents({})

    local_end_time = time.time()

    my_queue.put(('Customers', customer_count, initial_count, final_count,
                  local_end_time - local_start_time))

def import_products(directory_name, customer_file, my_queue):
    """Brings in products csv files, counts lines and adds to database"""
    local_start_time = time.time()
    products_count = 0

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.store
        products = database["products"]
        products.drop()

        initial_count = database.products.count_documents({})

        with open(os.path.join(directory_name, customer_file)) as csvfile:
            products_reader = csv.reader(csvfile, delimiter=',')
            for row in products_reader:
                products_count += 1
                products_info = {"product_id": row[0], "description": row[1],
                                 "product_type": row[2], "quantity_available": row[3]}
                products.insert_one(products_info)

        final_count = database.customer.count_documents({})

    local_end_time = time.time()

    my_queue.put(('Products', products_count, initial_count, final_count,
                  local_end_time - local_start_time))

def import_rentals(directory_name, customer_file, my_queue):
    """Brings in rental csv files, counts lines and adds to database"""
    local_start_time = time.time()
    rentals_count = 0

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.store
        rentals = database["rentals"]
        rentals.drop()

        initial_count = database.rentals.count_documents({})

        with open(os.path.join(directory_name, customer_file)) as csvfile:
            rentals_reader = csv.reader(csvfile, delimiter=',')
            for row in rentals_reader:
                rentals_count += 1
                rentals_info = {"product_id": row[0], "user_id": row[1], "rental_date": row[2],
                                "return_date": row[3]}
                rentals.insert_one(rentals_info)

        final_count = database.customer.count_documents({})

    local_end_time = time.time()

    my_queue.put((rentals_count, initial_count, final_count,
                  local_end_time - local_start_time))

if __name__ == '__main__':
    TOTAL_START_TIME = time.time()
    MY_QUEUE = queue.Queue()

    THREAD1 = threading.Thread(target=import_customers, args=('input_files', 'customers.csv',
                                                              MY_QUEUE))
    THREAD1.start()
    THREAD2 = threading.Thread(target=import_products, args=('input_files', 'products.csv',
                                                             MY_QUEUE))
    THREAD2.start()
    THREAD3 = threading.Thread(target=import_rentals, args=('input_files', 'rentals.csv',
                                                            MY_QUEUE))
    THREAD3.start()

    THREAD1.join()
    THREAD2.join()
    THREAD3.join()

    FIRST_DONE = MY_QUEUE.get()
    SECOND_DONE = MY_QUEUE.get()
    THIRD_DONE = MY_QUEUE.get()

    TOTAL_END_TIME = time.time()

    print(FIRST_DONE)
    print(SECOND_DONE)
    print(THIRD_DONE)
    print("Total time")
    print(TOTAL_END_TIME - TOTAL_START_TIME)
    