# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class RawContract(models.Model):

    _name = "nft_sniper.raw_contract"
    _description = "Raw Contract"

    _rec_name = 'raw_contract_address'
    
    raw_contract_address = fields.Char('contractAddress')
    raw_contract_block_hash = fields.Char('blockHash')
    raw_contract_transaction_hash = fields.Char('transactionHash')

    raw_contract_is_erc721 = fields.Boolean('rawContractIsErc721', default=False)
    raw_contract_is_erc20 = fields.Boolean('rawContractIsErc20', default=False)
    raw_contract_erc_std = fields.Char('rawContractErcStd')

    raw_contract_abi = fields.Char('rawContractAbi')
    raw_contract_source = fields.Char('rawContractSource')
    
