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


# Vector76攻撃とは? (実験中)

ざっくり言うとブロックチェーン上の問題をついて少ない承認数(1~2承認まで?)のトランザクションを無かったことにして二重払いを可能にする攻撃手法。
被害を受けるのは小売店、通販、ギャンブルサイトなどです。

- 貴重な資料: https://github.com/demining/Vector76-Attack
- フォーク(中身は一緒): https://github.com/h0tcatSub/Vector76-Attack


このプロジェクトの目的は次のとおりです。

- YoutubeなどにBitcoinに攻撃を仕掛けるツールのデモ動画がいくつか転がっていてだいたいそう言うのは有料らしく大金を騙し取ろうとしているものばっかり。そこでビットコインクラックツール(販売)詐欺師を潰す目的。(詐欺殺し) **本当にそんなことできるなら堂々とソースコードを見せてほしいものですね**
- 決済システムが脆いギャンブルサイト(ブックメーカー)を潰すため(胴元殺し)
- 教育目的。

# 使い方・必要なもの

- 自身だけが接続しているBitcoinノード
  - 例えばテストネットの場合、bitcoin.confでconnect=127.0.0.1:18332で設定可能です 。ポート番号を設定している場合はconnectの設定をうまくやってください。
  - listen=0 のパラメータをbitcoin.confに追加しておくのもいいと思います。

- **あくまでもこれは二重払いをするツールです。なので残高は必須です。**
- **立てているノードのネットワークの種類によって実験に使うアドレスやwif秘密鍵は変えてください**

つまり、

- テストネットでやるならテストネットのウォレットとノードが必要
- メインネットでやるならメインネットのウォレットとノードが必要

あと、subprocessを使ってコマンドを呼び出すため```bitcoin-cli```はsrcディレクトリと同じ場所に置くかPATHを通しておいてください。

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