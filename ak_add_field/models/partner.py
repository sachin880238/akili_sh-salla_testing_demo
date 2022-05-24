from odoo import models, api, fields, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    salla_id = fields.Char('Salla Id')

