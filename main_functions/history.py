#! /usr/bin/env python3
# coding: utf-8

from data_base.database_connect import UseDatabase


class History:
    """
    Class to manipulate history table
    """
    def __init__(self):
        self.get_saved_substitutes = self.get_saved_substitutes()
        self.get_saved_initial_products = self.get_saved_initial_products()
        self.print_history(self.get_saved_substitutes, self.get_saved_initial_products)

    def get_saved_substitutes(self):
        """
        Prints out substitute products saved by user
        """
        with UseDatabase() as cursor:
            cursor.execute("""SELECT product.product_id, product.product_name_fr,
                              product.product_nutrition_grade, product.product_url,
                              product.store_id, product.category_id, history.date_time,
                              history.initial_product_id
                              FROM product, category, history, store
                              WHERE product.product_id = history.product_id
                              AND product.store_id = store.store_id
                              AND product.category_id = category.category_id
                              ORDER BY history.date_time ASC
                              LIMIT 10""")

            data = cursor.fetchall()

        return data

    def get_saved_initial_products(self):
        """
        Prints out initial products saved by user
        """
        with UseDatabase() as cursor:
            cursor.execute("""SELECT product.product_name_fr, product.product_nutrition_grade
                              FROM product, history
                              WHERE product.product_id = history.initial_product_id
                              ORDER BY history.date_time ASC
                              LIMIT 10""")

            data = cursor.fetchall()

        return data

    def print_history(self, query1, query2):

        print("\n>> Your saved products : \n")

        i = 0
        while i < (len(query2)):
            for elem in query1:
                print(f"# date / time : {elem[6]} \n")
                print(f"\t## Your initial product : {query2[i][0]} "
                      f"\n\t\t# nutrition grade : {query2[i][1]} ")
                print(f"\n\t## Your substitute product : "
                      f"\n\t\t# barcode : {elem[0]} "
                      f"\n\t\t# substitute description : {elem[1]} "
                      f"\n\t\t# category : {elem[5]} "
                      f"\n\t\t# url : {elem[3]} "
                      f"\n\t\t# shop : {elem[4]} "
                      f"\n\t\t# nutrition grade : {elem[2]}\n "
                      f"\n ---------------------------------------------------------")
                i += 1
