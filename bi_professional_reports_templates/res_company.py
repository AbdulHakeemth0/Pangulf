# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields

class res_company(models.Model):
    _inherit = "res.company"

    sale_template = fields.Selection([
            ('fency', 'Fency'),
            ('classic', 'Classic'),
            ('modern', 'Modern'),
            ('odoo_standard', 'Odoo Standard'),
        ], 'Sale', default='odoo_standard')
    purchase_template = fields.Selection([
            ('fency', 'Fency'),
            ('classic', 'Classic'),
            ('modern', 'Modern'),
            ('odoo_standard', 'Odoo Standard'),
        ], 'Purchase', default='odoo_standard')
    stock_template = fields.Selection([
            ('fency', 'Fency'),
            ('classic', 'Classic'),
            ('modern', 'Modern'),
            ('odoo_standard', 'Odoo Standard'),
        ], 'Stock', default='odoo_standard')
    account_template = fields.Selection([
            ('fency', 'Fency'),
            ('classic', 'Classic'),
            ('modern', 'Modern'),
            ('odoo_standard', 'Odoo Standard'),
        ], 'Account', default='odoo_standard')


class account_invoice(models.Model):
    _inherit = "account.move"

    paypal_chk = fields.Boolean("Paypal")
    paypal_id = fields.Char("Paypal Id")


    def invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        self.ensure_one()
        self.is_move_sent = True
        return self.env.ref('account.account_invoices').report_action(self)


class res_company(models.Model):
    _inherit = "res.company"

    bank_account_id = fields.Many2one('res.partner.bank', 'Bank Account')

class res_partner_bank(models.Model):
    _inherit = "res.partner.bank"

    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', size=24, change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", 'State')
    country_id = fields.Many2one('res.country', 'Country')
    swift_code = fields.Char('Swift Code')
    ifsc = fields.Char('IFSC')
    branch_name = fields.Char('Branch Name')


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def print_quotation(self):
        self.write({'state': "sent"})
        return self.env.ref('purchase.report_purchase_quotation').report_action(self)
