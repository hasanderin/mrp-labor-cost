from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    labor_cost_unit = fields.Monetary(
        string='Birim İşçilik Maliyeti',
        currency_field='currency_id',
        compute='_compute_labor_costs',
        store=True,
    )
    labor_cost_total = fields.Monetary(
        string='Toplam İşçilik Maliyeti',
        currency_field='currency_id',
        compute='_compute_labor_costs',
        store=True,
    )
    material_cost_total = fields.Monetary(
        string='Toplam Malzeme Maliyeti',
        currency_field='currency_id',
        compute='_compute_labor_costs',
        store=True,
    )
    grand_total_cost = fields.Monetary(
        string='Genel Toplam Maliyet',
        currency_field='currency_id',
        compute='_compute_labor_costs',
        store=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        readonly=True,
    )

    @api.depends('bom_id', 'bom_id.labor_cost', 'product_qty', 'move_raw_ids',
                 'move_raw_ids.product_id', 'move_raw_ids.product_qty',
                 'move_raw_ids.product_id.standard_price')
    def _compute_labor_costs(self):
        for production in self:
            unit_labor = production.bom_id.labor_cost if production.bom_id else 0.0
            qty = production.product_qty or 1.0
            total_labor = unit_labor * qty

            material_cost = sum(
                move.product_id.standard_price * move.product_qty
                for move in production.move_raw_ids
                if move.product_id
            )

            production.labor_cost_unit = unit_labor
            production.labor_cost_total = total_labor
            production.material_cost_total = material_cost
            production.grand_total_cost = material_cost + total_labor
