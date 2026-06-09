from odoo import fields, models


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    labor_cost = fields.Float(
        string='Labor Cost (₺)',
        digits=(16, 2),
        default=0.0,
        help='Fixed labor cost per unit in TRY for this bill of materials.',
    )
