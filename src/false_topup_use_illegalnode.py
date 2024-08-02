import json
import time
import argparse
import requests
import subprocess
import cryptos
import bitcoin

from bitcoinaddress import Wallet
parser = argparse.ArgumentParser(description="How To Use fales_topup_use_illegalnode")
#parser.add_argument("send_from_wifkey",
#                    help="Fake send btc from wif key.",
#                    type=str)

parser.add_argument("fake_send_to",
                    help="Fake send btc to address.",
                    type=str)
#parser.add_argument("currency",
#                    help="Coin currency.  btc, ltc (Default=btc)",
#                    type=str,
#                    default="btc")
parser.add_argument("amount_of_coins",
                    help="Amount of coins sent. The maximum amount is 10 BTC",
                    type=float)

def to_satoshi(btc_amount):
    satoshi = 0.00000001
    return int(btc_amount / satoshi)

args = parser.parse_args()
fake_send_to = args.fake_send_to
amount_of_coins = to_satoshi(args.amount_of_coins)

wallet = Wallet()
fake_inputs = [{'tx_hash': "f" * 64, 'tx_pos': 0, 'height': 6730495, 'value': 1000200000, 'address': wallet.address.mainnet.pubaddr1}]

def generate_block(transaction_info):
    payload = json.loads(subprocess.run(f"bitcoin-cli decoderawtransaction {transaction_info}", shell=True))
    print(payload)
    print(f"bitcoin-cli generateblock {wallet.address.mainnet.pubaddr1} {payload}")
    subprocess.run(f"bitcoin-cli generateblock {wallet.address.mainnet.pubaddr1} {payload}",
                   shell=True)

def send_raw_transaction(rawtx):
    print(f"bitcoin-cli sendrawtransaction {rawtx}")
    return subprocess.run(f"bitcoin-cli sendrawtransaction {rawtx}",
                   shell=True).stdout
transaction_util = cryptos.Bitcoin(testnet=False)
fake_out = [{"address": fake_send_to, "value": amount_of_coins}]
tx = transaction_util.mktx_with_change(fake_inputs, fake_out, fee=20000)
tx = transaction_util.signall(tx, wallet.key.mainnet.wif)

print("--------------------")
print(f"Fake Send to                       : {fake_send_to}")
print(f"Fake Send Amount (Satoshi unit)    : {amount_of_coins} Satoshi")
print(f"Signed  RawTx (Serialized)         : {cryptos.serialize(tx)}")
print("--------------------")

input(" --- If you really want to continue, press enter. --- ")
print()
print("Index > 強固なブロックチェーン技術に対して強制干渉を開始...")
print()
time.sleep(3) #詠唱中...  -u- 

print("GEN IBLK PUB TOBC  (不正なブロックを生成、ブロックチェーンに公開!)")
time.sleep(2)

#send_raw_transaction(cryptos.serialize(tx))
print(generate_block(cryptos.serialize(tx)))

print()
print()
print("Kamijou Touma >> Kill that blockchain transaction!! 👊 💥 ")
print()
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

print("----------------")
balance = transaction_util.get_balance(fake_send_to)
print(f"victim : {fake_send_to}")
print(f"fake send to address Balance (satoshi unit) : {balance}")
print()
print("Done.")