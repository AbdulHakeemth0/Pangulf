# -*- coding: utf-8 -*-
{
    'name': "Purchase Order",
    'author': "Oodu Implementers Pvt. Ltd",
    'website': "http://www.odooimplementers.com",
    'category': 'Purchase',
    'version': '18.0',
    'depends': ['base', 'purchase','oi_luluat_sale_order','sale_term','purchase_line_discount','oi_luluat_quot_with_pic','oi_luluat_quot_wo_pic'],
    'data': [
        'report/quot_report_view.xml',
        'report/quot_template_view.xml',
        'views/purchase_views.xml',
    ],
    
}
