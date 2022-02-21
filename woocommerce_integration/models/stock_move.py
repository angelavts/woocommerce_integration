from odoo import models
from odoo.exceptions import AccessError
from odoo.addons.woocommerce_integration.models.tools import wcapi

class StockMove(models.Model):
    _inherit = "stock.move"
    def _action_done(self, cancel_backorder=False):
        print("Actualizar invenatio en woocommerce")
        moves = super(StockMove, self)._action_done()        
        for move in moves:
            # move.is_inventory and move.state == 'done' and
            if move.product_tmpl_id.is_wc_connect and move.product_tmpl_id.wc_id:
                print("Hacer PUT")
                # actualizar inventario en woocommerce
                data = {
                    "stock_quantity": str(move.product_tmpl_id.qty_available)
                    }
                # realizar la petición PUT para actualizar stock de producto
                try:
                    response = wcapi.put('products/%s' % move.product_tmpl_id.wc_id, data).json()
                except:
                    # posible error de conexión
                    response = False
                if response:
                    # revisar si existe data en la respuesta, lo cual
                    # es una posible indicación de error
                    data = response.get('data')
                    if data and data.get('status') != 200:
                        raise AccessError(_(response.get('message')))
                else:
                    raise AccessError(_("No fue posible establecer conexión con WooCommerce"))
        return moves