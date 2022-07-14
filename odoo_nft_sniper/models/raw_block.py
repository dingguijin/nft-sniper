# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class RawBlock(models.Model):

    _name = "nft_sniper.raw_block"
    _description = "Raw Block"
    _rec_name = 'raw_block_hash'
    
    raw_block_name = fields.Char('Name')
    raw_block_base_fee_per_gas = fields.Char('baseFreePerGas')
    raw_block_difficulty = fields.Char('difficulty')
    raw_block_extra_data = fields.Char('extraData')
    raw_block_gas_limit = fields.Char('gasLimit')
    raw_block_gas_used = fields.Char('gasUsed')
    raw_block_hash = fields.Char('hash')
    raw_block_logs_bloom = fields.Char('logsBloom')
    raw_block_miner = fields.Char('miner')
    raw_block_mix_hash = fields.Char('mixHash')
    raw_block_nonce = fields.Char('nonce')
    raw_block_number = fields.Char('number')
    raw_block_parent_hash = fields.Char('parentHash')
    raw_block_parent_id = fields.Many2one('nft_sniper.raw_block')
    
    raw_block_receipts_root = fields.Char('receiptsRoot')
    raw_block_sha3_uncles = fields.Char('sha3Uncles')
    raw_block_size = fields.Char('size')
    raw_block_state_root = fields.Char('stateRoot')
    raw_block_timestamp = fields.Char('timestamp')
    raw_block_total_difficulty = fields.Char('totalDifficulty')
    raw_block_transactions = fields.One2many('nft_sniper.raw_transaction', 'raw_transaction_block_id', string="Transactions")
    raw_block_transactions_root = fields.Char('transactionsRoot')
    raw_block_uncles = fields.Char('uncles')
    #uncles_ids = fields.One2many('nft_sniper.raw_block')
