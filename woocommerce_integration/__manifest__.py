# -*- coding: utf-8 -*-
{
    'name': "woocommerce_integration",
    'summary': """Conecta la data desde odoo hasta woocomerce y viceversa""",
    'description': """Conecta la data desde odoo hasta woocomerce y viceversa""",
    'author': "Morales Argenis, Torrealba Angela, Castro Angelica",
    'category': 'Products',
    'version': '0.1',
    'depends': ['base','stock','sale','product'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/products_views.xml',
    ],
}