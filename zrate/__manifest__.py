{
    'name': 'ZoftKo Rates',
    'summary': "Automatically update MXN to USD's exchange rate.",
    'author': 'ZoftKo',
    'website': 'https://github.com/ZoftKo',
    'category': 'Accounting',
    'version': '15.0.1.0.0',
    'depends': ['base_setup', 'account'],
    'external_dependencies': {
        'python': ['requests', 'bs4']
    },
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'wizard/update_rate_wizard_views.xml',
        'views/res_config_settings_views.xml',
        'views/res_currency_views.xml',
        'views/res_users_views.xml'
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'license': 'GPL-3'
}
