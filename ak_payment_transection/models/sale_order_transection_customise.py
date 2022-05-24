from odoo import fields, models, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    transection_count = fields.Integer('Transection', default=0)
    transection_ids = fields.One2many("payment.transaction", 'sale_id', string='Transections')
    
    def action_view_transection(self):
        action = self.env["ir.actions.actions"]._for_xml_id("payment.action_payment_transaction")
        
        form_id = self.env.ref('payment.transaction_form').id

        transections = self.mapped('transection_ids')
        if len(transections) > 1:
            action['domain'] = [('id', 'in', transections.ids)]
        elif transections:
            form_view = [(self.env.ref('payment.transaction_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = transections.id
        return action
