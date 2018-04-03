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

    product_name = json_data['products'][0]['product_name_fr']
    # brands_tags = json_data['product']['brands_tags'][0]
    # generic_name_fr = json_data['product']['generic_name_fr']
    # product_name_fr = json_data['product']['product_name_fr']
    print(product_name)

get_category()
