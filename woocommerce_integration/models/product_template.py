# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError
from datetime import date
from woocommerce import API
from odoo import api
from odoo.addons.woocommerce_integration.models.tools import wcapi, do_request

class ProductTemplate(models.Model):
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
        templates = super(ProductTemplate, self).create(vals_list)
        for template in self:
            # para cada producto, revisar si este se encuentra conectado a woocommerce
            if template.is_wc_connect:
                # crear el producto en woocommerce
                if not template.create_wc_product():
                    raise AccessError(_("Error en la creación del producto, es posible que exista un problema de conexión con woocommerce"))
                    # producto NO creado con exito
                    print("Error en la creación del producto") 
        return templates


    def write(self, vals):
        # actualizar el producto en odoo
        res = super(ProductTemplate, self).write(vals)
        # en caso de que si esté contectado con woocommerce,
        # se actualiza también ahí
        print("Preguntar si el producto está conectado con woocommerce")
        for template in self:
            if template.is_wc_connect:
                print("Preguntar si el producto está tiene id de woocommerce")
                print(template.wc_id)
                if template.wc_id:
                    print("Actualizar producto en woocommerce")
                    # en caso de que tenga un id de woocommerce, es porque
                    # ya existe en woocommerce, entonces se hace un PUT
                    response = do_request('PUT', 'products', template.get_data(), template.wc_id)
                    if not response:
                        raise AccessError(_("Error en la actualización del producto, es posible que exista un problema de conexión con woocommerce"))
                else:
                    print("Crear producto en woocommerce")
                    # como el producto aún no está en woocommerce, se crea
                    if not template.create_wc_product():
                        raise AccessError(_("Error en la creación del producto, es posible que exista un problema de conexión con woocommerce"))
                        # producto NO creado con exito
                        print("Error en la creación del producto") 
        return res

    def unlink(self):
        print("ELIMINAR DE WOOCOMMERCEEEE")
        # eliminar producto de woocommerce
        is_wc_connect = self.is_wc_connect
        wc_id = self.wc_id
        res = super(ProductTemplate, self).unlink()
        if is_wc_connect and wc_id:
            print("ELIMINARRRRRRRRRR")
            do_request('DELETE', 'products', wc_id=wc_id)      
        return res

    def get_data(self):
        # armar estructura con los datos requeridos por woocommerce
        data_product = {
            "name": str(self.name),
            "regular_price": str(self.list_price),
            "description": str(self.description),
            'type': 'simple',
            "sku": str(self.default_code) 
        }     
        return data_product

    def export_to_woocommerce(self):
        updatedProducts = 0
        productList = self.env['product.template'].search([])
        productList.search([], order='create_date', limit=10)
        for product in productList:
            if product.create_wc_product(True):
                updatedProducts += 1
        print(str(updatedProducts) + 'exportados con éxito')
        return {'warning': {
                'title': _('Productos exportados'),
                'message': _(str(updatedProducts) + ' exportados con éxito.')
            }}


    def create_wc_product(self, ignoreDataStatus=False):

        data_product = self.get_data()
        # indicar que se debe manejar el stock
        data_product["manage_stock"] = "true"
        # inficar la cantidad de productos
        data_product["stock_quantity"] = self.qty_available
        # insertar la imagen en caso de que la tenga
        if self.wc_img_link:
            data_product["images"] = [
                {
                    "src": self.wc_img_link 
                }
            ]
        # realizar la petición post para incluir producto
        response = do_request('POST', 'products', data_product, self.wc_id)        
        if response:
            self.write({
                        'wc_id': response.get('id'),
                        'wc_permalink': response.get('permalink')
                    })
            # incluir imagen en caso de que la tenga
            images = response.get('images')
            if images:
                self.write({
                            'wc_img_link': images[0]["src"],
                        })
                
        return response



    


