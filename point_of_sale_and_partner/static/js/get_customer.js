odoo.define('mxs_pos_partner.get_customer', function(require) {
    "use strict";
    
    var models = require('point_of_sale.models');
    models.load_fields("res.partner", ['x_numCheque','assurance2','medecin2']);
    models.load_fields("pos.medecin",['medecin']);
    models.load_fields("pos.assurance",['assurance']);
    var rpc = require('web.rpc');
    var core = require('web.core');
    var _t = core._t;
    var qweb = core.qweb;
    var web = require('web.data');
    var obj;
    
   
    var posmodel_super = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        get_all_medecs1: function(){
            var self = this;
            var all_medecs=[];
            rpc.query({
                model: 'res.partner',
                method: 'get_medecs',
            })
            .then(function (data_med) {
                self.data_med=data_med;
                all_medecs=data_med;
            }).fail(function (){
                console.error('Failed to load Data');
            });
            return self.data_med;
           
        },
        get_all_assur1: function(){
            var self=this;
            var all_assur=[];
            rpc.query({
                model: 'res.partner',
                method: 'get_assur',
            })
            .then(function (data_assur) {
               self.data_assur=data_assur;
               all_assur=data_assur;
            }).fail(function (){
                console.error('Failed to load Data');
            });
            return self.data_assur;
        },
      
        // get_medecss: function(){
        //     console.log("---------");
        //     this._model = 'res.partner';
        //     var x = this._model.call('get_medecs',[]).done(function(results){
        //     console.log("appel de get_medecss"); 
        //     console.log("x",x);   
        //     });
        //     console.log("--------------");
        //     return
        // },
   
        // get_assurance1: function(assur){
        //     return assur;
        // },
        get_x_numCheque1: function(num){
            console.log("inside of get assurance");
            return num;
        },
        // get_assurance:function(){
        //     return assurance;
        // },
        get_x_numCheque:function(){
            return x_numCheque;
        },
        get_assurance2:function(assur){
            return assur[1];
        },
        get_medecin2:function(medec){
            console.log("appel de get_medecin2", medec[1]);
            return medec[1];
        },
    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function() {
            _super_order.initialize.apply(this, arguments);
            if (this.pos.config.default_partner_id) {
            	this.set_client(this.pos.db.get_partner_by_id(this.pos.config.default_partner_id[0]));
            }
        },
        
    });
    
});