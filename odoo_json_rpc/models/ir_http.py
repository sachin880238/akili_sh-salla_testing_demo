# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

import logging
import werkzeug
import json
from odoo.http import request
from odoo import models
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

class ir_http(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _find_handler(cls, return_rule=False):
        return 


    @classmethod
    def _dispatch(cls):
        if request.uid:
            request.uid = None
        func = None
        jsonrpctoken_enabled = False
        # try:
        #     func, arguments = cls._find_handler()
        #     jsonrpctoken_enabled = func.routing.get('jsonrpctoken', False)
        # except werkzeug.exceptions.NotFound as e:
        jsonrpctoken_enabled = False

        token_id = None
        token_res = None
        if jsonrpctoken_enabled:
            token = None
            post=json.loads(request.httprequest.data)
            # if request.params.has_key('token'):
            if 'token' in post and post['token']:
                token= post['token']
                post.pop('token')

            try:
                if not func.routing['type'] == 'json':
                    raise Exception(_("Can't use jsonrpc_tokens in non json-rpc route"))

                if not token or len(token) == 0:
                    raise Exception(_('Invalid token!'))
                token_id, token_res = request.env['jsonrpc.token'].sudo().check_token(token, request.httprequest.path)
                if not token_id:
                    raise Exception(_('Access Denied!'))
                request.uid = token_id.user_id.id
            except Exception as e:
                resp = cls._handle_exception(e)
                return resp

        resp = super(ir_http, cls)._dispatch()

        if jsonrpctoken_enabled and token_id:
            if token_res:
                token_res.increase_uses()
                token_id.increase_uses()
            if token_id.reg_remote_addr_uses:
                print (_("%s used this token in '%s'") %(request.httprequest.remote_addr, request.httprequest.path))
        return resp
