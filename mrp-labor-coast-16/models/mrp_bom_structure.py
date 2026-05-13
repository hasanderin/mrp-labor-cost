from odoo import fields, models


class ReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'

    def _get_bom_data(self, bom, warehouse, product=False, line_qty=False,
                      bom_line=False, level=0, parent_bom=False, **kwargs):
        data = super()._get_bom_data(
            bom, warehouse, product=product, line_qty=line_qty,
            bom_line=bom_line, level=level, parent_bom=parent_bom, **kwargs
        )
        if level == 0 and bom and bom.labor_cost:
            qty = line_qty or bom.product_qty or 1.0
            bom_qty = bom.product_qty or 1.0
            factor = qty / bom_qty
            labor = bom.labor_cost * factor
            currency = data.get('currency') or self.env.company.currency_id
            if bom.currency_id != currency:
                labor = bom.currency_id._convert(
                    labor, currency, self.env.company, fields.Date.today()
                )
            data['cost'] = data.get('cost', 0.0) + labor
            data['bom_cost'] = data.get('bom_cost', 0.0) + labor
        return data
