#! /usr/bin/env python3
# coding: utf-8

import requests
import json
import os


class Json(object):
    def __init__(self):
        self.api_url = """https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=countries
    &tag_contains_0=contains&tag_0=france&tagtype_1=purchase_places
    &tag_contains_1=contains&tag_1=france&tagtype_2=languages
    &tag_contains_2=contains&tag_2=fran%C3%A7ais
    &sort_by=unique_scans_n&page_size=1000&axis_x=energy
    &axis_y=products_n&action=display&json=1"""
        self.is_local_json()

    def is_local_json(self):
        """
        Verifies if a local json is ready
        """
        if not os.path.isfile('data_base/json_openfoodfacts_db.json'):
            self.get_json_from_api_url()
        else:
            self.read_local_json()

    def get_json_from_api_url(self):
        """
        Retrieves data from api url
        """
        json_data = requests.get(self.api_url).json()
        self.write_json_file_in_local(json_data)

    def write_json_file_in_local(self, json_data):
        """
        Saves json database dump file on local disk
        """
        with open('data_base/json_openfoodfacts_db.json', 'w') as outfile:
            json.dump(json_data, outfile)

    @staticmethod
    def read_local_json():
        """
        Read json database dump file from local disk
        """
        if os.path.isfile('data_base/json_openfoodfacts_db.json'):
            with open('data_base/json_openfoodfacts_db.json') as json_data:
                raw_data = json.load(json_data)

                return raw_data
