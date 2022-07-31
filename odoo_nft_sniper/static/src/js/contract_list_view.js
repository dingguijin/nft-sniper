odoo.define('nft_sniper.contract.tree', function(require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');

    var KanbanController = require('web.KanbanController');
    var KanbanView = require('web.KanbanView');

    var viewRegistry = require('web.view_registry');
    var rpc = require('web.rpc');
    
    function renderButton() {
        var self = this;
        if (this.$buttons) {
            this.$buttons.on('click', '.o_button_refresh_contract', function() {
                rpc.query({
                    model: self.modelName,
                    method: 'refresh',
                    args:[]
                }).then(function() {
                    self.trigger_up("reload");
                });
            });                           
        }
    }

    var ContractListController = ListController.extend({
        willStart: function() {
            console.log(this);
            this.buttons_template = 'ContractListView.buttons';
            return this._super.apply(this, arguments);
        },

        renderButtons: function() {
            this._super.apply(this, arguments);
            renderButton.apply(this, arguments);
        }        
    });

    var ContractListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: ContractListController,
        }),
    });
    
    viewRegistry.add('contract_list_view', ContractListView);
});
