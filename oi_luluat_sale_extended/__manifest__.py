# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Extended',
    'version': '18.0',
    'author': 'Oodu Implementers Private Limited',
    'website': 'https://www.odooimplementers.com',
    'category': 'Sales',
    'summary': 'This module fetches total paid amount & balance against sale order',
    'description': """This module fetches total paid amount & balance against sale order""",
    'depends': ['base', 'sale'],
    'data': [
    # 'security/ir.model.access.csv',
    'views/sale_payment_view.xml',
    # 'views/sale_template_view.xml'
    ],
    'installable': True,
    'auto_install': False
}
