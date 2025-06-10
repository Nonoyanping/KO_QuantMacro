
# Setup

```shell
uv add matplotlib setuptools pandas pandas_datareader statsmodels
```

## 1. 景気循環

- ドイツを分析対象とし、ドイツの実質GDPデータを取得
- ドイツの対数実質GDPにHP-filterをかけ、循環変動成分およびトレンド成分に分解
- 日本についても対数実質GDPにHP-filterをかけ、循環変動成分およびトレンド成分に分解
- ドイツおよび日本について循環変動成分の標準偏差を計算して比較し、選んだ国と日本の間の循環変動成分の相関係数を計算
- ドイツおよび日本について循環変動成分の時系列データを一つのグラフ上にプロットして比較

Python Script Output:

```shell
=== HP Filter Business Cycle Analysis ===
1. Downloading data...
2. Log transformation...
3. Applying HP filter...
4. Creating plots...
Creating Germany trends plot...
Creating Germany cyclical components plot...
Creating Japan trends plot...
Creating Japan cyclical components plot...
5. Calculating statistics...

=== Results ===
Germany cyclical component std: 1.62%
Japan cyclical component std: 1.57%
Correlation between cycles: 0.7241

Analysis completed!
```

## 2. 経済成長

ソローモデルを用いてOECDの国々の1990~2019年間の経済成長を分析

Python Script Output -> `./assignment2_result/GrowthAccounting(1990_2019).csv`

```text
Table 5.1
Growth Accounting in OECD Countries: 1990-2019

Country         Growth Rate  TFP Growth   Capital Deepening  TFP Share  Capital Share
Australia       1.28         0.72         0.56               0.56       0.44
Austria         0.97         0.39         0.58               0.4        0.6
Belgium         0.72         0.16         0.56               0.22       0.78
Canada          0.93         0.36         0.57               0.39       0.61
Denmark         1.19         0.59         0.6                0.49       0.51
Finland         1.44         0.82         0.62               0.57       0.43
France          0.93         0.31         0.62               0.34       0.66
Germany         1.13         0.56         0.57               0.5        0.5
Greece          1.0          0.02         0.98               0.02       0.98
Iceland         1.36         1.03         0.33               0.76       0.24
Ireland         2.75         1.4          1.36               0.51       0.49
Italy           0.48         -0.25        0.74               -0.52      1.52
Japan           0.84         -0.53        1.37               -0.64      1.64
Netherlands     0.89         0.51         0.39               0.57       0.43
New Zealand     0.79         0.46         0.34               0.58       0.42
Norway          1.24         0.63         0.61               0.51       0.49
Portugal        1.36         0.21         1.15               0.15       0.85
Spain           0.95         -0.07        1.01               -0.07      1.07
Sweden          1.87         1.34         0.53               0.72       0.28
Switzerland     0.5          0.11         0.4                0.21       0.79
United Kingdom  1.39         0.99         0.4                0.71       0.29
United States   1.66         1.04         0.61               0.63       0.37
Average         1.17         0.49         0.68               0.35       0.65
```
