# -*- coding: utf-8 -*-
{
    'name': "Proforma Invoice",
    'author': "Oodu Implementers Pvt. Ltd",
    'website': "http://www.odooimplementers.com",
    'category': 'Sales',
    'version': '18.0',
    'depends': ['base', 'sale','float_number_discount','sale_quotation_number','hr','oi_luluat_sale_extended'],
    'data': [
        # 'security/ir.model.access.csv',
        'report/pi_report_view.xml',
        'report/pi_template_view.xml',
        # 'views/sales_views.xml',
        # 'views/custom_internal_layout.xml',
    ],
    
}
