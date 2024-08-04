import json
import time
import argparse
import requests
import subprocess
import cryptos
import bitcoin
from bitcoinaddress import Wallet

sender = "mxx6ihPVErRHJyExAMYU4wEUBW5vRb7GR2"
transaction_util = cryptos.Bitcoin(testnet=True)
fake_inputs = transaction_util.unspent(sender)
outputs = [{"address": "msYdBVfTiF4VayDD639mJr2dk8cNVHzSXV", "value": 10000}]

tx = transaction_util.mktx(fake_inputs, outputs)
print(tx)
print()
tx = transaction_util.signall(tx, Wallet().key.testnet.wif)
tx["outs"][0]["script"] = tx["ins"][0]["script"]
#tx["ins"][1]["script"] = tx["outs"][1]["script"]
print(tx)
print(cryptos.serialize(tx))