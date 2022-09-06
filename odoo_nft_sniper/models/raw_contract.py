# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class RawContract(models.Model):

    _name = "nft_sniper.raw_contract"
    _description = "Raw Contract"
    _rec_name = 'raw_contract_name'


    raw_contract_name = fields.Char('rawContractName', related='raw_contract_transaction_id.raw_transaction_contract_name')
    raw_contract_symbol = fields.Char('rawContractSymbol', related='raw_contract_transaction_id.raw_transaction_contract_symbol')

    raw_contract_address = fields.Char('rawContractAddress', related='raw_contract_receipt_id.raw_transaction_receipt_contract_address')
    
    raw_contract_abi = fields.Char('rawContractAbi')
    raw_contract_source_code = fields.Char('rawContractSourceCode')
    raw_contract_byte_code = fields.Char('rawContractByteCode')

    raw_contract_receipt_id = fields.Many2one('nft_sniper.raw_transaction_receipt')

    raw_contract_transaction_id = fields.Many2one('nft_sniper.raw_transaction')
    raw_contract_transaction_hash = fields.Char('rawContractTransactionHash')

    raw_contract_erc_std = fields.Char('rawContractErcStd')
    
    raw_contract_is_freemint = fields.Boolean('rawContractIsFreemint')

    raw_contract_is_erc20 = fields.Boolean(string='rawContractIsErc20', related='raw_contract_transaction_id.raw_transaction_is_erc20')
    raw_contract_is_erc721 = fields.Boolean(string='rawContractIsErc721', related='raw_contract_transaction_id.raw_transaction_is_erc721')

    raw_contract_image = fields.Image('rawContractImage')

    raw_contract_nft_parsed = fields.Boolean('rawContractNftParsed', default=False, index=True)

    @api.model
    def refresh(self):
        _receipts = self.env["nft_sniper.raw_transaction_receipt"]
        _verified = self.env["nft_sniper.raw_verified_contract"]
        _contract = self.env["nft_sniper.raw_contract"]

        _receipts_domain = [("raw_transaction_receipt_create_contract", "!=", True)]
        _receipt_rs = _receipts.search(_receipts_domain)
        if not _receipt_rs:
            return
        
        _verified_domain = []
        _verified_rs = _verified.search(_verified_domain)
        if not _verified_rs:
            return

        _verified_addresses = list(map(lambda x: x.contract_address, _verified_rs))
        _verified_sources = dict(zip(_verified_addresses, _verified_rs))
        
        _sources = []
        for _receipt in _receipt_rs:
            if _receipt.raw_transaction_receipt_contract_address in _verified_addresses:
                _source = _verified_sources.get(_receipt.raw_transaction_receipt_contract_address)
                if not _source:
                    continue
                _receipt.raw_transaction_receipt_create_contract = True
                _sources.append(_source)

        for _source in _sources:
            _raw_contract.create({
                "raw_contract_name": _source.contract_name,
                "raw_contract_address": _source.contract_address,
                "raw_contract_source_code": _source.contract_source,
                "raw_contract_transaction_hash": _source.tx_hash,
                "raw_contract_abi": _source.contract_abi                
            })
        return
