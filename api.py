#! /usr/bin/env python3
# coding: utf-8

import urllib.parse
import requests

def get_barcode():
    main_api = 'https://fr.openfoodfacts.org/'
    api_ending = '.json'

    barcode = input('> Type a barcode and press ENTER :')
    # barcode example : 3029330003533

    product_url = main_api + urllib.parse.urlencode({'/api/v0/produit/': barcode + api_ending})
    print('Request URL : ' + product_url)

    json_data = requests.get(product_url).json()
    # print(json_data)

    json_status = json_data['status_verbose']
    print('API Status : ' + json_status)

    brands_tags = json_data['product']['brands_tags'][0]
    generic_name_fr = json_data['product']['generic_name_fr']
    product_name_fr = json_data['product']['product_name_fr']
    print(f"Product : {generic_name_fr} \"{product_name_fr}\" de marque \"{brands_tags}\".")

get_barcode()
