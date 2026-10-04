from odoo import api, models, fields
class SaleOrderIn(models.Model):
    _inherit = 'sale.order'
    quote=fields.Char(string='Quote No',related='origin')
    payment_mode=fields.Many2one('payment.mode',string='Payment Mode')
    emp_master=fields.Many2one('hr.employee',groups='hr.group_hr_user',string='Project Supervisor', domain="[('active', '=', True)]")
class PaymentMode(models.Model):
    _name='payment.mode'
    name=fields.Char(string='Name')
