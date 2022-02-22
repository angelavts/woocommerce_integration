from odoo import models
from odoo.http import request
from werkzeug.exceptions import BadRequest



class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _auth_method_my_api_key(cls):
        api_key = request.httprequest.headers.get('Authorization')
        if not api_key:
            raise BadRequest('Authorization header with API key missing')

        user_id = request.env['res.users.apikeys']._check_credentials(
            scope='rpc', key=api_key
        )
        if not user_id:
            raise BadRequest('API key invalid')

        request.uid = user_id