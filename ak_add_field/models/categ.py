from odoo import models, api, fields, _

class ProductCateg(models.Model):
    _inherit = 'product.category'

    salla_id = fields.Char('Salla Id')


class WesbiteProductCateg(models.Model):
    _inherit = 'product.public.category'

    salla_id = fields.Char('Salla Id')





