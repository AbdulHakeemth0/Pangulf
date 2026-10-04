# -*- coding: utf-8 -*-
{
    'name': "Tax Invoice",
    'author': "Oodu Implementers Pvt. Ltd",
    'website': "http://www.odooimplementers.com",
    'category': 'Sales',
    'version': '18.0',
    'depends': ['base','account','float_number_discount','oi_luluat_sale_order','sale_term','hr','oi_luluat_quot_with_pic','oi_luluat_quot_wo_pic','stock'],
    'data': [
        #'security/ir.model.access.csv',
        'report/quot_report_view.xml',
        'report/quot_template_view.xml',
        'views/inv_views.xml',
    ],
    
}
