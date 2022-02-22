# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError
from datetime import date
from woocommerce import API
from odoo import api
from odoo.addons.woocommerce_integration.models.tools import do_request

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
                print("Actualizar orden en woocommerce")
                data = {
                    "status": "completed"
                }
                response = do_request('PUT', 'orders', data, order.wc_order_id)              
        return res
