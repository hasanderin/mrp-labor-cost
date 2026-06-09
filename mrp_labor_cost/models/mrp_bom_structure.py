from odoo import models


class ReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'

    def _get_bom_data(self, bom, warehouse, product=False, line_qty=False,
                      bom_line=False, level=0, parent_bom=False,
                      index=0, product_info=False, ignore_stock=False):
        data = super()._get_bom_data(
            bom, warehouse, product=product, line_qty=line_qty,
            bom_line=bom_line, level=level, parent_bom=parent_bom,
            index=index, product_info=product_info, ignore_stock=ignore_stock,
        )
        data['labor_cost'] = bom.labor_cost if bom else 0.0
        return data
