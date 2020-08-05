# Paper generator
## ETL-utils

現 産業技術総合研究所 にて作成された、「ETL文字データベース」を利用するためのツール群です。  
（一部 papaer-generator/fill_field2image に特化した機能あり）  
サイト：http://etlcdb.db.aist.go.jp/

## ETL data Convert to PNG image.
- etl6_conv_img.py
- etl9b_conv_img.py
- etl9g_conv_img.py

サイトより取得した、ETL6、ETL9B、ETL9G を.png 形式にコンバートするツールです。  
※ Python3系のみに対応  
※ 事前にデータをダウンロードする必要あり  

実行する.py と同じ階層に、サイトより取得した ETLx のデータのデータのみを含むディレクトリ **ETLx** に対して処理を行い、  
**ETLx_img** ディレクトリに文字コード毎にPNGファイルを出力します。

例：ETL9B データの場合
```
$ python3 etl9b_conv_img.py
```

    必要なディレクトリ構造
    <dir>
    ├ etl9b_conv_img.py
    ├ ETL9B << データが含まれるディレクトリ
    │　 ├ ETL9B_1
    │　 ├ ETL9B_2
    │　 ├ ETL9B_3
    │　 ├ ETL9B_4
    │　 └ ETL9B_5 ※ _INFO などのファイルは含めない
    └ ETL9B_img << 生成される画像データディレクトリ
        ├ 2422 << 文字コード別のディレクトリ
        │   ├ ETL9B_xxxx.png << 画像ファイル
        │   ├ ETL9B_xxxx.png
        │   ├   :
        ├ 2424
        │   ├

### 注意
- ETL9系に関しては、生成すると60万ファイルを超えるPNGファイルが生成されます。
- 実行時、データファイル以外のファイルはディレクトリ内に含めないでください。

## Text to ETL image list

- text2etlimg.py

### getETLImages(text)

ETLデータよりコンバートしたPNGファイルを読み込み、text の文字列に相当する 画像データ（cv_image：numpy）のリストとして返却します。

サンプル動作
```
$ python3 text2etlimg.py あいうえお
```

    必要なディレクトリ構造
    <dir>
    ├ text2etlimg.py
    ├ ETL6_img
    └ ETL9G_img

### 注意
- 現時点では、ELT6データ、ETL9Gデータのみ対応
- データセットに存在しないため、英字小文字→大文字化、カタカナ濁点→濁点無しカタカナ に変換
- papaer-generator/fill_field2image 用機能として、「!」→ チェックマークの出力、「#」→ 丸印の出力 に対応（※）
  - チェックマーク、丸印に対応するには、https://github.com/faxocr/kocr の images に含まれる、チェック画像、丸印画像を symbol_img/ 配下の 21 23 ディレクトリにそれぞれ格納する必要あり
- その他、存在しない、変換できない文字コードは空白データとして出力
