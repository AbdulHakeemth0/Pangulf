from odoo import api, models, fields

class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'
    sale_order=fields.Many2one('sale.order',string= 'Sale Order No')
    proj_supervisor=fields.Many2one('hr.employee',string='Project Supervisor')
    note = fields.Text(string='Note')
    enable_sign=fields.Boolean(string='Signature', default=True)
    
  
