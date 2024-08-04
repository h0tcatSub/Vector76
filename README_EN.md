# Investigating the Mystery Tool Fake Sender Flasher

It's common to see videos on YouTube where non-existent Bitcoin transactions are sent to exchanges to withdraw balances. Such videos are often scams to steal Bitcoin, Trojan Malware, or even if real, excessively expensive content.

By chance, I created a transaction with zero mining fees and sent it as a test. Temporarily, the unconfirmed balance was reflected. Of course, since it wasn't mined, the transaction remained unconfirmed. After some time, the transaction was erased, and the sent coins were returned.

Victims are mainly small retailers, online stores, and gambling sites that only manage balances. Exchanges and retailers should be wary of unconfirmed transactions.

**The following conditions are essential to execute the flash:**

- Private key of the address with coin balance (The amount that can be flashed depends on how much coin is prepared.)
- Temporary acceptance of broadcasts with zero mining fees
Why can a tool without a private key perform a flash? Possible explanations include:
- The developer securely manages the private key of an address with coins in advance and sends the private key to the app via communication to sign the transaction.

It's also possible that people and developers abusing Flasher are using more sophisticated techniques that aren't publicly known.

Additionally, people who abuse Flasher or developers might be using more advanced technology unknown to the public.

If you want to try it out, you can use flash_unconfirm.py.
It has been tested several times on the testnet but not confirmed on the mainnet.
If you seriously want to do this on the mainnet, be prepared for your account or address to be frozen.
For details, please refer to the disclaimer.

Moreover, instead of flashing, using the more efficient vector76 attack to cancel a single confirmation might be more effective for double-spending.


- 2024/8/4 Update: This might be used as a Spammer or Jammer to disrupt the operation of blockchain nodes rather than a Flasher. If you obtain a real Flasher from somewhere, reverse engineering and renewal are planned.


```
usage: flash_unconfirm.py [-h] send_from_wifkey fake_send_to blockcypher_token currency amount_of_coins

How To Use flash_unconfirm

positional arguments:
  send_from_wifkey   Fake send btc from wif key.
  fake_send_to       Fake send btc to address.
  blockcypher_token  blockcypher_apikey It might be possible to do it successfully with BTC.
  currency           Coin currency. btc, ltc (Default=btc)
  amount_of_coins    Amount of coins sent. The maximum amount delayed will vary depending on send_from.

options:
  -h, --help         show this help message and exit

```


# What is Double Spending? (Still experimenting...)

Vector76,   Roughly speaking, it is an attack method that takes advantage of blockchain issues and allows double spending by pretending that transactions with a small number of approvals (up to 1 or 2 Confirmations?) have not occurred.
Retail stores, mail order stores, etc. are affected.


When transactions with different destinations are sent to different nodes at almost the same time, a branch occurs on the blockchain. When such a case occurs, the longest chain, that is, the one with the newest block height, is judged to be correct. The shorter transaction is considered invalid, so if an invalid transaction is sent to an exchange or retail store, the store will be at a loss.

- Valuable materials (Head family): https://github.com/demining/Vector76-Attack
- Forked Repository  (The content is the same.): https://github.com/h0tcatSub/Vector76-Attack



The objectives of this project are:

- There are several demo videos of tools that attack Bitcoin on YouTube and elsewhere, and most of them seem to be paid and are trying to scam large sums of money. Therefore, the purpose is to destroy Bitcoin crack tool (sales) scammers. (Fraud Breaker)
 (Fraud Breaker) **If you really can do that, I'd like you to openly show me the source code.**
- To destroy a gambling site (bookmaker) with a fragile payment system (Boss Breaker)
- For educational purposes.

# How to use a this tool, Things necessary

**This is just a tool to make double spending. Therefore, the attacker needs to prepare Bitcoin.**


```
usage: fork_attack.py [-h] from_wifkey send_to attacker_address amount_of_coins fee symbol is_testnet

How To use fork_attack

positional arguments:
  from_wifkey       Fake send btc from wif key.
  send_to           Fake send btc to address.
  attacker_address  Address held by attacker to receive refund (Please prepare an address that is different from the address fthat can be generated
  amount_of_coins   Amount of coins sent. (Enter in BTC units) The maximum amount delayed will vary depending on send_from.
  fee               . (Enter in BTC units) The maximum amount delayed will vary depending on send_from.
  symbol            coin symbol btc or ltc
  is_testnet        Testnet flag 0 or 1

options:
  -h, --help        show this help message and exit
```

# Disclaimer

If you run this tool on mainnet, you do so at your own risk.

Also, since I am incompetent, I made this using these documents as reference. The operation is not yet confirmed as it takes time to synchronize the nodes.

- https://github.com/demining/Vector76-Attack
- https://www.fsa.go.jp/policy/bgin/ResearchPaper_ISID_ja.pdf

If you are trying to destroy the mainnet and use this tool, you will not know if your assets disappear due to a bug, exchange or wallet account being frozen, etc.
suffering the consequences. :D

Happy Hacking!


Kamijou Touma > Kill that blockchain!!  👊  💥 