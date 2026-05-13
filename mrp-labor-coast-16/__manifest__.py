{
    'name': 'MRP Labor Cost',
    'version': '16.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Üretim Ürün Reçetesine İşçilik Maliyeti Alanı Ekler',
    'description': """
        Üretim Ürün Reçetesi (BoM) formuna sabit işçilik maliyeti (TL/adet) alanı ekler.
        Bu maliyet üretim emirlerinde ve PDF çıktılarında toplam maliyete dahil edilir.
    """,
    'author': 'Custom',
    'depends': ['mrp'],
    'data': [
        'views/mrp_bom_views.xml',
        'views/mrp_production_views.xml',
        'report/mrp_production_report.xml',
        'report/mrp_production_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'mrp_labor_cost/static/src/components/bom_overview_labor.js',
            'mrp_labor_cost/static/src/components/bom_overview_labor.xml',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
