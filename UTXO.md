# UTXO :skull:
### Original：
https://blog.csdn.net/XYlittlework/article/details/115395099
https://www.jb51.net/article/249057.htm
https://github.com/liuchengxu/blockchain-tutorial/blob/master/content/part-4/transactions-1.md
### 一、UTXO解释
        UTXO（Unspent Transaction Outputs）是未花费的交易输出，它是比特币交易生成及验证的一个
    核心概念。交易构成了一组链式结构，所有合法的比特币交易都可以追溯到前向一个或多个交易的输出，这
    些链条的源头都是挖矿奖励，末尾则是当前未花费的交易输出。
        区块链用记账的方式记录比特币交易。每个区块由区块头和区块体组成，区块体中有账本，在账本上记
    录交易。如果交易特别多的话，计算过程会比较复杂，还很占内存。于是，中本聪提出UTXO，一种基于交易
    的记账方式，记录“之前剩余”和“现在剩余”的情况而不是每笔交易的具体情况。与基于账户的记账方式相比，
    UTXO在计算复杂度、存储空间等方面，都很占优势。
### 二、UTXO优点
    1.UTXO不能分割，只能被消耗，独立的数据结构大大减少了计算量。
    2.UTXO配合地址使用，具备天然的匿名性，保证了账户的安全。
    3.因为地址的存在，UTXO的销毁和产生，都可追溯，很难伪造。
    4.长期来看，UTXO的数据占用更小，而余额系统会越来越臃肿。
    由此来看，比特币不是具体的钱币，只是UTXO账单上的一个数。
