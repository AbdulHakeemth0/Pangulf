from odoo import api, models, fields
class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    enable_sign = fields.Boolean(string='Signature', default=True)
    proj_supervisor=fields.Many2one('hr.employee',string='Project Supervisor')
    pay_mode=fields.Many2one('payment.mode',string='Payment Mode')
    subj=fields.Char(string='Subject')
    cont=fields.Text(string='Content')
    driver=fields.Many2one('hr.employee',string='Driver')
    vehicle_no=fields.Char(string='Vehicle No')
    total_discount_only = fields.Monetary(string='Total discount only', default=0.0, store=True,readonly=True, currency_field='currency_id', compute='_compute_total_discount_only')
    total_tax_only = fields.Monetary(string='Total tax only', default=0.0, store=True,readonly=True, currency_field='currency_id', compute='_compute_total_tax_only')
    @api.depends('invoice_line_ids.tax_ids', 'invoice_line_ids.tax_amt')
    def _compute_total_tax_only(self):
        tax = 0
        for rec in self:
            for line in rec.invoice_line_ids:
                if line.discount_amount:
                    tax += line.tax_amt
            rec.total_tax_only = tax
            print ("lllllllllllllllllllllllllllllllllll",tax)

    @api.depends('invoice_line_ids.discount_amount', 'invoice_line_ids.price_total')
    def _compute_total_discount_only(self):
        disc = 0
        for rec in self:
            for line in rec.invoice_line_ids:
                if line.discount_amount:
                    disc += line.price_total
            rec.total_discount_only = disc
            print ("lllllllllllllllllllllllllllllllllll",disc)

class AMLInherit(models.Model):
    _inherit = 'account.move.line'
    tax_amt = fields.Monetary(string='Tax Amount',compute='_compute_price_tax', readonly=True, store=True)
    @api.depends('price_unit', 'tax_ids','discount', 'move_id','quantity', 'product_id', 'move_id.partner_id', 'move_id.currency_id')
    def _compute_price_tax(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            currency = line.move_id and line.move_id.currency_id or None
            if line.move_id:
                taxes = line.tax_ids.compute_all(price, currency, line.quantity, product=line.product_id, partner=line.move_id.partner_id)
                tax_amount = 0
                if taxes['total_included']:
                    tax_amount = taxes['total_included'] - taxes['total_excluded']
                line.tax_amt = tax_amount
                if line.move_id:
                    line.tax_amt = line.move_id.currency_id.round(line.tax_amt)



class SaleIn(models.Model):
    _inherit='sale.order'
    delivery_no=fields.Many2one('stock.picking',string='Delivery No') 
    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        invoice_vals = super()._prepare_invoice()
        invoice_vals.update({
            'so_id': self.id,
            'subj': self.subject,
            'proj_supervisor': self.emp_master.id,
            'cont': self.content,
            'pay_mode': self.payment_mode.id,
            'driver': self.delivery_no.driver.id,
            'vehicle_no': self.delivery_no.vehicle.license_plate,
            'account_term': self.sale_term,
        })

        return invoice_vals
'''
class SaleOrderLineInherit(models.Model):
    _inherit='sale.order.line'
    def _prepare_invoice_line(self, **optional_values):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        :param optional_values: any parameter that should be added to the returned invoice line
        """
        self.ensure_one()
        res = {
            'discount_amount': self.discount_amount,
            'discount_show': self.discount_show,
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'tax_amt':self.price_tax,
            'analytic_account_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
        }
        if optional_values:
            res.update(optional_values)
        if self.display_type:
            res['account_id'] = False
        return res
'''
class StockPickingInherit(models.Model):
    _inherit='stock.picking'
    def button_validate(self):
        res = super(StockPickingInherit, self).button_validate()
        for rec in self:
            if rec.origin:
                self.env['sale.order'].search([('name','=',rec.origin)]).delivery_no = rec.id
        return res
            
