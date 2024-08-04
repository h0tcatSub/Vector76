# 謎ツールFake Sender Flasherの正体を探る

よくYoutubeにBitcoinの存在しないトランザクションを取引所に送りつけて残高を抜き取る動画を見かける。
そういった動画はビットコインを奪う詐欺であったり、トロイの木馬、本物だとしても高額すぎるコンテンツばかり。

たまたまマイニング手数料が0になるように細工したトランザクションを作って仮に送信したところ一時的に未承認の残高が反映されていた。
もちろんマイニングはされないためその取引は未承認のまま。一時的に残高を相手に送ることが可能。
しばらく時間が経つと、その取引は抹消され送ったコインは返されていた。

被害を受けるのは残高だけで管理をしている小売店、通販、ギャンブルサイトなどです。
取引所や小売店は未承認のトランザクションに要注意。

**フラッシュを実行するには下記の条件は必須。**
- 残高があるコインのアドレス秘密鍵 (フラッシュできる量はどれだけコインを用意したかに依存します。)
- マイニング手数料0のブロードキャストが一時的に受け入れられること

秘密鍵なしにできるツールがどうしてFlashできるかというと次の可能性が考えられます。
- 開発者が事前に何らかの方法でコインが入っているアドレスの秘密鍵を厳重に管理し、通信でアプリに秘密鍵を送りそれで署名している説。

あとは、Flasherを乱用している人たちや開発者は公に知らされてないもっと高度な技術を使っている可能性もある。

実際に試してみたい人は、```flash_unconfirm.py```で試すことができます。
テストネットでは何度か試していますが、メインネットでは未確認です。
**本気でメインネットでやりたいなら口座やアドレスが凍結される覚悟がある人がやってください。**
詳しくは免責事項をご確認ください。

また、flashするくらいだったら1承認を打ち消せる可能性が高いvector76攻撃を使って二重払いしたほうが効率が逆にいいかもしれません。

- 2024/8/4 追記: おそらくこれはFlasherというかブロックチェーンのノードの働きを妨害するSpammer、もしくはJammerとして使えるかもしれません。もし本物のFlasherを何処かから手に入れたらリバースエンジニアリングなどしてリニューアル予定です。

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


# 二重払い攻撃とは? (実験中)

Vector76攻撃だったら、ざっくり言うとブロックチェーン上の問題をついて少ない承認数(1~2承認まで?)のトランザクションを無かったことにして二重払いを可能にする攻撃手法。

ほぼ同時に異なるノードに送り先だけが異なるトランザクションを送りつけるとブロックチェーン上で分岐が生じます。このようなケースが発生した場合、長いチェーンつまり一番ブロック高が新しい方が正しいと判断されます。短い方の取引は無効としてみなされるため、もし無効な取引が取引所や小売店に送られていたらお店は泣き寝入りするでしょう。

被害を受けるのは小売店、通販、ギャンブルサイトなどです。

- 貴重な資料: https://github.com/demining/Vector76-Attack
- リポジトリミラーフォーク(中身は一緒): https://github.com/h0tcatSub/Vector76-Attack


このプロジェクトの目的は次のとおりです。

- YoutubeなどにBitcoinに攻撃を仕掛けるツールのデモ動画がいくつか転がっていてだいたいそう言うのは有料らしく大金を騙し取ろうとしているものばっかり。そこでビットコインクラックツール(販売)詐欺師を潰す目的。(詐欺殺し) **本当にそんなことできるなら堂々とソースコードを見せてほしいものですね**
- 決済システムが脆いギャンブルサイト(ブックメーカー)を潰すため(胴元殺し)
- 教育目的。

# 使い方・必要なもの

**あくまでもこれは二重払いをするツールです。なので残高は必須です。**

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

# 免責事項


このツールをメインネットで実行する際は自己責任でやってください。
また、私は無能なのでこれらのドキュメントを参考にし作りました。ノードの同期に時間がかかっているからまだ動作は未確認です。

- https://github.com/demining/Vector76-Attack
- https://www.fsa.go.jp/policy/bgin/ResearchPaper_ISID_ja.pdf

もしあなたがメインネットを潰そうとしている場合でこのツールを使い、万が一バグ・取引所やウォレットの口座が凍結されるなどして資産が消えても知りません。
だってそれは自業自得でしょ? :D

Happy Hacking!

上条当麻 > そのブロックチェーンをぶち殺す!!  👊  💥 