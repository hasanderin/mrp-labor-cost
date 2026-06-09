from odoo import fields, models


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    iscilik_tutari = fields.Float(
        string='İşçilik (₺)',
        digits=(16, 2),
        default=0.0,
        help='Bu reçete için birim başına TL cinsinden sabit işçilik maliyeti.',
    )
