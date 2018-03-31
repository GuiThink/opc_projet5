#! /usr/bin/env python3
# coding: utf-8

import urllib.parse
import requests

main_api = 'https://fr.openfoodfacts.org/'
api_ending = '.json'

barcode = input('> Type a barcode and press ENTER :')
# barcode example : 3029330003533

product_url = main_api + urllib.parse.urlencode({'/api/v0/produit/': barcode + api_ending})
print(product_url)

json_data = requests.get(product_url).json()
print(json_data)

# json_status = json_data['']
