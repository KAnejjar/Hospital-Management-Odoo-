odoo.define("mxs_pos_partner.buttons", function(require) {
    "use strict";

    var Screens = require('point_of_sale.screens');
    var core = require('web.core');
    var QWeb = core.qweb;
   
    Screens.ClientListScreenWidget.include({
        toggle_save_button: function(){
            var $button = this.$('.button.next');
            if (this.editing_client) {
                $button.addClass('oe_hidden');
                return;
            } else if( this.new_client ){
                if( !this.old_client){
                    $button.text(_t('Set Patient'));
                }else{
                    $button.text(_t('Change Patient'));
                }
            }else{
                $button.text(_t('Deselect Patient'));
            }
            $button.toggleClass('oe_hidden',!this.has_client_changed());
        },
    });
});