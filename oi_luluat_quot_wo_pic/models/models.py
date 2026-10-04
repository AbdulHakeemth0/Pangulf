# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Sale_order_inherit(models.Model):
    _inherit = 'sale.order'
    subject = fields.Text(string='Subject')
    content = fields.Text(string='Content')
class Res_Company_inherit(models.Model):
    _inherit = 'res.company'
    fax = fields.Char(string='Fax')
