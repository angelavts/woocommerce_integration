# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError
from datetime import date
from woocommerce import API
from odoo import api
from odoo.addons.woocommerce_integration.models.tools import wcapi

class sale_order_custom(models.Model):
    _inherit = 'sale.order'

    # campos agregados
    # Id del usuario en woocommerce
    wc_customer_id = fields.Integer()
    wc_number = fields.Char(string='Order Number')
    wc_order_key = fields.Char(string='Order Key')

    def action_confirm(self):
        res = super(sale_order_custom, self).action_confirm()
        print("SE ACABA DE CONFIRMAR UNA ORDEN!!!!")
        for order in self:
            if order.wc_order_key:
                print(order.wc_order_key)
                print("Actualizar orden en woocommerce")
                data = {
                    "status": "completed"
                }
                try:
                    response = wcapi.put('orders/%s' % order.wc_number, data).json()      
                except:
                    # posible error de conexión
                    response = False
                if response:
                    # revisar si existe data en la respuesta, lo cual
                    # es una posible indicación de error  
                    data = response.get('data')
                    if data and data.get('status') != 200:
                        raise AccessError(_(response.get('message')))
        return res
