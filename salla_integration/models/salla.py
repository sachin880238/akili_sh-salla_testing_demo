from odoo import models, api, fields, _
from odoo.exceptions import UserError, ValidationError
import http.client
import json
import urllib.parse
import requests
from odoo.tools import float_compare, float_is_zero





class CustomersMapping(models.Model):

    _name = "customermap.customermap"
    _description = "Description"

    partner_id= fields.Many2one("res.partner", string="Partner ID")
    odoo_id= fields.Integer(string="Odoo ID")
    ecom_id= fields.Integer(string="E.Com ID")

class AttributeMapping(models.Model):

    _name = "attributemap.attributemap"
    _description = "Description"

    attribute_id= fields.Many2one("product.attribute", string="Attribute ID")
    odoo_id= fields.Integer(string="Odoo ID")
    ecom_id= fields.Integer(string="E.Com ID")

class AttributeValueMapping(models.Model):

    _name = "attributeval.attributeval"
    _description = "Description"

    attribute_value_id= fields.Many2one("product.attribute.value", string="Attribute Value ID")
    odoo_id= fields.Integer(string="Odoo ID")
    ecom_id= fields.Integer(string="E.Com ID")

class CategoryMapping(models.Model):

    _name = "categorymap.categorymap"
    _description = "Description"

    category_id= fields.Many2one("product.public.category", string="Category ID")
    odoo_id= fields.Integer(string="Odoo ID")
    ecom_id= fields.Integer(string="E.Com ID")

class ProductTemplateMapping(models.Model):

    _name = "producttempmap.producttempmap"
    _description = "Description"

    product_template_id= fields.Many2one("product.template", string="Product Template ID")
    odoo_id= fields.Integer(string="Odoo ID")
    ecom_id= fields.Integer(string="E.Com ID")

class ProductMapping(models.Model):

    _name = "productmap.productmap"
    _description = "Description"

    product_id= fields.Many2one("product.product", string="Product ID")
    odoo_id= fields.Integer(string="Odoo ID")
    ecom_id= fields.Integer(string="E.Com ID")

class WebHooks(models.Model):

    _name = "web.hooks"
    _description = "Description"

    name= fields.Char(string="Name",required=True)
    url= fields.Many2one("webhooks.url", string="URL",required=True)
    user_id= fields.Many2one("res.users",string="User ID",required=True)
    # function_name= fields.Many2one("webhooks.url", string="Function Name")
    state=fields.Selection([('draft','Draft'),('posted','Posted')],string="State" ,default='draft')
    sala_id  = fields.Char(string="Salla ID")
    complete_url = fields.Char(string="Complete URL")

    logs = fields.One2many('webhooks.logs', 'name', string='Logs')


    def set_webhook(self):
        if self.state=='draft':
            if self.user_id:
                if self.user_id.access_token:
                    api_key = self.env['ir.config_parameter'].search([('key','=','api_key')])
                    if api_key.value:
                        
                        base_url = self.env['ir.config_parameter'].search([('key','=','web.base.url')])
                        str_url='"%s"' % (base_url.value+str(self.url.url)+"?user_id="+str(self.user_id.id)+"&token="+str(self.user_id.access_token))
                        name='"%s"' %self.url.name
                        function_name = '"%s"' %self.url.function_name
                        payload = "{\n  \"name\": "+name+",\n  \"event\": "+function_name+",\n  \"url\": "+str_url+",\n  \"version\": 2,\n  \"headers\": [\n    {\n      \"key\": \"Content-Type\",\n      \"value\": \"application/json\"\n    },\n    {\n      \"key\": \"Content-Length\",\n      \"value\": \"<calculated when request is sent>\"\n    }    ]\n}"
                        headers = {
                            'Content-Type': "application/json",
                            'Authorization': 'Bearer '+str(api_key.value)
                            }
                        conn = http.client.HTTPSConnection("api.salla.dev")
        
                        conn.request("POST", "/admin/v2/webhooks/subscribe", str(payload), headers)

                        res = conn.getresponse()
                        data = res.read()

                        return_data=json.loads(data.decode('utf-8'))
                        if return_data['success'] == True:
                            self.complete_url=str_url.strip('"')
                            self.sala_id=return_data['data']['id']
                            val={
                                
                                'request_type':'post',
                                'event_name':'active webhook',
                                'data':return_data['data'],
                                'status':'Success'
                            }
                            self.logs=[(0,0,val)]
                            

                            self.write({'state':'posted'})
                        

                    else:
                        raise UserError(_('Please Generate token for Selected user.'))
                else:
                    raise UserError(_('Please Generate token for Selected user.'))

    def set_draft(self):
        if self.state=='posted':
            api_key = self.env['ir.config_parameter'].search([('key','=','api_key')])
                    
            
            headers = {
                'Content-Type': "application/json",
                'Authorization': "Bearer "+api_key.value
                }
            safe_string = urllib.parse.quote_plus(self.complete_url)
            conn = http.client.HTTPSConnection("api.salla.dev")

            
            url="/admin/v2/webhooks/unsubscribe?id="+self.sala_id+"&url="+safe_string
            conn.request("DELETE", url, headers=headers)

            res = conn.getresponse()
            data = res.read()
            return_data=json.loads(data.decode('utf-8'))
            
            if return_data['success'] == True:
                val={
                    
                    'event_name':'Inactive Webhook',
                    'request_type':'post',
                    'data':return_data['data'],
                    'status':'Success'
                }
                self.logs=[(0,0,val)]

            self.write({'state':'draft'})


