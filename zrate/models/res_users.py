from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    zrate_notify = fields.Boolean(
        string='Notifications',
        help="Receive notifications when ZoftKo fails to update MXN exchange rates.",
        groups='account.group_account_invoice'
    )

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ['zrate_notify']

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ['zrate_notify']
