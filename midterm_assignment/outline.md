## Setup

```shell
uv add matplotlib setuptools pandas pandas_datareader statsmodels
```

## 1. 景気循環

1. ドイツを分析対象とし、ドイツの実質GDPデータを取得

2. ドイツの対数実質GDPにHP-filterをかけ、循環変動成分およびトレンド成分に分解

3. 日本についても対数実質GDPにHP-filterをかけ、循環変動成分およびトレンド成分に分解

4. ドイツおよび日本について循環変動成分の標準偏差を計算して比較し、選んだ国と日本の間の循環変動成分の相関係数を計算

5. ドイツおよび日本について循環変動成分の時系列データを一つのグラフ上にプロットして比較
