#! /usr/bin/env python3
# coding: utf-8

import urllib.parse
import requests

def get_category_list():
    """
    This function sends a GET query to the openfoodfacts API
    to get all the categories.
    Query response is a JSON file.
    """
    main_api = 'https://fr.openfoodfacts.org/categories.json'
    print('Request URL : ' + main_api)

    json_data = requests.get(main_api).json()

    # json_status = json_data['status_verbose']
    # print('API Status : ' + json_status)

    for each in json_data['tags']:
        print(f"category_id : {each['id']} \nname_fr : {each['name']} \nurl_fr : {each['url']}\n----------")


get_category_list()