class WebHooksUrl(models.Model):
    _name = 'webhooks.url'
    _description = "Description"

    name = fields.Char(string="Name", required=True, readonly=True)
    url = fields.Char(string="URL", required=True, readonly=True)
    function_name = fields.Char(string="Function Name", required=True, readonly=True)
    

class WebHooksLogs(models.Model):
    _name = 'webhooks.logs'
    _description = "Description"

    name = fields.Many2one('web.hooks', string="name")
    request_type = fields.Selection([
        ('get', "GET"),
        ('post', "POST")], string="Requst Type", required=True, readonly=True)
    data = fields.Text(string="Data", required=True, readonly=True)
    event_name = fields.Char('Event')
    status = fields.Char('Status')


class AccountTax(models.Model):
    _inherit = 'account.tax'
    salla_id = fields.Integer("Salla ID")

    



class Stockinventory(models.Model):
    _inherit = 'stock.inventory'


    def custom_action_validate(self):
        if not self.exists():
            return
        self.ensure_one()
        # if not self.user_has_groups('stock.group_stock_manager'):
        #     raise UserError(_("Only a stock manager can validate an inventory adjustment."))
        if self.state != 'confirm':
            raise UserError(_(
                "You can't validate the inventory '%s', maybe this inventory "
                "has been already validated or isn't ready.", self.name))
        inventory_lines = self.line_ids.filtered(lambda l: l.product_id.tracking in ['lot', 'serial'] and not l.prod_lot_id and l.theoretical_qty != l.product_qty)
        lines = self.line_ids.filtered(lambda l: float_compare(l.product_qty, 1, precision_rounding=l.product_uom_id.rounding) > 0 and l.product_id.tracking == 'serial' and l.prod_lot_id)
        if inventory_lines and not lines:
            wiz_lines = [(0, 0, {'product_id': product.id, 'tracking': product.tracking}) for product in inventory_lines.mapped('product_id')]
            wiz = self.env['stock.track.confirmation'].create({'inventory_id': self.id, 'tracking_line_ids': wiz_lines})
            return {
                'name': _('Tracked Products in Inventory Adjustment'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'views': [(False, 'form')],
                'res_model': 'stock.track.confirmation',
                'target': 'new',
                'res_id': wiz.id,
            }
        self._action_done()
        self.line_ids._check_company()
        self._check_company()
        return True



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    weight = fields.Char('Weight')
    salla_id = fields.Integer("Salla ID")
    # is_tax_fixed = fields.Boolean()
    # custom_tax_amount= fields.Float()


    # @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    # def _compute_amount(self):
    #     """
    #     Compute the amounts of the SO line.
    #     """
    #     for line in self:
    #         price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
    #         taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
    #         if line.is_tax_fixed== False:
    #             line.update({
    #                 'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
    #                 'price_total': taxes['total_included'],
    #                 'price_subtotal': taxes['total_excluded'],
    #             })
    #         else:
    #             line.update({
    #                 'price_tax': line.custom_tax_amount,
    #                 'price_total': taxes['total_included'],
    #                 'price_subtotal': taxes['total_excluded'],
    #             })
    #         if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
    #             line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])




class SaleOrdermap(models.Model):

    _name = "sale.order.map"
    _description = "Description"

    sale_id= fields.Many2one("sale.order", string="Sale ID")
    odoo_id= fields.Integer(string="Odoo ID")
    ecom_id= fields.Integer(string="E.Com ID")

