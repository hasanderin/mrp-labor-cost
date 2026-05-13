from odoo import fields, models


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

            # Toplam maliyete ekle
            data['cost'] = data.get('cost', 0.0) + labor
            data['bom_cost'] = data.get('bom_cost', 0.0) + labor

            # Tabloda ayrı satır olarak göster
            labor_row = {
                'prod_id': False,
                'prod_name': 'İşçilik Maliyeti',
                'prod_code': '',
                'quantity': qty,
                'uom': bom.product_uom_id.name if bom.product_uom_id else 'Adet',
                'prod_link': False,
                'type': 'labor',
                'cost': labor,
                'bom_cost': labor,
                'total': labor,
                'level': level + 1,
                'route_name': '',
                'route_detail': '',
                'availability_state': 'ok',
                'availability_display': '',
                'quantity_available': 0,
                'quantity_on_hand': 0,
                'free_qty': 0,
                'lead_time': False,
                'components': [],
                'attachment_ids': [],
            }
            data.setdefault('components', []).append(labor_row)

        return data
