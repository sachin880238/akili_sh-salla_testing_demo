from odoo import api, models, fields, _
import xmlrpc.client
import re




class Wizard(models.TransientModel):
    _name = "wizard.alert"
    _description = "wizard.alert"

    popup = fields.Text(string="Text")
    no_of_records = fields.Char(string="Records")