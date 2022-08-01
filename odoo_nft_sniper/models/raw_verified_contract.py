# -*- coding: utf-8 -*-

import logging
import os
import requests

from odoo import api, fields, models, _

from . import download_contract_source

_logger = logging.getLogger(__name__)

class RawVerifiedContract(models.Model):

    _name = "nft_sniper.raw_verified_contract"
    _description = "Raw Verified Contract"

    _rec_name = 'contract_name'
    
    contract_address = fields.Char('ContractAddress', index=True)
    contract_name = fields.Char('ContractName')
    tx_hash = fields.Char('Txhash')

    contract_abi = fields.Char("ContractAbi")
    contract_source = fields.Char("ContractSource")

    contract_is_downloaded = fields.Boolean('ContractIsDownloaded', default=False, index=True)

    _sql_constraints = [
        ('contract_address_key', 'UNIQUE (contract_address)',  'You can not have two contract with the same address !')
    ]

    @api.model
    def download(self):
        _undownload = self.search([("contract_is_downloaded", "!=", True)])
        if not _undownload:
            return
        for _contract in _undownload:
            download_contract_source(_contract.contract_address)
        return
    
    @api.model
    def refresh(self):

        _all = self.search([]) or []
        _addresses = list(map(lambda x: x.contract_address, _all))
        _dir = os.path.abspath(os.path.dirname(__file__))
        _verified_file_path = os.path.join(_dir, "../data/export-verified-contractaddress-opensource-license.csv")
        with open(_verified_file_path, "rb") as _file:
            # ignore the first two lines
            _lines = _file.readline()
            _lines = _file.readline()
            _lines = _file.readlines()
            for _line in _lines:
                _line = _line.decode("utf-8")
                _line = _line.replace("\"", "")
                _line = _line.replace("'", "")
                _fs = _line.split(",")
                _fs = list(map(lambda x: x.strip(), _fs))
                if _fs[1] in _addresses:
                    continue
                self.create({
                    "tx_hash": _fs[0],
                    "contract_address": _fs[1],
                    "contract_name": _fs[2]
                })
        return


    """
    https://api.etherscan.io/api
    ?module=contract
    &action=getabi
    &address=0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413
    &apikey=YourApiKeyToken
    
    https://api.etherscan.io/api
    ?module=contract
    &action=getsourcecode
    &address=0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413
    &apikey=YourApiKeyToken 
    
    """

    def _action_url(self, contract_address, etherscan_api_key, action):
        _url = "https://api.etherscan.io/api?module=contract"
        _url = "%s&action=%s&address=%s&apiKey=%s" % (action, _url,
                                                      contract_address, etherscan_api_key)
        
        return _url
    
    def _download_contract_source(self, contract_address, etherscan_api_key):
        _url = self._action_url(contract_address, etherscan_api_key, "getabi")
        _abi = requests.get(_url)
        _url = _action_url(contract_address, etherscan_api_key, "getsourcecode")
        _sourcecode = requests.get(_url)
        return _abi, _sourcecode
