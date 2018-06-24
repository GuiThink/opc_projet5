#! /usr/bin/env python3
# coding: utf-8

from datetime import datetime
from data_base.database_connect import UseDatabase


class Save:
    """
    Saving process
    """
    def __init__(self):
        self.saving_choice = self.saving_choice()

    def saving_choice(self):
        """
        Saves the saving choice of user (yes or no)
        """
        while True:
            choice = input(">> Do you want to save this ? Type YES or NO and then press ENTER : \n").strip().lower()
            if choice in ("yes", "no"):
                return choice

    def save_substitute(self, chosen_product_id, pdct_id):
        """
        Process of saving the current substitute product into the history table
        """
        dt = datetime.now()

        with UseDatabase() as cursor:
            cursor.execute("INSERT INTO history (product_id, initial_product_id, date_time) "
                           "VALUES (%s, %s, %s)", (chosen_product_id, pdct_id, dt))

        print("\n>> Product saved.")
