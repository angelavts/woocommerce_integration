# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date
from woocommerce import API
from odoo import api
from odoo.addons.woocommerce_integration.models.tools import wcapi

class product_template_export(models.Model):
    _inherit = 'product.template'

    # campos agregados
    is_wc_connect = fields.Boolean(string="Connect to Woocommerce", default=False)
    wc_id = fields.Integer()
    wc_permalink = fields.Char(string='Permalink')
    wc_img_link = fields.Char(string='Woocommerce Image')
    
    @api.model_create_multi
    def create(self, vals_list):
        # crear el producto en woocommerce cuando se crea en odoo
        # primero crear en odoo
        templates = super(product_template_export, self).create(vals_list)
        for template in templates:
            # para cada producto, revisar si este se encuentra conectado a woocommerce
            if template.is_wc_connect:
                # crear el producto en woocommerce
                if not create_wc_product(template):
                    # producto creado con exito
                    print("Error en la creación del producto") 
        return templates



    def export_to_woocommerce(self):
        updatedProducts = 0
        productList = self.env['product.template'].search([])
        productList.search([], order='create_date', limit=10)
        for product in productList:
            if create_wc_product(product, True):
                updatedProducts += 1
        print(str(updatedProducts) + 'exportados con éxito')
        return {'warning': {
                'title': _('Productos exportados'),
                'message': _(str(updatedProducts) + ' exportados con éxito.')
            }}


def create_wc_product(product, ignoreDataStatus=False):
    # armar estructura con los datos requeridos por woocommerce
    data_product = {
        "name": product.name,
        "regular_price": str(product.list_price),
        "description": product.description,
        'type': 'simple',
        "sku": str(product.default_code) 
    } 
    # insertar la imagen en caso de que la tenga
    if product.wc_img_link:
        data_product["images"] = [
            {
                "src": product.wc_img_link 
            }
        ]
    # realizar la petición post para incluir producto
    try:
        response = wcapi.post("products", data_product).json()        
    except:
        # posible error de conexión
        response = False
    if response:
        # revisar si existe data en la respuesta, lo cual
        # es una posible indicación de error  
        data = response.get('data')
        if not ignoreDataStatus and data and data.get('status') != 200:
            raise AccessError(_(response.get('message')))
        else:
            product.write({
                        'wc_id': response.get('id'),
                        'wc_permalink': response.get('permalink')
                    })
            # incluir imagen en caso de que la tenga
            images = response.get('images')
            if images:
                product.write({
                            'wc_img_link': images[0]["src"],
                        })
            
    return response

