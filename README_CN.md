# 探索神秘工具Fake Sender Flasher的真相

经常在Youtube上看到有人将不存在的比特币交易发送到交易所以提取余额的视频。这些视频要么是骗取比特币的骗局，要么是特洛伊木马，或者即使是真的，也都是昂贵的内容。

偶然间，我制作了一笔矿工费用为0的交易并发送，发现未确认的余额暂时反映在账户中。当然，由于没有被矿工确认，该交易一直处于未确认状态。但在一段时间后，这笔交易会被取消，发送的比特币会被退还。

受害者主要是那些只管理余额的小型零售店、网店、赌博网站等。交易所和零售店要警惕未确认的交易。

**要执行闪存操作，必须满足以下条件：**

- 具有余额的比特币地址的私钥（闪存的金额取决于准备的比特币数量。）
- 一时能够接受矿工费用为0的广播

没有私钥的工具为什么能闪存？可能的解释是：

开发者预先以某种方式严密管理含有比特币的地址的私钥，通过通信将私钥发送到应用程序并进行签名。
另外，滥用Flasher的人和开发者可能使用了更高级的技术，公众尚未知道。

想亲自尝试的人可以使用```flash_unconfirm.py```进行测试。在测试网进行了多次尝试，但在主网上尚未确认。

**如果真的想在主网上进行操作，请准备好账户或地址被冻结的觉悟。**
详情请查看免责条款。

此外，与其进行闪存操作，不如使用可能性更高的vector76攻击来进行双重支付，可能效率更高。

- 2024/8/4 追加：这可能可以作为阻止区块链节点运行的Spammer或Jammer使用。如果从某处获得了真正的Flasher，将进行逆向工程等以进行更新。


```
usage: flash_unconfirm.py [-h] send_from_wifkey fake_send_to blockcypher_token currency amount_of_coins

How To Use flash_unconfirm

positional arguments:
  send_from_wifkey   从wif密钥发送伪造的比特币。
  fake_send_to       发送伪造的比特币到地址。
  blockcypher_token  blockcypher_apikey 有可能成功与BTC一起使用。
  currency           货币。btc, ltc (默认=btc)
  amount_of_coins    发送的比特币数量。延迟的最大金额取决于send_from。

options:
  -h, --help         显示此帮助信息并退出

```

# 什么是双重支付攻击？（实验中）
Vector76  简单来说，这是利用区块链上的问题，将少量确认数（1~2个确认？）的交易变成无效，以实现双重支付的攻击手段。

几乎同时向不同节点发送仅接收地址不同的交易，会在区块链上产生分叉。在这种情况下，长链（即最新区块高度）被视为正确。短链上的交易被视为无效，如果无效交易发送到交易所或零售店，他们将会遭受损失。

受害者主要是小型零售店、网店、赌博网站等。

- 宝贵资料：https://github.com/demining/Vector76-Attack
- 仓库镜像（内容相同）：https://github.com/h0tcatSub/Vector76-Attack

该项目的目标如下：

- 在Youtube等平台上有一些演示攻击比特币工具的视频，这些工具通常是收费的，试图骗取大量资金。因此，目的是摧毁这些比特币破解工具（销售）骗子。（欺诈杀手） **如果真能做到这些，请公开源代码。**
- 摧毁支付系统脆弱的赌博网站（庄家杀手）
- 教育目的。

# 使用方法和必需品
**这只是一个双重支付工具。因此，余额是必需的。**

```
usage: fork_attack.py [-h] from_wifkey send_to attacker_address amount_of_coins fee symbol is_testnet

How To use fork_attack

positional arguments:
  from_wifkey       从wif密钥发送伪造的比特币。
  send_to           发送伪造的比特币到地址。
  attacker_address  攻击者持有的接收退款的地址（请准备一个不同于生成的地址的地址）
  amount_of_coins   发送的比特币数量。（以BTC单位输入）延迟的最大金额取决于send_from。
  fee               手续费。（以BTC单位输入）延迟的最大金额取决于send_from。
  symbol            货币符号btc或ltc
  is_testnet        测试网标志0或1

options:
  -h, --help        显示此帮助信息并退出
```

# 免责声明
在主网上执行此工具时，请自行承担风险。此外，由于我能力有限，参考这些文件制作了此工具。节点同步需要时间，尚未确认其运行。

- https://github.com/demining/Vector76-Attack
- https://www.fsa.go.jp/policy/bgin/ResearchPaper_ISID_ja.pdf


如果你打算用此工具摧毁主网，并因此导致账户冻结或资产消失等问题，我概不负责。
这是自作自受 

Happy Hacking!

上条当麻 > 那个区块链，我要杀了你!! 👊 💥