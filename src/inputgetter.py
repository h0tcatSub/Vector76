import sys
import cryptos

testnet = True
transaction_util = cryptos.Bitcoin(testnet=testnet)
inputs  = transaction_util.get_unspents(sys.argv[1])
print(inputs)