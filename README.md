# Vector76攻撃とは?

ざっくり言うとブロックチェーン上の問題をついて少ない承認数(1~2承認まで?)のトランザクションを無かったことにして二重払いを可能にする攻撃手法。
被害を受けるのは小売店、通販、ギャンブルサイトなどです。

貴重な資料: https://github.com/demining/Vector76-Attack
フォーク(中身は一緒): https://github.com/h0tcatSub/Vector76-Attack


このプロジェクトの目的は次のとおりです。

- YoutubeなどにBitcoinに攻撃を仕掛けるツールのデモ動画がいくつか転がっていてだいたいそう言うのは有料らしく大金を騙し取ろうとしているものばっかり。そこで詐欺を潰す目的。(詐欺殺し)
- 決済システムが脆いギャンブルサイト(ブックメーカー)を潰すため(胴元殺し)
- 教育目的。

# 使い方・必要なもの

**あくまでもこれは二重払いをするツールです。なので残高は必須です。**

```
usage: vector76.py [-h] [--network NETWORK]
                   node_host node_port username password attacker_signkey victim_address attacker_address amount_of_coins prev_deposit_TXID

How To Use vector76

positional arguments:
  node_host          Blockchain Node Host
  node_port          Blockchain Node Port
  username           Node username
  password           Node password
  attacker_signkey   The attacker has the WIF format private key of the first address (this is used to sign the transaction)
  victim_address     victim address.
  attacker_address   Address held by attacker to receive refund (Please prepare an address that is different from the address that can be generated with the
                     private key specified in the first place.)
  amount_of_coins    Amount of coins sent. (Enter in BTC units)
  prev_deposit_TXID  Last deposit TXID of first attacker address

options:
  -h, --help         show this help message and exit
  --network NETWORK  mainnet or testnet. (Default = testnet)
```

実行中、
```--- Send the block after pressing the enter key. ---```
が表示されたらやることは、
被害者側のウォレットアドレスに送金し、 1承認が経過し、お店などの決済が完了された後すぐに
エンタキーを押します。そうするとブロックが送信されVector76攻撃を行う感じです。なのでその間は画面から目を離さないでください。

# 免責事項


このツールをメインネットで実行する際は自己責任でやってください。
また、私は無能なのでこれらのドキュメントを参考にし作りました。ノードの同期に時間がかかっているからまだ動作は未確認です。

- https://github.com/demining/Vector76-Attack
- https://www.fsa.go.jp/policy/bgin/ResearchPaper_ISID_ja.pdf

もしあなたがメインネットを潰そうとしている場合でこのツールを使い、万が一バグ・取引所やウォレットの口座が凍結されるなどして資産が消えても知りません。
それは自業自得 :D

Happy Hacking!

上条当麻 > そのブロックチェーンをぶち殺す!!  👊  💥 