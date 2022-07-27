class Transaction(object):
    def __init__(self,vins,vouts):
        self.txid = ''
        self.vins = vins
        self.vouts = vouts

class TXOutput(object):
    def __init__(self,value,script_publickey):
        self.value = value   #一定量的比特币
        self.script_publickey = script_publickey   #一个锁定脚本，要花这笔钱，必须要解锁该脚本

def New_Transaction(self,from_addr,to_addr,amount):
    inputs = []
    outputs = []
    acc,valid_outputs = self.find_spendable_outputs(from_addr,amount)
    if acc < amount:
        print(u'not enough coin')
    for txid,outs in valid_outputs.items():
        for out in outs:
            out_index = out[0]
            input = TXInput(txid,out_index,from_addr)
            inputs.append(input)
    output = TXOutput(amount,to_addr)
    outputs.append(output)
    if acc > amount:
        outputs.append(TXOutput(acc-amount,from_addr))
    tx = Transaction(inputs,outputs)
    tx.set_td()
    return tx

def add_block(self,transactions):
    last_block = self.get_last_block()
    prev_hash = last_block.get_header_hash()
    height = last_block.block_header.height + 1
    block_header = BlockHeader('', height, prev_hash)
    block = Block(block_header, transactions)
    block.mine()
    block.set_header_hash()
    self.db.create(block.block_header.hash, block.serialize())
    last_hash = block.block_header.hash
    self.set_last_hash(last_hash)

def send(bc, from_addr, to_addr, amount):
    bc = BlockChain()
    tx = bc.new_transaction(from_addr, to_addr, amount)
    bc.add_block([tx])
    print('send %d from %s to %s' %(amount, from_addr, to_addr))
        
def get_balance(bc, addr):
    balance = 0
    utxos = bc.find_UTXO(addr)
    for utxo in utxos:
        balance += utxo.value
    print('%s balance is %d' %(addr, balance))


