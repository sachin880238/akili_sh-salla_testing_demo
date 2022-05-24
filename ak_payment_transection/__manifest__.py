# -*- coding: utf-8 -*-
{
    'name': "Payment Transection",

    'summary': """
        It maps the payment transection and payment accounting.""",

    'description': """
        It maps the payment transection and payment accounting.
    """,

    'author': "Akili systems Pvt. Ltd.",
    'website': "http://www.akilisystems.in",
    'category': 'Product',
    'version': '14.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale','ak_add_field', 'payment', 'account'],

    # always loaded
    'data': [
    'views/sale_order_transection_customise.xml',
    'views/picking.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
