{
    'name': 'Sync Data from database',
    'summary': 'Sync data form another database. compatible for v8 and v11 to v15. Ok & Tested',
    'version': '15.0.1.0.8',
    'category': 'Tools',
    'price': 15.00,
    'currency': 'DOLLAR',
    'author': 'Akili Systems Pvt. Ltd.',
    'website': 'http://www.akilisystems.in',
    'depends': [
        'base','stock','sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/data_sync_view.xml',
        'wizards/data_sync_wizard_view.xml',
    ],
    'images': [
        'static/description/icon.png'
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}