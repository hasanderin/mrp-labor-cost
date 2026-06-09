{
    'name': 'MRP Labor Cost',
    'version': '16.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Üretim Reçetesine İşçilik Maliyeti Alanı Ekler',
    'description': """
        Üretim Ürün Reçetesi (BoM) formuna TL cinsinden sabit işçilik maliyeti alanı ekler.
        İşçilik tutarı PDF raporunda ve web Genel Bakış görünümünde ayrı kolon olarak gösterilir.
    """,
    'author': 'Custom',
    'depends': ['mrp'],
    'data': [
        'views/mrp_bom_views.xml',
        'report/mrp_bom_report.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
