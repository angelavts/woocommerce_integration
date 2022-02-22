from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    wc_customer_id = fields.Integer()