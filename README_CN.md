# 找出神秘工具Fake Sender Flasher的真實身份

我經常在 YouTube 上看到將不存在的比特幣交易發送到交易所並提取餘額的影片。
這類影片都是盜取比特幣、特洛伊木馬的騙局，即使是正版，也往往價格過高。

一次偶然的機會，當我創建了一筆特製交易，使挖礦費用為0並發送時，暫時反映了未經授權的餘額。
當然，由於它沒有被開採，交易仍未得到確認。您可以暫時將餘額發送給對方。
過了一會兒，交易被取消，發送的幣被退回。

受影響的是僅透過餘額管理的零售商店、郵購商店、賭博網站等。
交易所和零售商店應警惕未經授權的交易。

**執行快閃記憶體需要以下條件。**
- 餘額的幣私鑰地址（可沖的金額取決於您準備的幣數）
- 暫時接受0挖礦費的廣播。

為什麼不需要私鑰的工具可以運行Flash，可以考慮以下可能性。
- 原理是開發者嚴格管理預先存幣地址的私鑰，並透過通訊將私鑰發送到應用程式並與之簽署。

濫用 Flasher 的人和開發人員也可能使用不為公眾所知的更複雜的技術。

想嘗試的可以用```flash_unconfirm.py```來嘗試。
我在測試網上嘗試了幾次，但在主網上還沒有得到證實。
**如果您真的想在主網上執行此操作，請僅在您準備好凍結您的帳戶或地址的情況下執行此操作。 **
請參閱我們的免責聲明以了解更多詳情。


另外，如果只是一閃而過，使用 vector76 攻擊進行雙花可能會更有效，這種攻擊很有可能取消一次授權。

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

# 什麼是 Vector76 攻擊？ (仍在嘗試)

粗略地說，這是一種利用區塊鏈問題，透過假裝少量批准（1個或2個批准？）的交易沒有發生來允許雙重支付的攻擊方法。
受影響的包括零售商店、郵購商店和賭博網站。

- 有價值的資料：https://github.com/demining/Vector76-Attack
- Fork（內容相同）：https://github.com/h0tcatSub/Vector76-Attack

該專案的目標是：

- YouTube 和其他地方有幾個攻擊比特幣的工具演示視頻，其中大多數似乎是付費的，並試圖詐騙大筆資金。因此，目的是摧毀比特幣破解工具（銷售）騙子。 （詐騙殺手）**如果你真的能做到這一點，我希望你公開地向我展示原始碼。**
- 摧毀支付系統脆弱的賭博網站（賭場荷官迷戀）
- 用於教育目的。

# 如何使用/您需要什麼

- 只有您連接的比特幣節點
  - 這可以在 bitcoin.conf 中使用 connect=127.0.0.1 進行配置
  - 我認為將listen=0參數新增至bitcoin.conf是個好主意。

**這只是一個雙重支付的工具。因此，需要平衡。**
**請根據您設定的節點的網路類型更改實驗所使用的位址和wifi私鑰**

- 現在設定一個節點，以便submitblock可以發送。另外，

換句話說，
- 如果您想使用測試網，您需要測試網錢包和節點。
- 如果你想在主網上進行，你需要一個主網錢包和節點。

另外，為了使用子程序呼叫指令，請將「bitcoin-cli」放在與 src 目錄相同的位置或將其包含在 PATH 中。

```
usage: vector76.py [-h] [--is_testnet IS_TESTNET] [--fee FEE] [--last_txid LAST_TXID]
                   node_host node_port username password attacker_signkey victim_address attacker_address amount_of_coins

How To Use vector76

positional arguments:
  node_host             Blockchain Node Host
  node_port             Blockchain Node Port
  username              Your BTC node username
  password              Your BTC node password
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
  --last_txid LAST_TXID, -txid LAST_TXID
                        Last txid (address of attacker_signkey)
```


當攻擊期間出現此訊息時，
```--- Send the block after pressing the enter key. ---```
該怎麼做：
錢被送到受害者的錢包地址後，立即通過1個批准，並完成在商店等待的付款。
按回車鍵。然後發送一個區塊並執行 Vector76 攻擊。所以請大家在這段時間密切注意螢幕。


# 免責聲明

在主網上執行此工具的風險由您自行承擔。
另外，由於我能力不足，所以我參考了這些文件。該操作尚未確認，因為同步節點需要時間。
- https://github.com/demining/Vector76-Attack
- https://www.fsa.go.jp/policy/bgin/ResearchPaper_ISID_ja.pdf

如果您試圖破壞主網並使用此工具，您將不知道您的資產是否因錯誤、交易所或錢包帳戶被凍結等原因而消失。
那是我的錯 :D


Happy Hacking!


上條鬥真 > 殺死那個區塊鏈！ 👊  💥 