# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class RawContract(models.Model):

    _name = "nft_sniper.raw_contract"
    _description = "Raw Contract"
    _rec_name = 'raw_contract_name'
    
    raw_contract_name = fields.Char('rawContractName')
    raw_contract_abi = fields.Char('rawContractAbi')
    raw_contract_transaction_hash = fields.Char('rawContractTransactionHash')
    raw_contract_transaction_id = fields.Many2one('nft_sniper.raw_transaction')
    raw_contract_is_freemint = fields.Boolean('rawContractIsFreemint')
    
