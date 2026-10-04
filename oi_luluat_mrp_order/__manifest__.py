# -*- coding: utf-8 -*-
{
    'name': "Production Order",
    'author': "Oodu Implementers Pvt. Ltd",
    'website': "http://www.odooimplementers.com",
    'category': 'Stock',
    'version': '18.0',
    'depends': ['base', 'stock','mrp','oi_luluat_sale_order','oi_luluat_quot_with_pic','oi_luluat_quot_wo_pic'],
    'data': [
        'report/quot_report_view.xml',
        'report/quot_template_view.xml',
        'views/mrp_views.xml',
    ],
    
}
