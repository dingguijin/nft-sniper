# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class RawTransactionReceipt(models.Model):

    _name = "nft_sniper.raw_transaction_receipt"
    _description = "Raw Transaction Receipt"

    _rec_name = 'raw_transaction_receipt_transaction_hash'
    
    raw_transaction_receipt_block_hash = fields.Char('blockHash')
    raw_transaction_receipt_block_number = fields.Char('blockNumber')
    raw_transaction_receipt_contract_address = fields.Char('contractAddress')
    raw_transaction_receipt_cumulative_gas_used = fields.Char('cumulativeGasUsed')
    raw_transaction_receipt_effective_gas_price = fields.Char('raw_transaction_receipt_effective_gas_price')
    
    raw_transaction_receipt_from = fields.Char('from')
    raw_transaction_receipt_gas_used = fields.Char('gasUsed')
    raw_transaction_receipt_logs = fields.Char('logs')
    raw_transaction_receipt_logs_bloom = fields.Char('logsBloom')
    raw_transaction_receipt_root = fields.Char('root')
    raw_transaction_receipt_to = fields.Char('to')
    raw_transaction_receipt_status = fields.Char('status')
    raw_transaction_receipt_type = fields.Char('type')

    
    raw_transaction_receipt_transaction_hash = fields.Char('transactionHash')
    raw_transaction_receipt_transaction_index = fields.Char('transactionIndex')

    raw_transaction_receipt_create_contract = fields.Boolean('createContract')

    raw_transaction_receipt_transaction_id = fields.Many2one('nft_sniper.raw_transaction')
    raw_transaction_receipt_block_id = fields.Many2one('nft_sniper.raw_block')

    
    raw_transaction_receipt_create_contract = fields.Boolean('createContract', default=False, index=True)
    raw_transaction_receipt_create_nft = fields.Boolean('createNft', default=False, index=True)
    
