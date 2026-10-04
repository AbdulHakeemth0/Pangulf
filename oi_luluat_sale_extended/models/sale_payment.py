# -*- coding: utf-8 -*-

from odoo import models, fields, api

    
class Sale(models.Model):
    _inherit = 'sale.order'
   
    amount_paid = fields.Float(compute='_get_amount_paid', string="Amount Received")
    balance = fields.Float(compute='_get_amount_paid',string="Balance")

    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        invoice_vals = super()._prepare_invoice()
        invoice_vals.update({
            'so_id': self.id,
        })

        return invoice_vals

    def _get_amount_paid(self):
        amount = 0
        balance = 0
        for record in self:
            pay_obj = self.env['account.payment'].search([('so_id','=',record.id),('state','=','posted')])
            if pay_obj:
                
                for each in pay_obj:
                    amount += each.amount
            record.amount_paid = amount
            record.balance = record.amount_total - amount


class sale_order_line(models.Model):
    _inherit = "sale.order.line"
    
    proforma_invoice = fields.Boolean('PI')
    
   
class Payment(models.Model):
   _inherit = 'account.payment'
   
   so_id = fields.Many2one('sale.order','Sale Order')


class AccountMove(models.Model):
   _inherit = 'account.move'
   
   so_id = fields.Many2one('sale.order','Sale Order')




class AccountPaymentRegisterInherit(models.TransientModel):
    _inherit = 'account.payment.register'

    so_id = fields.Many2one('sale.order','Sale Order',compute='_get_order')

    def _get_order(self):
        act_ids = self.env.context.get('active_ids', [])
        move_obj = self.env['account.move'].browse(act_ids)
        if act_ids:
            self.so_id = move_obj.so_id.id


    def _create_payment_vals_from_wizard(self, batch_result):
        payment_vals = super()._create_payment_vals_from_wizard(batch_result)
        payment_vals['so_id'] = self.so_id.id
        return payment_vals


