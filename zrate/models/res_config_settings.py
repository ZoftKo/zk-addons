from odoo import fields, models, _

import requests


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    zk_rate = fields.Boolean(
        string='Automatic USD exchange rates',
        readonly=False,
        related='company_id.zrate',
        help='USD to MXN exchange rates will be automatically updated every day with official data from DOF.'
    )
    banxico_token = fields.Char(
        string='Token',
        config_parameter='zrate.banxico_token',
        help='Token provided by Banxico to be able to use their API'
    )

    def test_token(self):
        self.ensure_one()
        try:
            r = requests.get(f'https://www.banxico.org.mx/SieAPIRest/service/sec/token/{self.banxico_token}/status')
            data = r.json().get('status', {})
            if data.get('activoOportuno', False) and data.get('activoHistorico', False):
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': _("Success. Valid token!"),
                        'type': 'success',
                        'sticky': False,
                    }
                }

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': _("Error. Invalid token!"),
                    'type': 'danger',
                    'sticky': False,
                }
            }
        except requests.exceptions.ConnectionError:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': _("Failed to connect to Banxico, couldn't check token."),
                    'type': 'danger',
                    'sticky': False,
                }
            }
