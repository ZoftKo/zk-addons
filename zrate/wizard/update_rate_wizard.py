from datetime import datetime, timedelta

from odoo import fields, models, _
from odoo.exceptions import UserError

from ..models.res_currency import get_rates, RESPONSE_DATE_FORMAT


class UpdateRateWizard(models.TransientModel):
    _name = 'zrate.update.wizard'
    _description = 'Wizard to update USD exchange rates'

    date_start = fields.Date(string='From', default=lambda self: fields.Datetime.now(), required=True)
    date_end = fields.Date(string='Up to', default=lambda self: fields.Datetime.now(), required=True)

    def update_rate(self):
        self.ensure_one()
        # Banxico rates are always one day ahead.
        banxico_start = self.date_start - timedelta(1)
        token = self.env['ir.config_parameter'].sudo().get_param('zrate.banxico_token')
        if not token:
            raise UserError(_('A Banxico token is needed. Please add it under the Invoicing settings.'))

        banxico_rates = get_rates(token, banxico_start, self.date_end)
        rates = self.env['res.currency.rate']
        usd_id = self.env.ref('base.USD').id
        for i in range(len(banxico_rates) - 1):
            # The next rate in the list has the rate of the day behind it, so we simply look ahead and use its date.
            rate = banxico_rates[i]
            next_rate = banxico_rates[i + 1]
            rate_date = datetime.strptime(next_rate['fecha'], RESPONSE_DATE_FORMAT).date()

            current_rate = rates.search([
                ('currency_id', '=', usd_id), ('name', '=', rate_date), ('company_id', '=', self.env.company.id)
            ])
            if not current_rate:
                rates.create([{
                    'name': rate_date,
                    'inverse_company_rate': rate['dato'],
                    'currency_id': usd_id,
                    'company_id': self.env.company.id
                }])
            else:
                current_rate.write({'inverse_company_rate': rate['dato']})
