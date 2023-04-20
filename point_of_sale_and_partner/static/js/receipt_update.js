odoo.define("mxs_pos_partner.receipt_update", function(require) {
    "use strict";

    var Screens = require('point_of_sale.screens');
    var core = require('web.core');
    var QWeb = core.qweb;
    Screens.ReceiptScreenWidget.include({
        get_receipt_render_env: function() {
            var order = this.pos.get_order();
            console.log("order",order); 
            console.log("medecin2--",order.attributes.client.medecin2);
            console.log("assurance2--",order.attributes.client.assurance2[1]);
            console.log("x_num",order.attributes.client.x_numCheque);
            console.log("patient_name",order.attributes.client.name);
            var x_numCheque = order.attributes.client.x_numCheque;  
           
            return {
                widget: this,
                pos: this.pos,
                order: order,
                receipt: order.export_for_printing(),
                orderlines: order.get_orderlines(),
                paymentlines: order.get_paymentlines(),
                x_numCheque : order.attributes.client.x_numCheque,
                medecin2 : order.attributes.client.medecin2[1],
                assurance2 : order.attributes.client.assurance2[1],
                patient_name : order.attributes.client.name,
            };
        },
    });
});