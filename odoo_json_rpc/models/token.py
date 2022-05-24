# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta
import os
import binascii
import logging

_logger = logging.getLogger(__name__)


class jsonrpc_tokens(models.Model):
    _name = 'jsonrpc.token'
    _description = "Json Token"
    _inherit = ['mail.thread']
    _rec_name = "user_id"
    _order = "write_date desc"
    _track = {
        'token': {},
        'user_id': {},
        'actived': {},
    }

    token = fields.Char(string='Token', size=128, unique=True, track_visibility='onchange')
    user_id = fields.Many2one('res.users', string='User', required=True, track_visibility='always')
    actived = fields.Boolean(string='Activated', default=True, track_visibility='always')
    reg_remote_addr_uses = fields.Boolean(string="Register Remote Address of Request", default=True,
                                          track_visibility='onchange')
    uses = fields.Integer(string="Uses", default=0)
    url = fields.Char(string="URL", size=128, required=True)

    def check_token(self, token, url):
        token_id = self.search([('token', '=', token), ('actived', '=', True)], limit=1)
        if not token_id:
            return (None, None)
        if token_id.url:
            clean_url = url.split('?')[0].lower()
            if clean_url == token_id.url.lower():
                return (token_id, token_id)
            return (None, None)
        return (token_id, None)

    
    def generate_token(self):
        for record in self:
            record.token = binascii.hexlify(os.urandom(32)).decode()

    
    def increase_uses(self):
        for record in self:
            record.uses += 1

    
    def increase_uses(self):
        for record in self:
            record.uses += 1

    @api.onchange('url')
    def onchange_url(self):
        self.uses = 0

    
    def remove_old_tokens_cron(self):
        # old_tokens = self.sudo().search([('create_date', '<', datetime.now() - timedelta(days=1))])
        old_tokens = self.sudo().search([('create_date', '<', datetime.now() - timedelta(hours=25))])
        if old_tokens:
            old_tokens.sudo().unlink()
        return True


