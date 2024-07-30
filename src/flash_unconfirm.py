import argparse
import time
import requests
import subprocess
import cryptos
import hashlib
import uuid

import bitcoin.rpc

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="How To Use flash_unconfirm")

parser.add_argument("node_host",
                    help="your bitcoind node host name",
                    type=str)
parser.add_argument("node_port",
                    help="your bitcoind node host port",
                    type=int)
parser.add_argument("node_user",
                    help="your bitcoind node user name",
                    type=str)
parser.add_argument("node_password",
                    help="your bitcoind node password",
                    type=str)
parser.add_argument("send_from_wifkey",
                    help="Fake send btc from wif key.",
                    type=str)
parser.add_argument("fake_send_to",
                    help="Fake send btc to address.",
                    type=str)
parser.add_argument("amount_of_coins",
                    help="Amount of coins sent. (Enter in BTC units) The maximum amount delayed will vary depending on send_from.",
                    type=float)
parser.add_argument("--is_testnet",
                    "-test",
                    help="Testnet flag (Default=True)",
                    default=True,
                    type=bool)
parser.add_argument("--loop_count",
                    "-count",
                    help="How many fraudulent transactions to submit? If the balance is low, it may be possible to deceive the balance by sending it multiple times. (Default is 1.)",
                    default=1,
                    type=int)

def to_satoshi(btc_amount):
    satoshi = 0.00000001
    return round(btc_amount / satoshi)

def broadcast_transaction(raw_tx, testnet):

    url = "https://live.blockcypher.com/btc/pushtx"
    res = requests.get(url).text
    bs = BeautifulSoup(res, 'html.parser')
    csrf_token = bs.find(attrs={'name':'csrfmiddlewaretoken'}).get('value')
    print(csrf_token)
    if testnet:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = raw_tx
        payload = {"tx_hex": raw_tx,
               "coin_symbol": "btc-testnet",
               "csrfmiddlewaretoken": csrf_token}
    else:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {"tx_hex": raw_tx,
               "coin_symbol": "btc",
               "csrfmiddlewaretoken": csrf_token}

    response = requests.post(url,
                             allow_redirects=True,
                             data=payload,
                             headers=headers)
    print(f"response url : {response.url}")
    if response.status_code == 200:
        print("Transaction successfully broadcasted!")
    else:
        print(f"Failed to broadcast transaction. Status code: {response.status_code}")



args = parser.parse_args()
node_host        = args.node_host
node_port        = args.node_port
node_user        = args.node_user
node_password    = args.node_password

fake_send_from   = args.send_from_wifkey
victim_address   = args.fake_send_to
amount_btc = args.amount_of_coins
testnet    = args.is_testnet
loop_count = args.loop_count

if loop_count <= 0:
    loop_count = 1

transaction_util = cryptos.Bitcoin(testnet=testnet)
print("Connecting node.")
rpc_node = bitcoin.rpc.Proxy(f"http://{node_user}:{node_password}@{node_host}",
                             service_port=node_port)

print(rpc_node.getinfo())

balance = transaction_util.get_balance(transaction_util.wiftoaddr(fake_send_from))
inputs  = transaction_util.unspent(transaction_util.wiftoaddr(fake_send_from))
    #balance = transaction_util.get_balance(send_from)
if balance["confirmed"] <= 0:
    balance = balance["unconfirmed"]
else:
    balance = balance["confirmed"]


send_amount = to_satoshi(amount_btc)

if balance < send_amount:
    print(f"[!] insufficient funds. ")
    exit()

fee = 0
change_btc_amt = (balance - send_amount) - fee#おつり

input(" --- If you really want to continue, press enter. --- ")

for i  in range(loop_count):

    print(f"Fake Transaction {i}...")
    if testnet:
        tx_victim = [{"address": victim_address, "value": send_amount}, {"address": transaction_util.wiftoaddr(fake_send_from), "value": change_btc_amt}]
    else:
        tx_victim = [{"address": victim_address, "value": send_amount}, {"address": transaction_util.wiftoaddr(fake_send_from), "value": change_btc_amt}]

    tx_victim = transaction_util.mktx(inputs, tx_victim)
    print(tx_victim)
    if testnet:
        tx_victim = cryptos.serialize(transaction_util.sign(tx_victim, 0, fake_send_from))
    else:
        tx_victim = cryptos.serialize(transaction_util.sign(tx_victim, 0, fake_send_from))
    
    if i == 0:
        print()
        print("--------------------")
        print(f"Fake Send to                       : {victim_address}")
        print(f"Fake Send Amount (Satoshi unit)    : {send_amount} Satoshi")
        print(f"Signed  RawTx             : {tx_victim}")
        print(f"Testnet Mode              : {testnet}")
        print(f"Loop                      : {loop_count}")
        print("--------------------")
        print()
        print()

    print()

    print()
    print("Index > 強固なブロックチェーン技術に対して強制干渉を開始...")
    print()
    print("SND PRNT ITX (不正なトランザクションを 表示送信 !)")
    rpc_node.sendrawtransaction(tx_victim)
    print(tx_victim)
    print()
    #ゴリ押し
    print()
    #おまけ
    print("Kamijou Touma >> Kill that blockchain transaction!! 👊 💥 ")
    print()
    #print("What if you send the generated transaction using https://live.blockcypher.com/btc/pushtx/??")
    sound_name = "ImagineBreaker.mp3"
    try:
        import soundplay
        soundplay.playsound(sound_name)
    except:
        # Termux Only
        imagine_breaker_cmd = ["cvlc", "--play-and-exit", sound_name]
        subprocess.run(imagine_breaker_cmd)
    time.sleep(1) #休ませる

print("----------------")
print("Done.")