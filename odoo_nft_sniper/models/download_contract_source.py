# -*- coding: utf-8 -*-

import requests
import logging

_logger = logging.getLogger(__name__)

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

def _action_url(contract_address, etherscan_api_key, action):
    _url = "https://api.etherscan.io/api?module=contract"
    _url = "%s&action=%s&address=%s&apiKey=%s" % (action, _url,
                                                  contract_address, etherscan_api_key)

    return _url

def download_contract_source(contract_address, etherscan_api_key):
    _url = _action_url(contract_address, etherscan_api_key, "getabi")
    _abi = requests.get(_url)
    _url = _action_url(contract_address, etherscan_api_key, "getsourcecode")
    _sourcecode = requests.get(_url)
    return _abi, _sourcecode
