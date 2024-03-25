JP / [EN](README_en.md)

# JQuants Python Client
このPythonクライアントは、[J-Quants API](https://jpx.gitbook.io/j-quants-ja/)を簡単に利用するためのラッパーです。金融データの取得、分析、アルゴリズムトレーディングの開発などに役立ちます。

# 機能
- 株価や企業情報などの金融データを取得
- ユーザー認証およびトークンの自動更新
- 複数の金融情報エンドポイントへのアクセス

# 事前準備
このクライアントを使用する前に、J-Quantsのアカウントが必要です。また、利用するにはAPIキー（EmailとPassword）を取得しておく必要があります。

# インストール
依存関係として`requests`モジュールが必要です。以下のコマンドでインストールしてください。

```bash
pip install requests
```

# 使い方
1. JQuantsクラスをインポートします。
2. EmailとPasswordを使ってJQuantsのインスタンスを作成します。
3. 提供されているメソッドを呼び出して、必要な金融データを取得します。

## サンプルコード

```python
from jquants import JQuants

# JQuantsのインスタンスを作成
email = "your_email@example.com"
password = "your_password"
jq = JQuants(email, password)

# 株式のリスト情報を取得
listed_info = jq.listed_info()

# 日次の株価情報を取得
daily_quotes = jq.prices_daily_quotes(code="9434", date_from="20240101", date_to="20240131")

print(listed_info)
print(daily_quotes)
```

# 全データ取得プログラム
すべてのデータを取得するための`get_all_data.py`を付属しています。cloneしたjquantsディレクトリにて以下コマンドを実行します。

```bash
python get_all_data.py
```

出力ファイルの構成を確認するために、ループ処理を最初の1回だけ出力するtestモードがあります。

```bash
python get_all_data.py -test
```

# データチェックプログラム
取得したデータをGoogle Driveなどにアップロードした場合に、（ファイル数の多さやサイズの大きさのためか）データが欠落してしまうケースがありました。データをチェックするプログラムを添付します。

```bash
python data_checker.py path/to/directory
```

Google Drive側のデータチェックを行うには、Google Colaboraoryで下記のように本リポジトリをクローンしたあとでデータチェックを行ってください。

```bash
!git clone https://github.com/t5kit/jquants.git

!python /content/jquants/data_checker.py path/to/directory
```

# API対応表
| API  | エンドポイント | メソッド  |
|:--------|:--------:|--------:|
| [上場銘柄一覧](https://jpx.gitbook.io/j-quants-ja/api-reference/listed_info) | /listed/info | listed_info |
| [株価四本値](https://jpx.gitbook.io/j-quants-ja/api-reference/daily_quotes) | /prices/daily_quotes | prices_daily_quotes |
| [前場四本値](https://jpx.gitbook.io/j-quants-ja/api-reference/prices_am) | /prices/prices_am | prices_prices_am |
| [投資部門別情報](https://jpx.gitbook.io/j-quants-ja/api-reference/trades_spec) | /markets/trades_spec | markets_trades_spec |
| [信用取引週末残高](https://jpx.gitbook.io/j-quants-ja/api-reference/weekly_margin_interest) | /markets/weekly_margin_interest | markets_weekly_margin_interest |
| [業種別空売り比率](https://jpx.gitbook.io/j-quants-ja/api-reference/short_selling) | /markets/short_selling | markets_short_selling |
| [売買内訳データ](https://jpx.gitbook.io/j-quants-ja/api-reference/breakdown) | /markets/breakdown | markets_breakdown |
| [取引カレンダー](https://jpx.gitbook.io/j-quants-ja/api-reference/trading_calendar) | /markets/trading_calendar | markets_trading_calendar |
| [指数四本値](https://jpx.gitbook.io/j-quants-ja/api-reference/indices) | /indices | indices |
| [TOPIX指数四本値](https://jpx.gitbook.io/j-quants-ja/api-reference/topix) | /indices/topix | indices_topix |
| [財務情報](https://jpx.gitbook.io/j-quants-ja/api-reference/statements) | /fins/statements | fins_statements |
| [財務諸表(BS/PL)](https://jpx.gitbook.io/j-quants-ja/api-reference/statements-1) | /fins/fs_details | fins_fs_details |
| [配当金情報](https://jpx.gitbook.io/j-quants-ja/api-reference/dividend) | /fins/dividend | fins_dividend |
| [決算発表予定日](https://jpx.gitbook.io/j-quants-ja/api-reference/announcement) | /fins/announcement | fins_announcement |
| [オプション四本値](https://jpx.gitbook.io/j-quants-ja/api-reference/index_option) | /option/index_option | option_index_option |

# ライセンス
このプロジェクトはMITライセンスの下で公開されています。詳細については、[LICENSE](LICENSE)ファイルをご覧ください。