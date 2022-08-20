# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class RawTransaction(models.Model):

    _name = "nft_sniper.raw_transaction"
    _description = "Raw Transaction"

    _rec_name = 'raw_transaction_hash'
    
    raw_transaction_name = fields.Char('Name')
    raw_transaction_block_id = fields.Many2one('nft_sniper.raw_block', string="Block Id")
    
    raw_transaction_block_hash = fields.Char('blockHash')
    raw_transaction_block_number = fields.Char('blockNumber')
    raw_transaction_from = fields.Char('from')
    raw_transaction_gas = fields.Char('gas')
    raw_transaction_gas_price = fields.Char('gasPrice')
    raw_transaction_max_fee_per_gas = fields.Char('maxFeePerGas')
    raw_transaction_max_priority_fee_per_gas = fields.Char('maxPriorityFeePerGas')
    raw_transaction_hash = fields.Char('hash', index=True)
    raw_transaction_input = fields.Char('input')
    raw_transaction_nonce = fields.Char('nonce')
    raw_transaction_to = fields.Char('to')
    raw_transaction_transaction_index = fields.Char('transactionIndex')
    raw_transaction_value = fields.Char('value')
    raw_transaction_type = fields.Char('type')
    raw_transaction_access_list = fields.Char('accessList')
    raw_transaction_chain_id = fields.Char('chainId')
    raw_transaction_v = fields.Char('v')
    raw_transaction_r = fields.Char('r')
    raw_transaction_s = fields.Char('s')
    
    raw_transaction_create_receipt = fields.Boolean('createReceipt', default=False, index=True)
    raw_transaction_create_contract = fields.Boolean('createContract', default=False, index=True)
    
    raw_transaction_is_erc20 = fields.Boolean('isErc20')
    raw_transaction_is_erc721 = fields.Boolean('isErc721')
    
