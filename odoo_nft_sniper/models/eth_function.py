import binascii

class EthFunction(object):
    def __init__(self):
        pass

    def find_functions(self, bytecode):
        bytecode = bytecode.strip()
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
                            #name = ''.join(map(chr, value))
                            #print(name)
                            print('Found function %s at offset %s' % (binascii.hexlify(value), offset))
                            functions.append((offset, binascii.hexlify(value)))
                            break
                i += 5
            elif 0x60 <= opcode and opcode < 0x80: # pushX
                i += opcode - 0x5f
            i += 1
        return functions


    
