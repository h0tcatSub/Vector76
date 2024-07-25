# 什麼是 Vector76 攻擊？

粗略地說，這是一種利用區塊鏈問題，透過假裝少量批准（1個或2個批准？）的交易沒有發生來允許雙重支付的攻擊方法。
受影響的包括零售商店、郵購商店和賭博網站。

有價值的資料：https://github.com/demining/Vector76-Attack
Fork（內容相同）：https://github.com/h0tcatSub/Vector76-Attack

該專案的目標是：

- YouTube 上有幾個攻擊比特幣的工具的演示視頻，其中大多數似乎是付費的，並試圖騙取您很多錢。目的是摧毀那裡的詐欺行為。 （詐騙殺手）
- 摧毀支付系統脆弱的賭博網站（博彩公司）（殺死老闆）
- 用於教育目的。

# 如何使用/您需要什麼

**這只是一個雙重支付的工具。因此，需要平衡。**

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


當攻擊期間出現此訊息時，
```--- Send the block after pressing the enter key. ---```
該怎麼做：
錢被送到受害者的錢包地址後，立即通過1個批准，並完成在商店等待的付款。
按回車鍵。然後發送一個區塊並執行 Vector76 攻擊。所以請大家在這段時間密切注意螢幕。


# 免責聲明

在主網上執行此工具的風險由您自行承擔。
另外，由於我能力不足，所以我參考了這些文件。該操作尚未確認，因為同步節點需要時間。
https://github.com/demining/Vector76-Attack
https://www.fsa.go.jp/policy/bgin/ResearchPaper_ISID_ja.pdf

如果您試圖破壞主網並使用此工具，您將不知道您的資產是否因錯誤、交易所或錢包帳戶被凍結等原因而消失。
那是我的錯 :D


Happy Hacking!






上條鬥真 > 殺死那個區塊鏈！ 👊  💥 