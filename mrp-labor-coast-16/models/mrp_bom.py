from odoo import fields, models


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    labor_cost = fields.Monetary(
        string='İşçilik Maliyeti',
        currency_field='currency_id',
        default=0.0,
        help='Üretilen her birim için sabit işçilik maliyeti.',
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Para Birimi',
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
