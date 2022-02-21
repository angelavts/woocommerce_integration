# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError
from datetime import date
from woocommerce import API
from odoo import api
from odoo.addons.woocommerce_integration.models.tools import wcapi

class SaleOrderCustom(models.Model):
    _inherit = 'sale.order'

    # campos agregados
    # Id de la orden en woocommerce
    wc_order_id = fields.Integer()
    # numero de orden en woocommerce
    wc_number = fields.Char(string='Order Number')


    def action_confirm(self):
        # acción que se realiza al confirmar un presupuesto
        res = super(SaleOrderCustom, self).action_confirm()
        for order in self:
            if order.wc_order_id:
                print(order.wc_order_key)
                print("Actualizar orden en woocommerce")
                data = {
                    "status": "completed"
                }
                try:
                    response = wcapi.put('orders/%s' % order.wc_order_id, data).json()      
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
