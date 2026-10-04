# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    discount_amount = fields.Float(string="Discount Amount", default=0.0, digits=(16, 2))
    discount_show = fields.Float(string="Discount (%)", default=0.0, digits=(16, 2))

    def _get_discount_base_amount(self):
        self.ensure_one()
        return (self.price_unit or 0.0) * (self.product_uom_qty or 0.0)

    def _update_discount_from_percent(self, percent):
        self.ensure_one()
        base_amount = self._get_discount_base_amount()
        self.update({
            "discount": percent,
            "discount_show": percent,
            "discount_amount": (base_amount * percent) / 100 if base_amount else 0.0,
        })

    @api.onchange("discount", "product_uom_qty", "price_unit")
    def _onchange_discount_sync_amount(self):
        if self.env.context.get("skip_discount_sync"):
            return
        self.with_context(skip_discount_sync=True)._update_discount_from_percent(self.discount or 0.0)

    @api.onchange("discount_amount")
    def _onchange_discount_amount(self):
        if self.env.context.get("skip_discount_sync"):
            return
        base_amount = self._get_discount_base_amount()
        percent = (self.discount_amount / base_amount) * 100 if base_amount else 0.0
        self.with_context(skip_discount_sync=True)._update_discount_from_percent(percent)

    @api.onchange("discount_show")
    def _onchange_discount_show(self):
        if self.env.context.get("skip_discount_sync"):
            return
        self.with_context(skip_discount_sync=True)._update_discount_from_percent(self.discount_show or 0.0)

    def _prepare_invoice_line(self, **optional_values):
        values = super()._prepare_invoice_line(**optional_values)
        values.update({
            "discount_amount": self.discount_amount,
            "discount_show": self.discount_show,
        })
        return values


class SaleOrder(models.Model):
    _inherit = "sale.order"

    discount = fields.Monetary(
        string="Discount",
        compute="_compute_discount_totals",
        store=True,
        readonly=True,
        currency_field="currency_id",
    )
    amount_without_discount_tax = fields.Monetary(
        string="Amount without Discount and Tax",
        compute="_compute_discount_totals",
        store=True,
        readonly=True,
        currency_field="currency_id",
    )

    @api.depends("order_line.discount_amount", "amount_untaxed")
    def _compute_discount_totals(self):
        for order in self:
            discount_total = sum(order.order_line.mapped("discount_amount"))
            order.discount = discount_total
            order.amount_without_discount_tax = order.amount_untaxed + discount_total


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    discount_amount = fields.Float(string="Discount Amount", default=0.0, digits=(16, 2))
    discount_show = fields.Float(string="Discount (%)", default=0.0, digits=(16, 2))

    def _get_discount_base_amount(self):
        self.ensure_one()
        return (self.price_unit or 0.0) * (self.quantity or 0.0)

    def _update_discount_from_percent(self, percent):
        self.ensure_one()
        base_amount = self._get_discount_base_amount()
        self.update({
            "discount": percent,
            "discount_show": percent,
            "discount_amount": (base_amount * percent) / 100 if base_amount else 0.0,
        })

    @api.onchange("discount", "quantity", "price_unit")
    def _onchange_discount_sync_amount(self):
        if self.env.context.get("skip_discount_sync"):
            return
        self.with_context(skip_discount_sync=True)._update_discount_from_percent(self.discount or 0.0)

    @api.onchange("discount_amount")
    def _onchange_discount_amount(self):
        if self.env.context.get("skip_discount_sync"):
            return
        base_amount = self._get_discount_base_amount()
        percent = (self.discount_amount / base_amount) * 100 if base_amount else 0.0
        self.with_context(skip_discount_sync=True)._update_discount_from_percent(percent)

    @api.onchange("discount_show")
    def _onchange_discount_show(self):
        if self.env.context.get("skip_discount_sync"):
            return
        self.with_context(skip_discount_sync=True)._update_discount_from_percent(self.discount_show or 0.0)


class AccountMove(models.Model):
    _inherit = "account.move"

    discount = fields.Monetary(
        string="Discount",
        compute="_compute_discount_totals",
        store=True,
        readonly=True,
        currency_field="currency_id",
    )
    amount_without_discount_tax = fields.Monetary(
        string="Amount without Discount and Tax",
        compute="_compute_discount_totals",
        store=True,
        readonly=True,
        currency_field="currency_id",
    )

    @api.depends("invoice_line_ids.discount_amount", "amount_untaxed")
    def _compute_discount_totals(self):
        for move in self:
            discount_total = sum(move.invoice_line_ids.filtered(lambda line: not line.display_type).mapped("discount_amount"))
            move.discount = discount_total
            move.amount_without_discount_tax = move.amount_untaxed + discount_total


