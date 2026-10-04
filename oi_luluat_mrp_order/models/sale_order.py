from odoo import api, models, fields
class MoOrderInherit(models.Model):
    _inherit='mrp.production'
    note=fields.Text(string='Note')
