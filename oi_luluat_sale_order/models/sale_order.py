from odoo import api, fields, models


class SaleOrderIn(models.Model):
    _inherit = 'sale.order'

    payment_mode = fields.Many2one('payment.mode', string='Payment Mode')
    emp_master = fields.Many2one('hr.employee', string='Project Supervisor', domain="[('active', '=', True)]")
    total_discount_only = fields.Monetary(
        string='Total discount only',
        default=0.0,
        store=True,
        readonly=True,
        currency_field='currency_id',
        compute='_compute_total_discount_only',
    )
    total_tax_only = fields.Monetary(
        string='Total tax only',
        default=0.0,
        store=True,
        readonly=True,
        currency_field='currency_id',
        compute='_compute_total_tax_only',
    )
    enable_sign = fields.Boolean(string='Signature in Quotation', default=True)

    @api.depends('order_line.discount_amount', 'order_line.price_total')
    def _compute_total_discount_only(self):
        for rec in self:
            rec.total_discount_only = sum(
                line.price_total for line in rec.order_line if line.discount_amount
            )

    @api.depends('order_line.tax_id', 'order_line.price_tax')
    def _compute_total_tax_only(self):
        for rec in self:
            rec.total_tax_only = sum(
                line.price_tax for line in rec.order_line if line.discount_amount
            )


class PaymentMode(models.Model):
    _name = 'payment.mode'
    _description = 'Payment Mode'

    name = fields.Char(string='Name', required=True)


class RescompanyIn(models.Model):
    _inherit = 'res.company'

    footer = fields.Binary(string='Footer', attachment=True)
    sign = fields.Binary(string='Signature', attachment=True)
