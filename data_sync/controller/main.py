# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import binascii

from odoo import fields, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.osv import expression
from odoo import fields as odoo_fields, http, tools, _, SUPERUSER_ID
from odoo.tools import consteq
import uuid








class CustomerPortal(CustomerPortal):


    def _document_check_expense_access(self, model_name, document_id, access_token=None):
        document = request.env[model_name].browse([document_id])
        document_sudo = document.with_user(SUPERUSER_ID).exists()
        if not document_sudo:
            raise MissingError(_("This document does not exist."))
        try:
            document.check_access_rights('read')
            document.check_access_rule('read')
            
        except AccessError:
            if not access_token or not document_sudo.access_token or not consteq(document_sudo.access_token, access_token):
                raise
        return document_sudo



    @http.route(['/customer/update/<int:user_id>'], type='http', auth="public", website=True)
    def customer_update_page(self, user_id, report_type=None, access_token=None, message=False, download=False, **kw):
        print("===============================>>>")
        try:
            expense_id = self._document_check_expense_access('res.users', expense_id, access_token=user_id)
        except (AccessError, MissingError):
            values = {'expense_id':expense_id,'status':'already'}
            request.render('ak_expense_approval.expense_order_portal_template', values)
        if not isinstance(expense_id, int):

            values = {'expense_id':expense_id,'status':'accept'}
            token=str(uuid.uuid4())
            base_url = request.env['ir.config_parameter'].search([('key','=','web.base.url')])
            url=base_url.value+'/reject/expense/approval/'+str(expense_id.id)+'?access_token='+token
            expense_id.write({'state':'ceo','access_token':token,'access_url':url})

            return request.render('ak_expense_approval.expense_order_portal_template', values)
        else:
            values = {'status':'already'}
            request.render('ak_expense_approval.expense_order_portal_template', values)



    