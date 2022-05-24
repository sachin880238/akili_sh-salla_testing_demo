from odoo import models, api, fields, _

class PromotionPromotion(models.Model):
    _name = 'promotion.promotion'


    name = fields.Char('Name')
    title = fields.Char('Title')
    sub_title = fields.Char('Sub Title')
    salla_id = fields.Char()
