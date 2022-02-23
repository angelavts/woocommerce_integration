from odoo import models, _
from odoo.exceptions import AccessError
from odoo.addons.woocommerce_integration.models.tools import do_request

class StockMove(models.Model):
    _inherit = 'stock.move'
    def _action_done(self, cancel_backorder=False):
        moves = super(StockMove, self)._action_done()        
        for move in moves:
            # move.is_inventory and move.state == 'done' and
            if move.state == 'done' and move.product_tmpl_id.is_wc_connect and move.product_tmpl_id.wc_id:
                # actualizar inventario en woocommerce
                data = {
                    'stock_quantity': str(move.product_tmpl_id.qty_available)
                }
                # realizar la petición PUT para actualizar stock de producto
                response = do_request('PUT', 'products', data, move.product_tmpl_id.wc_id)
                if not response:
                    raise AccessError(_('No fue posible establecer conexión con WooCommerce'))
        return moves