# What is Vector76 Attack?

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

**This is just a tool to make double spending. Therefore, the attacker needs to prepare Bitcoin.**

- Now set up a node so that submitblock can send. Also, **Please change the address and wifi private key used for the experiment depending on the type of network of the node you are setting**

In other words,
- If you want to use testnet, you need a testnet wallet and node.

- If you want to do it on the mainnet, you need a mainnet wallet and node.


```
usage: vector76.py [-h] [--is_testnet IS_TESTNET] [--fee FEE]
                   node_host node_port username password attacker_signkey victim_address attacker_address amount_of_coins

How To Use vector76

positional arguments:
  node_host             Blockchain Node Host
  node_port             Blockchain Node Port
  username              Public node username
  password              Public node password
  attacker_signkey      The attacker has the WIF format private key of the first address (this is used to sign the transaction)
  victim_address        Victim address.
  attacker_address      Address held by attacker to receive refund (Please prepare an address that is different from the address that can be generated
                        with the private key specified in the first place.)
  amount_of_coins       Amount of coins sent. (Enter in BTC units)

options:
  -h, --help            show this help message and exit
  --is_testnet IS_TESTNET
                        testnet flag (Default=True)
  --fee FEE             BTC send fee. (Default=0.00015)
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