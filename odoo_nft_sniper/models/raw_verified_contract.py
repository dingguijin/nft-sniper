# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class RawVerifiedContract(models.Model):

    _name = "nft_sniper.raw_verified_contract"
    _description = "Raw Verified Contract"

    _rec_name = 'contract_name'
    
    contract_address = fields.Char('ContractAddress', index=True)
    contract_name = fields.Char('ContractName')
    tx_hash = fields.Char('Txhash')
    
