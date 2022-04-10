import logging

from datetime import date, datetime
from typing import List

from bs4 import BeautifulSoup
from odoo import api, fields, models, _

import pytz
import requests

RESPONSE_DATE_FORMAT = r'%d/%m/%Y'

_logger = logging.getLogger(__name__)


def get_rates(token: str, date_start: date, date_end: date = False) -> List:
    get_rates.REQUEST_DATE_FORMAT = r'%Y-%m-%d'
    date_start = date_start.strftime(get_rates.REQUEST_DATE_FORMAT)
    if not date_end:
        date_end = date_start
    else:
        date_end = date_end.strftime(get_rates.REQUEST_DATE_FORMAT)

    r = requests.get(
        f'https://www.banxico.org.mx/SieAPIRest/service/v1/series/sf43718/datos/{date_start}/{date_end}',
        headers={'Bmx-Token': token}
    )
    r.raise_for_status()
    return r.json()['bmx']['series'][0]['datos']


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    banxico_enabled = fields.Boolean(string="Banxico's API", default=lambda self: self.env.company.zrate,
                                     readonly=True, store=False)

    @api.model
    def zk_update_rate(self):
        """
        Gathers today's rate. Scrapes DOF, it is not as clean as using Banxico, but it is much easier to obtain
        a correct result.
        """
        companies = self.env['res.company'].search([('zrate', '=', True)])
        if len(companies) < 1:
            return

        tz = self.env.ref('base.user_admin').tz
        if tz:
            today_date = datetime.now(pytz.timezone(tz)).date()
        else:
            today_date = date.today()
        # No official exchange rate on weekends.
        if today_date.weekday() > 4:
            return

        rates = self.env['res.currency.rate']
        usd_id = self.env.ref('base.USD').id
        try:
            dof_time = today_date.strftime('%d/%m/%Y')
            # Long live Mexican bureaucracy. Incomplete SSL chain so requests can't verify certificate.
            r = requests.get(
                'https://www.dof.gob.mx/indicadores_detalle.php',
                verify=False,
                params={'cod_tipo_indicador': 158, 'dfecha': dof_time, 'hfecha': dof_time}
            )
            r.raise_for_status()
            rate = float(BeautifulSoup(r.text, 'html.parser').select_one(
                'table.Tabla_borde tr:nth-of-type(2) td:nth-of-type(2)'
            ).text)

            for company in companies:
                current_rate = rates.search([
                    ('currency_id', '=', usd_id), ('company_id', '=', company.id), ('name', '=', today_date)
                ])
                if not current_rate:
                    rates.create([{
                        'name': today_date,
                        'inverse_company_rate': rate,
                        'currency_id': usd_id,
                        'company_id': company.id
                    }])
                else:
                    current_rate.write({'inverse_company_rate': rate})
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, AttributeError, Exception):
            _logger.exception('Exception when updating exchange rate. Notifying users.')

            mail_channel = self.env['mail.channel']
            odoo_bot = self.env.ref("base.partner_root").id
            users = [x.partner_id.id for x in self.env['res.users'].search([
                ('zk_rate_notification', '=', True),
                ('groups_id', 'in', self.env.ref('account.group_account_invoice').id)
            ])]
            for user in users:
                channel_info = mail_channel.channel_get([odoo_bot, user])
                channel = mail_channel.browse(channel_info['id'])
                message = _("ZoftKo's automatic MXN exchange rate update failed.<br/>"
                            "Please manually verify your currency rates.<br/>"
                            "Remember there is no rate on holidays, in which case failure is normal.")
                channel.sudo().message_post(
                    body=message,
                    author_id=odoo_bot,
                    message_type="comment",
                    subtype_xmlid="mail.mt_comment"
                )
