from odoo import models, api, fields, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    salla_id = fields.Char('Salla Id')
    order_status_id = fields.Many2one('order.status')


class OrderStatus(models.Model):
    _name = 'order.status'

    salla_id = fields.Char('Salla Id')
    name   = fields.Char('Name')

