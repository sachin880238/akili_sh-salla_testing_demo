from odoo import fields, models, api, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'


    shipping_product_id = fields.Many2one('product.product',string="Shiping type",readonly=True,compute="_compute_shipping_type",store=True)


    @api.depends('sale_id')
    def _compute_shipping_type(self):
        for rec in self:
            for line in rec.sale_id.order_line:
                if int(line.product_id.salla_id) in [1026614558,814202285,1492787992,1723506348]:
                    product_id = self.env['product.product'].search([('salla_id','=',line.product_id.salla_id)],limit=1)
                    if product_id:
                        rec.shipping_product_id=product_id.id
                        

