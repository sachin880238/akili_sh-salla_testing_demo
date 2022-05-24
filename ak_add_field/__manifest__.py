{
    'name': 'Add Fields Salla',
    'version': '14.0.1.0.0',
    'summary': """Add fields for store salla id""",
    'description': """"Add fields for store salla id.""",
    'category': 'Salla',
    'author': 'Akili Systems',
    'company': 'Akili Systems Pvt. Ltd',
    'website': "http://www.akilisystems.in",
    'depends': ['base','product','website_sale'],
    'data': [
        'views/categ_view.xml',
        'views/partner_view.xml',
        'data/product_pricelist.xml',
        'data/product_delivery.xml',
        'security/ir.model.access.csv'
        
    ],
    'images': [],
    'license': 'AGPL-3',
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
