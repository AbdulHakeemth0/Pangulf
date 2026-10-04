from odoo import api, fields, models

class StockIn(models.Model):
    _inherit = 'stock.picking'

    delivery_type = fields.Selection([('partial', 'Partial'), ('full', 'Full')], string='Delivery Type')
    vehicle = fields.Many2one('fleet.vehicle', string='Vehicle Model')
    sale_order = fields.Many2one('sale.order', string='Sale Order No')
    driver = fields.Many2one('hr.employee', string='Driver')
    supervisor = fields.Many2one('res.users', string='Supervisor')
    customer_reference = fields.Char(string='Customer Reference')

    @api.onchange('vehicle', 'vehicle.driver_id', 'vehicle.manager_id')
    def _onchange_vehicle(self):
        if self.vehicle:
            if self.vehicle.driver_id:
                self.driver = self.vehicle.driver_id
        if self.vehicle:
            if self.vehicle.manager_id:
                self.supervisor = self.vehicle.manager_id

class FleetVehicleInherit(models.Model):
    _inherit = 'fleet.vehicle'


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
            rec.picking_ids.write({
                'sale_order': rec.id,
                'customer_reference': rec.client_order_ref,
            })
        return res
