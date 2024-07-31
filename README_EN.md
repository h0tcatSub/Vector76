# Find out the true identity of the mysterious tool Fake Sender Flasher

I often see videos on Youtube of sending non-existing Bitcoin transactions to exchanges and extracting the balance.
Such videos are scams that steal Bitcoin, Trojan Malware, and even if they are genuine, they are often too expensive.

By chance, when I created a specially crafted transaction so that the mining fee would be 0 and sent it, an unauthorized balance was temporarily reflected.
Of course, since it is not mined, the transaction remains unconfirmed. You can temporarily send your balance to the other party.
After a while, the transaction was canceled and the sent coins were returned.

Those affected are retail stores, mail order stores, gambling sites, etc. that are managed solely by balances.
Exchanges and retail stores should be wary of unauthorized transactions.

**The following conditions are required to execute flash.**
- Address private key of coins with balance (The amount that can be flushed depends on how many coins you have prepared.)
- Broadcasts with 0 mining fees are temporarily accepted.

The following possibilities can be considered as to why a tool that does not require a private key can run Flash.
- The theory is that the developer strictly manages the private key of the address where the coins are stored in advance, and sends the private key to the app via communication and signs with it.

It's also possible that people and developers abusing Flasher are using more sophisticated techniques that aren't publicly known.

Those who want to try it out can try it out with ```flash_unconfirm.py```.
I have tried it several times on the testnet, but it has not been confirmed on the mainnet.
**If you seriously want to do it on the mainnet, please do it only if you are prepared to have your account or address frozen. **
Please see our disclaimer for more details.


Also, if it's just a flash, it might be more efficient to double-spend using a vector76 attack, which has a high possibility of canceling one authorization.


```
usage: flash_unconfirm.py [-h] [--is_testnet IS_TESTNET] send_from_wifkey fake_send_to amount_of_coins

How To Use flash_unconfirm

positional arguments:
  send_from_wifkey      Fake send btc from wif key.
  fake_send_to          Fake send btc to address.
  amount_of_coins       Amount of coins sent. (Enter in BTC units) The maximum amount delayed will vary depending on send_from.

options:
  -h, --help            show this help message and exit
  --is_testnet IS_TESTNET, -test IS_TESTNET
                        Testnet flag (Default=True)
```

# What is Vector76 Attack? (Still experimenting...)

Roughly speaking, it is an attack method that takes advantage of blockchain issues and allows double spending by pretending that transactions with a small number of approvals (up to 1 or 2 Confirmations?) have not occurred.
Retail stores, mail order stores, etc. are affected.

- Valuable materials (Head family): https://github.com/demining/Vector76-Attack
- Forked Repository  (The content is the same.): https://github.com/h0tcatSub/Vector76-Attack



The objectives of this project are:

- There are several demo videos of tools that attack Bitcoin on YouTube and elsewhere, and most of them seem to be paid and are trying to scam large sums of money. Therefore, the purpose is to destroy Bitcoin crack tool (sales) scammers. (Fraud Breaker)
 (Fraud Breaker) **If you really can do that, I'd like you to openly show me the source code.**
- To destroy a gambling site (bookmaker) with a fragile payment system (Boss Breaker)
- For educational purposes.

# How to use a this tool, Things necessary

- Bitcoin nodes that only you are connected to
  - This is configurable in bitcoin.conf with connect=127.0.0.1
  - I think it's a good idea to add the listen=0 parameter to bitcoin.conf.

**This is just a tool to make double spending. Therefore, the attacker needs to prepare Bitcoin.**
**Please change the address and wifi private key used for the experiment depending on the type of network of the node you are setting**

- Now set up a node so that submitblock can send. Also,

In other words,
- If you want to use testnet, you need a testnet wallet and node.

- If you want to do it on the mainnet, you need a mainnet wallet and node.

Also, in order to call the command using subprocess, please put ``bitcoin-cli`` in the same location as the src directory or include it in the PATH.


```
usage: vector76.py [-h] [--is_testnet IS_TESTNET] from_wifkey send_to attacker_address amount_of_coins

How To use vector76

positional arguments:
  from_wifkey           Fake send btc from wif key.
  send_to               Fake send btc to address.
  attacker_address      Address held by attacker to receive refund (Please prepare an address that is different from the address that can be generated
  amount_of_coins       Amount of coins sent. (Enter in BTC units) The maximum amount delayed will vary depending on send_from.

options:
  -h, --help            show this help message and exit
  --is_testnet IS_TESTNET, -test IS_TESTNET
                        Testnet flag (Default=True)
```

During the attack,
```--- Send the block after pressing the enter key. ---```
What to do when this appears is
Immediately after the money is sent to the victim's wallet address, 1 approval has passed, and the payment at the store etc. is completed.
Press enter. Then a block is sent and a Vector76 attack is performed. So please keep your eyes on the screen during this time.

# Disclaimer

If you run this tool on mainnet, you do so at your own risk.

Also, since I am incompetent, I made this using these documents as reference. The operation is not yet confirmed as it takes time to synchronize the nodes.

- https://github.com/demining/Vector76-Attack
- https://www.fsa.go.jp/policy/bgin/ResearchPaper_ISID_ja.pdf

If you are trying to destroy the mainnet and use this tool, you will not know if your assets disappear due to a bug, exchange or wallet account being frozen, etc.
suffering the consequences. :D

Happy Hacking!


Kamijou Touma > Kill that blockchain!!  👊  💥 