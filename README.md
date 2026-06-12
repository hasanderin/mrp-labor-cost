# mrp_labor_cost — Odoo 16 Custom Addon

Üretim Ürün Reçetesi (BoM) formuna TL cinsinden sabit işçilik maliyeti alanı ekler.
İşçilik tutarı PDF raporunda ve web Genel Bakış görünümünde ayrı satır olarak gösterilir ve Birim Maliyet toplamına dahil edilir.

---

## Yapı

```
mrp-labor-cost/               ← GitHub repo kök dizini
└── mrp_labor_cost/           ← Odoo addon (addons_path buraya eklenir)
    ├── __init__.py
    ├── __manifest__.py
    ├── models/
    │   ├── __init__.py
    │   ├── mrp_bom.py             ← labor_cost alanı
    │   └── mrp_bom_structure.py   ← _get_bom_data override
    ├── views/
    │   └── mrp_bom_views.xml      ← BOM form view
    ├── report/
    │   └── mrp_bom_report.xml     ← PDF QWeb template
    └── static/src/components/
        └── bom_overview_labor.xml ← OWL web Genel Bakış template
```

---

## Ne Yapar

### 1. Model — `models/mrp_bom.py`
`mrp.bom` modeli inherit edilerek `labor_cost` adında 2 ondalıklı float alan eklenir.
- Teknik ad: `labor_cost`
- Kullanıcıya görünen etiket: **İşçilik (₺)**
- Varsayılan: `0.0`

### 2. Form View — `views/mrp_bom_views.xml`
`mrp.mrp_bom_form_view` inherit edilir. Miktar satırının (`<div class="o_row">`) hemen altına **İşçilik (₺)** alanı eklenir.

> **XPath notu:** Odoo 16'da `product_qty` ve `product_uom_id` bir `<div class="o_row">` içinde birlikte yer alır. Bu nedenle `//field[@name='product_uom_id']` yerine `//div[hasclass('o_row')][field[@name='product_qty']]` hedef alınır; aksi hâlde alan etiket olmadan aynı satırda görünür.

### 3. PDF Raporu — `report/mrp_bom_report.xml`
`mrp.report_mrp_bom` template'i inherit edilir (wrapper olan `mrp.report_bom_structure` değil).

İki değişiklik yapılır:
- **Birim Maliyet** satırındaki BoM Maliyeti hücresi: `bom_cost / quantity` → `(bom_cost + labor_cost) / quantity`
- **İşçilik Maliyeti** satırı: Birim Maliyet satırının hemen üstüne eklenir, işçilik > 0 ise gösterilir.

PDF'de görünüm:
```
İşçilik Maliyeti  |  5.000,00 ₺
Birim Maliyet     |  8.829,39 ₺   ← işçilik dahil toplam
```

> **Template notu:** Odoo 16'da PDF raporunun asıl tablosu `mrp.report_mrp_bom` içindedir; `mrp.report_bom_structure` yalnızca wrapper'dır ve `<thead>` içermez.

### 4. Report Model — `models/mrp_bom_structure.py`
`report.mrp.report_bom_structure` abstract model override edilerek `_get_bom_data` metoduna `labor_cost` anahtarı eklenir. Bu sayede hem PDF QWeb template'i hem de OWL bileşeni bu değere erişebilir.

### 5. Web Genel Bakış — `static/src/components/bom_overview_labor.xml`
Odoo 16'da "Genel Bakış" butonu QWeb değil OWL tabanlı `mrp.BomOverviewTable` bileşenini açar. OWL template inheritance (`t-inherit`) kullanılır.

İki değişiklik yapılır:
- **İşçilik Maliyeti** satırı: `<tfoot>`tan önce `<tbody>` içinde eklenir, işçilik > 0 ise gösterilir.
- **Birim Maliyeti** hücresi: `bom_cost / quantity` → `(bom_cost + labor_cost) / quantity`

> **Template notu:** Doğru template adı `mrp.BomOverview` değil `mrp.BomOverviewTable`'dır.

---

## Kurulum

1. Repo'yu clone'la ya da `addons_path`'e ekle:
   ```
   /path/to/mrp-labor-cost
   ```
2. Odoo'yu yeniden başlat veya güncelle:
   ```bash
   odoo -u mrp_labor_cost -d <veritabanı_adı>
   ```
3. Uygulamalar menüsünden **MRP Labor Cost** modülünü yükle.

---

## Bağımlılıklar

- `mrp` (Odoo 16 Manufacturing)
- `uom` grubu için UoM (zaten mrp bağımlılığı içinde gelir)
