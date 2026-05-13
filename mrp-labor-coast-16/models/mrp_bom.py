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

    def _get_bom_data(self, bom, product, qty=1.0, parent_bom=None,
                      product_info=False, ignore_stock=False):
        data = super()._get_bom_data(
            bom, product, qty=qty, parent_bom=parent_bom,
            product_info=product_info, ignore_stock=ignore_stock,
        )
        if bom and bom.labor_cost:
            labor = bom.currency_id._convert(
                bom.labor_cost * qty,
                self.env.company.currency_id,
                self.env.company,
                fields.Date.today(),
            )
            data['cost'] = data.get('cost', 0.0) + labor
            data['labor_cost'] = labor
        return data
