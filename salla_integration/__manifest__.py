{
	'name' : 'salla_integration',
	'summary' : """This module will add a record to store student details.""",
	'version' : '15.0.1.0.0',
	'author' : 'Akili Systems Pvt. Ltd. , Aman',
	 'company': 'Akili Systems Pvt. Ltd.',
    'website': 'https://www.akilisystems.in',
    'category': 'Tools',
    'depends': ['base','stock','sale_management','website_sale','ak_add_field','data_sync'],
    'data': [
        'security/ir.model.access.csv',
        'views/salla.xml',
        'views/create_records.xml',
        'views/salla_settings.xml'
        ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',

}





