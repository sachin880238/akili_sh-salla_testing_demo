from odoo import models, fields, api, _
from datetime import date
import logging

class PaymentTransection(models.Model):
    _inherit = 'payment.transaction'

    sale_id = fields.Many2one('sale.order', string='Sale Order')

    @api.model
    def create(self, vals):
        logging.info("payment Transection Vals=====>>>%s",str(vals))
        customer_payment = self.env['account.payment']
        if 'partner_id' in vals:
            if vals['partner_id']:
                customer_payment_vals = {'partner_id': vals["partner_id"],
                                 'amount': vals["amount"],
                                 'date': date.today(),
                                 'currency_id':vals["currency_id"],
                                } 
                payment_id = customer_payment.create(customer_payment_vals)
                payment_id.write({'state': 'posted'})

                vals['payment_id'] = payment_id.id

        res = super(PaymentTransection, self).create(vals)
        
        sale_transection = self.env['sale.order'].search([('salla_id', '=', vals['reference'])])

        if sale_transection:
            sale_transection.transection_count = len(sale_transection)

        return res
