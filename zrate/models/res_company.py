from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    zrate = fields.Boolean(string="Enable ZoftKo's Automatic Exchange Rates functionality")
