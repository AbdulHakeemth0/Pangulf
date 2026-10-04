from odoo import api, models, fields
class SaleOrderInherit(models.Model):
    _inherit='sale.order'
    #note=fields.Text(string='Note')
