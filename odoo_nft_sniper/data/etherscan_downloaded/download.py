import os
import time
import requests

class Download():
    def __init__(self, etherscan_key):
        self.etherscan_key = etherscan_key
        return

    def _action_url(self, contract_address, action):
        _url = "https://api.etherscan.io/api?module=contract"
        _url = "%s&action=%s&address=%s&apiKey=%s" % (_url, action,
                                                      contract_address, self.etherscan_key)        
        return _url
    
    def _download_contract_source(self, contract_address):
        _url = self._action_url(contract_address, "getabi")
        try:
            _abi = requests.get(_url)
        except Exception as e:
            print(e)
            return None, None
        
        _url = self._action_url(contract_address, "getsourcecode")
        try:
            _sourcecode = requests.get(_url)
        except Exception as e:
            print(e)
            return None, None
        return _abi, _sourcecode

    def _source_exists(self, contract_address):
        _abi = contract_address + ".abi"
        _source = contract_address + ".source"
        if os.path.exists(_abi) and os.path.exists(_source):
            return True
        return False

    def _save_source(self, contract_address, abi, source):
        _abi = contract_address + ".abi"
        _source = contract_address + ".source"
        with open(_abi, "wb") as _file:
            _file.write(abi.encode("utf-8"))
        with open(_source, "wb") as _file:
            _file.write(source.encode("utf-8"))
        return

def main():
    _etherscan_key = open(".etherscan.key").read()
    _file = "../export-verified-contractaddress-opensource-license.csv"
    _download = Download(_etherscan_key)
    with open(_file, "rb") as _f:
        _f.readline()
        _f.readline()
        _lines = _f.readlines()
        for _line in _lines:
            _line = _line.decode("utf-8")
            _line = _line.replace("\"", "")
            x = _line.split(",")
            print(x[1])
            if _download._source_exists(x[1]):
                continue
            
            _abi, _source = _download._download_contract_source(x[1])
            if not _abi:
                continue
            _abi = _abi.text
            _source = _source.text
            print(_abi)
            print(_source)
            time.sleep(0.3)
            _download._save_source(x[1], _abi, _source)
    return


if __name__ == "__main__":
    main()
