from odoo import models, fields, api

class SallaSettingsConfiguration(models.TransientModel):
    _inherit = 'res.config.settings'

    api_key = fields.Char(string="Salla API key")

    @api.model
    def get_values(self):
        res = super(SallaSettingsConfiguration, self).get_values()

        res['api_key'] = self.env['ir.config_parameter'].sudo().get_param('api_key')
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('api_key', self.api_key)
        res = super(SallaSettingsConfiguration, self).set_values()
        return res