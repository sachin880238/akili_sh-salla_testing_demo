# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, exceptions
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import DataSet
import json
import logging
_logger = logging.getLogger(__name__)
import decimal
from datetime import datetime ,timedelta



from math import radians, cos, sin, asin, sqrt


        #User api for create api
class ResUsers(models.Model):
    _inherit = 'res.users'


    @api.model
    def create_user(self,vals):
        if  not vals.get('login'):
            logging.info("-please send login--")
            return {'error': '-please send login--','status':'Failed'}
        if  not vals.get('name'):
            logging.info("-please send name--")
            return {'error': '-please send name--','status':'Failed'}
        user_obj = self.env['res.users']
        data={
            'login':vals.get('login'),
            'name':vals.get('name'),
            'password': vals.get('password'),
        }
        user_obj.create(data)
        logging.info("-User create--")
        return {'Success': 'User Create Done','status':'Done'}

        # Business API For Business create
class ResCompany(models.Model):
    _inherit = 'res.company'


    @api.model
    def create_business(self,vals):
        if  not vals.get('name'):
            logging.info("-please send name--")
            return {'error': '-please send name--','status':'Failed'}
        company_obj = self.env['res.company']
        data={
            'name':vals.get('name')
        }
        if vals.get('street'):
            data['street']=vals.get('street')
        if vals.get('street2'):
            data['street2']=vals.get('street2')
        if vals.get('city'):
            data['city']=vals.get('city')
        if vals.get('zip'):
            data['zip']=vals.get('zip')
        if vals.get('phone'):
            data['phone']=vals.get('phone')
        if vals.get('email'):
            data['email']=vals.get('email')
        if vals.get('website'):
            data['website']=vals.get('website')
        if vals.get('vat'):
            data['vat']=vals.get('vat')
        if vals.get('company_registry'):
            data['company_registry']=vals.get('company_registry')
        
        new_company_id=company_obj.sudo().create(data)
        if vals.get('user_id'):
            token_id, token_res = request.env['jsonrpc.token'].sudo().check_token(vals.get('token'), request.httprequest.path)
            user_id=self.env['res.users'].sudo().search([('id','=',int(vals.get('user_id')))])
            if user_id and token_id.user_id.id == user_id.id:
                user_id.sudo().write({'company_ids': [(4, new_company_id.id)] })         
                #user_id.write({'company_ids':[(4, [new_company_id.id])]})
        logging.info("-User create--")
        return {'Success': 'Business Create Done','status':'Done'}



        

        

