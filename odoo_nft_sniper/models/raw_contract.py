# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class RawContract(models.Model):

    _name = "nft_sniper.raw_contract"
    _description = "Raw Contract"
    _rec_name = 'raw_contract_name'
    
    raw_contract_name = fields.Char('rawContractName')
    raw_contract_address = fields.Char('rawContractAddress')
    
    raw_contract_abi = fields.Char('rawContractAbi')
    raw_contract_source_code = fields.Char('rawContractSourceCode')
    raw_contract_transaction_hash = fields.Char('rawContractTransactionHash')

    raw_contract_erc_std = fields.Char('rawContractErcStd')
    
    raw_contract_is_freemint = fields.Boolean('rawContractIsFreemint')
    raw_contract_is_erc20 = fields.Boolean('rawContractIsErc20')
    raw_contract_is_erc721 = fields.Boolean('rawContractIsErc721')
    
