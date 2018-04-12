#! /usr/bin/env python3
# coding: utf-8

import urllib.parse
import requests

def get_category():
    """
    This function sends a GET query to the openfoodfacts API
    with a category as a filter.
    Query response is a JSON file.
    Terminal prints API status and Category details.
    """
    main_api = 'https://fr.openfoodfacts.org/'
    api_ending = '.json'

    category = input('> Type a category name and press ENTER :')
    # barcode example : pizzas

    category_url = main_api + urllib.parse.urlencode({'category/': category + api_ending})
    print('Request URL : ' + category_url)

    json_data = requests.get(category_url).json()

    # json_status = json_data['status_verbose']
    # print('API Status : ' + json_status)

    for each in json_data['products']:
        print(each['product_name_fr'])


get_category()
