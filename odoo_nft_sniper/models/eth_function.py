import binascii
import logging
import qiling
from eth_utils import function_signature_to_4byte_selector

_logger = logging.getLogger(__name__)

def clean_bytecode(bytecode):
    if bytecode is None or bytecode == '0x':
        return None
    elif bytecode.startswith('0x'):
        return bytecode[2:]
    else:
        return bytecode

class EthFunction(object):
    def __init__(self):
        pass

    def find_name(self, bytecode):
        def get_function_sighash(signature):
            return '0x' + function_signature_to_4byte_selector(signature).hex()

        name_function_hash = get_function_sighash("name()")
        symbol_function_hash = get_function_sighash("symbol()")

        bytecode = bytecode.strip()
        if bytecode[:2] != "0x":
            bytecode = "0x" + bytecode
        ql = qiling.Qiling(archtype="evm", code=bytecode)
        user_account = ql.arch.evm.create_account(balance=100*10**18)
        contract_account = ql.arch.evm.create_account()
        try:
            msg = ql.arch.evm.create_message(user_account, b'', gas=5000000, code=bytecode, contract_address=contract_account)
            ret = ql.run(code=msg)
        except Exception as e:
            _logger.error("Evm error [%s]" % e)
            _logger.info("[%s]" % bytecode)
            return None
        
        if ret.is_error:
            _logger.error("Create contract meets error: [%s]" % ret.error)
            return None

        def _decode_return_string(output):
            if len(output) != 96:
                _logger.error("output length error: [%s]" % output)
                return ""
            # 000000002/00000000length/XXXXX00000000
            _last_piece = output[64:]
            _str = []
            for i in _last_piece:
                if i == 0:
                    break
                _str.append(chr(i))
            _str = "".join(_str)
            return _str

        try:
            msg = ql.arch.evm.create_message(user_account, contract_account, name_function_hash)
            ret = ql.run(code=msg)
        except Exception as e:
            _logger.error("Evm error %s" % e)
            return None
        
        if ret.is_error:
            _logger.error("Name meets error: [%s]" % ret.error)
            return None
        name = _decode_return_string(ret.output)
        
        msg = ql.arch.evm.create_message(user_account, contract_account, symbol_function_hash)
        ret = ql.run(code=msg)
        if ret.is_error:
            _logger.error("Symbol meets error: [%s]" % ret.error)
            return None
        symbol = _decode_return_string(ret.output)

        _logger.info("Find name: [%s:%s]" % (name, symbol))
        return {"name": name, "symbol": symbol}
    
    def find_functions(self, bytecode):
        bytecode = bytecode.strip()
        bytecode = clean_bytecode(bytecode)
        if not bytecode:
            return []
        
        code = binascii.unhexlify(bytecode)
        functions = []
        i = 0
        while i < len(code):
            opcode = code[i]
            if opcode == 0x63:  # push4
                value = code[i + 1:i + 5]
                # an awful heuristic below
                if i + 10 < len(code):
                    # (dup*), eq, push2, jumpi
                    # if re.match('.?\x14\x61..\x57', code[i:i + 10])
                    for off in range(2):
                        if code[i + off + 5] == 0x14 \
                           and code[i + off + 6] == 0x61 \
                           and code[i + off + 9] == 0x57:
                            offset = code[i + off + 7] * 256 + code[i + off + 8]
                            #_logger.info('Found function %s at offset %s' % (binascii.hexlify(value), offset))
                            functions.append((offset, binascii.hexlify(value)))
                            break
                i += 5
            elif 0x60 <= opcode and opcode < 0x80: # pushX
                i += opcode - 0x5f
            i += 1
        return functions
    
