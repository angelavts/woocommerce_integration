# -*- coding: utf-8 -*-

from odoo import models
from datetime import date
from woocommerce import API
from odoo import api


# LOCAL DATA(TEST)
LOCAL_KEY = "ck_04c7be916fe8a2cfc9a1d114a1896c4f9c5d2f62"
LOCAL_SECRET = "cs_63c03d4df8e7d03e0f9b49d19488295157c14403"
LOCAL_URL = "http://localhost/wordpress/"

# SERVER DATA
SERVER_KEY = "ck_da9d1afb7938fbc35035dbfaa9289dc681d4e208"
SERVER_SECRET = "cs_7e6a337cbafbefdc58d4f33449549371cbe2060a"
SERVER_URL = "http://argemtshop.com"

# conexión con la API

wcapi = API(
    url=LOCAL_URL,
    consumer_key=LOCAL_KEY,
    consumer_secret=LOCAL_SECRET,
    version="wc/v3"
)

class product_template_export(models.Model):
    _inherit = 'product.template'

    def export_to_woocommerce(self):
        productList = self.env['product.template'].search([])
        productList.search([], order='create_date', limit=10)
        for product in productList:
            export_product(product, wcapi)


def export_product(product, wcapi):

    data = {
        "name": product.name,
        "type": "simple",
        "regular_price": str(product.list_price),
        "description": str(product.description),
        "short_description": str(product.description),
        "categories": [
            {
                "id": 9
            }
        ],
        "sku": str(product.default_code)
    }
    response = wcapi.post("products" , data).json()
    