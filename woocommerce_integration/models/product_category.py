# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, AccessError
from odoo.addons.woocommerce_integration.models.tools import wcapi, do_request

class ProductCategory(models.Model):
	_inherit = 'product.category'

	is_wc_connect = fields.Boolean(string='Connect to Woocommerce', default=False)
	wc_id = fields.Integer()

	@api.onchange('is_wc_connect')
	def _onchange_is_wc_connect(self):
		if self.is_wc_connect:
			return {'warning': {
				'title': _('Warning'),
				'message': _('Connecting products to Woocommerce may take time to save changes.')
			}}

	def _get_data(self):
		return {
			'name': self.name,
			'parent': self.parent_id.wc_id,
		}

	@api.model
	def create(self, vals_list):
		# crea una nueva categoria
		categories = super(ProductCategory, self).create(vals_list)
		for category in categories:
			if category.is_wc_connect:
				if category.parent_id and not category.parent_id.wc_id:
					category.parent_id.write({'is_wc_connect': True})
				category.create_wc()
		return category


	def create_wc(self):
		# crea una nueva categoria en woocommerce
		response = do_request('POST', 'products/categories', self._get_data())
		if response:
			self.write({'wc_id': response.get('id')})


	def write(self, vals):
		# edita una categoria existente
		res = super(ProductCategory, self).write(vals)
		for category in self:
			if not {'wc_id'} <= vals.keys():
				if category.is_wc_connect and category.wc_id:
					response = do_request('PUT', 'products/categories', self._get_data(), category.wc_id)

				elif not category.wc_id and vals.get('is_wc_connect') == True:
					if category.parent_id and not category.parent_id.wc_id:
						category.parent_id.write({'is_wc_connect': True})
					category.create_wc()
		return res


	def unlink(self):
		# elimina una categoria
		wc_ids = [category.wc_id for category in self if category.is_wc_connect]
		res = super(ProductCategory, self).unlink()
		for wc_id in wc_ids:
			response = self._connect_to_wc(op='delete', wc_id=wc_id)
			response = do_request('DELETE', 'products/categories', wc_id=wc_id)
		return res