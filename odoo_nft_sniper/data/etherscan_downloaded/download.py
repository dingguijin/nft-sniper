
class Download():
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


def main():
    _file = "../export-verified-contractaddress-opensource-license.csv"
    with open(_file, "rb") as _f:
        _f.readline()
        _f.readline()
        _lines = _f.readlines()
        for _line in _lines:
            _line = _line.decode("utf-8")
            _line = _line.replace("\"", "")
            x = _line.split(",")
            print(x[1])
            Download()._download_contract_source(x[1], ETHERSCAN_KEY)
    return


if __name__ == "__main__":
    main()
