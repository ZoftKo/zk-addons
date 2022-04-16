{
    'name': 'ZoftKo Web',
    'summary': 'Make Odoo responsive',
    'version': '15.0.1.0',
    'category': 'Website',
    'website': 'https://github.com/ZoftKo',
    'author': 'ZoftKo',
    'installable': True,
    'depends': ['web'],
    'data': ['views/web.xml'],
    'assets': {
        'web.assets_backend': [
            '/zflex/static/src/scss/side_chatter.scss',
            '/zflex/static/src/js/FullScreenButton.js',
        ]
    },
    'license': 'GPL-3',
}
