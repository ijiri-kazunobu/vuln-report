# Vuln Report

脆弱性データのCSVをpandasで集計し、グラフ付きのExcelレポートを自動で作成するPythonツールです。

## 背景

大量のデータを集計して、Excelで表やグラフにまとめる作業は、手作業ではフィルター・並べ替え・コピー・グラフ作成・書式設定と多くの手順が必要です。本ツールでは、この一連の作業を自動化し、コマンド1つで同じ形式のレポートを作成できるようにしました。

題材には脆弱性情報を使用していますが、「CSVを集計し、グラフ付きのExcelレポートにする」という処理は、売上データや業務データなど、さまざまなデータの集計に応用できます。

## セットアップ

```
$ pip install -r requirements.txt
```

## 使い方

```
$ python report.py data/wordpress.csv
$ python report.py data/wordpress.csv --output wordpress_report.xlsx
```

| 引数 | 説明 |
|---|---|
| `csv_file` | 集計するCSVファイルのパス（必須） |
| `--output` | 保存するExcelファイル名（省略時：report.xlsx） |

入力するCSVは、[vuln-collector](https://github.com/ijiri-kazunobu/vuln-collector) で作成したものを想定しています。

## 実行例

```
$ python report.py data/wordpress.csv --output wordpress_report.xlsx
全件数: 100 件

=== 深刻度ごとの件数 ===
     深刻度  件数
CRITICAL   9
    HIGH  15
  MEDIUM  66
     LOW  10
     未評価   0

平均スコア: 6.0
最高スコア: 9.8
対応が必要な脆弱性 (CRITICAL・HIGH) : 24 件

📊 wordpress_report.xlsx を作成しました
```

存在しないファイルを指定した場合

```
$ python report.py data/nothing.csv
[エラー] data\nothing.csv が見つかりません
```

## 作成されるレポート

| シート | 内容 |
|---|---|
| サマリー | 深刻度ごとの件数の表と棒グラフ |
| 要対応 | 深刻度がCRITICAL・HIGHの脆弱性を、スコアの高い順に並べた一覧 |
| 全件 | すべての脆弱性の一覧 |

すべてのシートで、見出しの色付け・列幅の調整・見出し行の固定を行っています。グラフは画像ではなくExcelのグラフ機能で作成しているため、受け取った人があとからデザインを変更することもできます。

## vuln-collector との連携

[vuln-collector](https://github.com/ijiri-kazunobu/vuln-collector) と組み合わせることで、「収集 → 分析 → レポート作成」の流れを自動化できます。

```
$ python collector.py --keyword Apache --days 30 --limit 100 --output ../vuln-report/data/apache.csv
$ python report.py data/apache.csv --output apache_report.xlsx
```

収集と分析を別のツールに分けているため、本ツールはvuln-collector以外で作成した同じ形式のCSVにも利用できます。

## 工夫した点

- **危険な順に並べた集計表**：深刻度ごとの件数を、件数の多い順ではなくCRITICAL → HIGH → MEDIUM → LOW → 未評価の順に並べています。レポートを読む人が、緊急度の高いものから確認できるようにするためです。
- **毎回同じ形式のレポート**：データに含まれない深刻度も0件として表示するため、週ごとのレポートを並べて比較しやすくなっています。
- **処理の分割**：集計（`analyze`）、画面表示（`print_summary`）、レポート保存（`save_report`）を別の関数に分けました。たとえば、画面表示をせずにレポートだけ作成するといった変更も簡単に行えます。
- **設定の一元管理**：深刻度の並び順や列幅を、ファイル冒頭の定数にまとめています。
- **入力ファイルの確認**：指定されたCSVが存在しない場合は、エラーで停止せずにメッセージを表示します。

## 今後の改善

- **上書きの防止**：開発中、保存先と読み込み元のファイルを取り違え、元のデータを上書きしかねない誤りに気づきました。読み込み元と保存先が同じ場合にエラーを表示するチェックを追加したいと考えています。
- **日付ごとの推移グラフ**：公開日ごとの件数を折れ線グラフにし、脆弱性の増減の傾向を確認できるようにしたいと考えています。
- **前回のレポートとの比較**：前回から新しく増えた脆弱性を強調表示できるようにしたいと考えています。

## 使用技術

- Python 3.12
- pandas（データの集計・Excelへの出力）
- openpyxl（Excelの書式設定・グラフ作成）
- 標準ライブラリ（argparse、pathlib）