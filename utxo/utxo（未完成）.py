class TXInput(object):   #输入
    def __init__(self,Txid,Vout,ScriptSig):
        self.Txid = Txid   #交易id
        self.Vout = Vout   #输出的编号
        self.ScriptSig = ScriptSig   #执行脚本
        
class TXOutput(object):   #输出
    def __init__(self,Value,ScriptPublickey):
        self.Value = Value   #金额
        self.ScriptPublickey = ScriptPublickey   #公钥

class Transaction(object):   #交易
    def __init__(self,ID,Vin,Vout)
        self.ID = ID   #交易hash
        self.Vin = Vin   #交易的输入（付款方）
        self.Vout = Vout   #交易的输出（收款方）

class Block(object):   #区块
    def __init__(self,Timestamp,Transactions,PrevBlockHash,Hash,Nonce):
        self.Timestamp = Timestamp
        self.Transactions = Transactions
        self.PrevBlockHash = PrevBlockHash
        self.Hash = Hash
        self.Nonce = Nonce

def HashTransactions():   #计算Hash值

def prepareData():   #挖矿前的准备

def IsCoinbase():   #判断是否为系统奖励

def CanUnlockOutputWith():   #判断是否可以解锁TXInput

def CanBeUnlockedWith():   #判断是否可以解锁TXOutput
    

def New_Transaction(self,from_addr,to_addr,amount):
    inputs = []
    outputs = []
    acc,valid_outputs = self._find_spendable_outputs(from_addr,amount)
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


