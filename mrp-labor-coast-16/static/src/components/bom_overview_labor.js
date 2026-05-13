/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { BomOverviewComponent } from "@mrp/components/bom_overview/mrp_bom_overview";

patch(BomOverviewComponent.prototype, "mrp_labor_cost.BomOverviewComponent", {
    /**
     * BoM datasından işçilik maliyetini döndürür.
     * Python _get_bom_data'dan gelen labor_cost_value alanını okur.
     */
    get laborCostValue() {
        return this.state.bomData?.labor_cost_value || 0;
    },

    get laborCostFormatted() {
        const cost = this.laborCostValue;
        if (!cost) return "";
        // Para birimi sembolünü al
        const currencies = this.env.services?.currency;
        const currencyId = this.state.bomData?.currency_id;
        if (currencies && currencyId) {
            const currency = currencies[currencyId];
            if (currency) {
                return `${currency.symbol} ${cost.toLocaleString("tr-TR", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                })}`;
            }
        }
        return `${cost.toLocaleString("tr-TR", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        })}`;
    },
});
