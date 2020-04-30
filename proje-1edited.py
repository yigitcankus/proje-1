import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore
from scipy.stats.mstats import winsorize
from wordcloud import WordCloud
import seaborn as sns
import scipy.stats as stats
from scipy.stats import jarque_bera
from scipy.stats import normaltest
import math
import re

df = pd.read_csv("games_details.csv")

#Finding which team scored how many. --- tabloda göster ilk 10 takım
# x=df.groupby("TEAM_ABBREVIATION").sum()["PTS"]
# x=x.sort_values(ascending=False)
# plt.plot(x.head(10))
# plt.show()
# print(x)

##Match scores
# a = df.groupby(["GAME_ID", "TEAM_ABBREVIATION"]).sum()["PTS"]
# print(a)

##Points of some classy players -- grafik , en çok skor yapan 10 oyuncu.
# players = ["Giannis Antetokounmpo", "LeBron James", "Kobe Bryant", "Shaquille O'Neal", "James Harden"]
# points= []
# for i in players:
#     points.append(df.loc[df['PLAYER_NAME'] == i, 'PTS'].sum())
#
# for i in range(len(players)):
#     print(players[i] ,":", points[i] )
#
# plt.bar(players,points)
# plt.show()

# b= df.groupby(["PLAYER_NAME"]).sum()["PTS"]
# b= b.sort_values(ascending=False)
# plt.plot(b.head(5))
# plt.show()
# print(b.head(10))

####
# df["offensivity"] = df["PTS"]+ df["AST"]+ df["OREB"]
#
# print(df["offensivity"].describe())
# df["seg"] = 3
# df.loc[df["offensivity"]<5,"seg"]=1
# df.loc[(df["offensivity"]<=19) & (df["offensivity"]>=5),"seg"]=2
# df.loc[df["offensivity"]>19,"seg"]=3
#
# print(df[["offensivity","seg"]])
#
# x=df[(df.seg == 1)]
#
# offensive_players = x.groupby(["PLAYER_NAME"]).sum()["offensivity"]
# offensive_players=offensive_players.sort_values(ascending=False)
# plt.plot(offensive_players.head(5))
# plt.show()
#######


###Top 10 offensive rebounder
# c= df.groupby(["PLAYER_NAME"]).sum()["OREB"]
# c= c.sort_values(ascending=False)
# plt.plt(c.head(5))
# plt.show()

### Avg blocks per match
# len_match = len(df["GAME_ID"].unique())
# blocks = df["BLK"].sum()
# avg_block = blocks/len_match
# print("maç başına yapılan blok:",avg_block)


##how many players are there by positions
# x = df["START_POSITION"].value_counts()
# print(x)


#### Aykırı değerler boxplot ile göstermek için ortalam ile doldurdum
# doldurma_listesi = []
#
# for col in df.columns:
#     doldurma_listesi.append(col)
#
# doldurma_listesi = doldurma_listesi[9:]
#
# for colm in doldurma_listesi:
#     df[colm].fillna(df[colm].mean(), inplace=True)
#
# plt.boxplot(df["FGA"] )
# plt.title("FGA sayısının kutu grafiği")
# plt.show()

#### top değerleri winsorize edersek eğer
# doldurma_listesi = []
#
# for col in df.columns:
#     doldurma_listesi.append(col)
#
# doldurma_listesi = doldurma_listesi[9:]
#
# for colm in doldurma_listesi:
#     df[colm].fillna(df[colm].mean(), inplace=True)
#
#
# winsorize_goruntulenme = winsorize(df["FGA"], (0, 0.035))
# plt.boxplot(winsorize_goruntulenme)
# plt.title("Görüntülenme sayısının kutu grafiği (whis=1.5)")
# plt.show()

### Z_score ile eşik değerlerdeki aykırı değer sayısı
# doldurma_listesi = []
#
# for col in df.columns:
#     doldurma_listesi.append(col)
#
# doldurma_listesi = doldurma_listesi[9:]
#
# for colm in doldurma_listesi:
#     df[colm].fillna(df[colm].mean(), inplace=True)
#
# for colm in doldurma_listesi:
#     z_scores = zscore(df[colm])
#     for threshold in range(1,5):
#         print(colm," için eşik değeri: {}".format(threshold))
#         print("Aykırı değerlerin sayısı: {}".format(len((np.where(z_scores > threshold)[0]))))
#         print()
#     print('------')



##Oyuncu isimlerine wordcloud ile bakalım. No:1 tabiki lebron james
#
# wordcloud = WordCloud(background_color="orange").generate(" ".join(df["PLAYER_NAME"]))
# plt.figure(figsize=(15,10))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
#
# plt.show()

## points ile saha içi isabet verimlilik puanı ve reb ilişkisi
#
# plt.subplot(1,3,1)
# plt.scatter(df["PTS"], df["FGM"])
# plt.title("Points & Saha içi isabet")
# plt.xlabel('points')
# plt.ylabel('saha içi isabet')
#
# plt.subplot(1,3,2)
# plt.scatter(df["PTS"], df["PLUS_MINUS"])
# plt.title("Points & Verimlilik puanı")
# plt.xlabel('Points')
# plt.ylabel('Verimlilik puanı')
#
# plt.subplot(1,3,3)
# plt.scatter(df["PTS"], df["REB"])
# plt.title("Points & Rebound")
# plt.xlabel('Points')
# plt.ylabel('Rebound')
#
# plt.show()

### Elimizdeki sayısal verilerin corelasyonları. Point için bakarsak saha içi isabet(FGM), saha içi deneme (FGA)
# ve serbest atış yüksek oranlı.
# plt.figure(figsize=(10, 16))
# df2 = df.drop(df.columns[[0, 1, 2,3,4,5,6,7]], axis=1)
#
# corr_df = df2.corr()
# print(corr_df)
#
# sns.heatmap(corr_df, square=True, annot=True, linewidths=.9, vmin=0, vmax=1, cmap='viridis')
# plt.show()


## t test for start position " G,F,C "

# dereceler = df["START_POSITION"].unique()
#
# pd.options.display.float_format = '{:.15f}'.format
# for var in ["PTS", "REB", "AST"]:
#     karsilastirma = pd.DataFrame(columns=['grup_1', 'grup_2', 'istatistik', 'p_degeri'])
#     print("{} için karşılaştırma \n".format(var), end='')
#     for i in range(0, len(dereceler)):
#         for j in range(i + 1, len(dereceler)):
#             ttest = stats.ttest_ind(df[df["START_POSITION"] == dereceler[i]][var],
#                                     df[df["START_POSITION"] == dereceler[j]][var])
#             grup_1 = dereceler[i]
#             grup_2 = dereceler[j]
#             istatistik = ttest[0]
#             p_degeri = ttest[1]
#
#             karsilastirma = karsilastirma.append({"grup_1": grup_1,
#                                                   "grup_2": grup_2,
#                                                   "istatistik": istatistik,
#                                                   "p_degeri": p_degeri}, ignore_index=True)
#     print(karsilastirma)


##hepsi 0.00 eğer 0.05ten büyük olsaydı tam olarak nasıl bir sonuç çıkarıcaktık yorumlayamadım.
#--------------------------------



###pts reb ve ast değerlerinin dağılımına ve log dağılımı
#
# doldurma_listesi = []
#
# for col in df.columns:
#     doldurma_listesi.append(col)
#
# doldurma_listesi = doldurma_listesi[9:]
#
# for colm in doldurma_listesi:
#     df[colm].fillna(df[colm].mean(), inplace=True)
#
# plt.figure(figsize=(18, 15))
#
# degiskenler = ['PTS', 'REB', 'AST']
#
# df["PTS"] = df["PTS"].replace(0.0, 0.01)
# df["REB"] = df["REB"].replace(0.0, 0.01)
# df["AST"] = df["AST"].replace(0.0, 0.01)
##log dönüşümü yaparken 0.0 değerler sorun çıkarıyordu
# for i in range(3):
#     plt.subplot(2, 3, i + 1)
#     plt.hist(df[degiskenler[i]])
#     plt.title(degiskenler[i])
#
# for i in range(3):
#     plt.subplot(2, 3, i + 4)
#     plt.hist(np.log(df[degiskenler[i]]))
#     plt.title(degiskenler[i] + ' (log dönüşümlü)')
#
# plt.show()

##normal dağılımlı gibi görünüyor ama tam olarak bilemeyiz


#--------------------------------------------
## Lets look p values
# doldurma_listesi = []
#
# for col in df.columns:
#     doldurma_listesi.append(col)
#
# doldurma_listesi = doldurma_listesi[9:]
#
# for colm in doldurma_listesi:
#     df[colm].fillna(df[colm].mean(), inplace=True)
#
# pd.options.display.float_format = '{:.5f}'.format
# df["PTS"] = df["PTS"].replace(0.0, 0.01)
# df["REB"] = df["REB"].replace(0.0, 0.01)
# df["AST"] = df["AST"].replace(0.0, 0.01)
#
#
# degiskenler = ["PTS", "REB", "AST"]
# dagilim_testleri = pd.DataFrame(columns=['ozellik', 'jarque_bera_stats', 'jarque_bera_p_value',
#                                          'normal_stats', 'normal_p_value'])
#
# for ozellik in degiskenler:
#     jb_stats = jarque_bera(np.log(df[ozellik]))
#     norm_stats = normaltest(np.log(df[ozellik]))
#     dagilim_testleri = dagilim_testleri.append({"ozellik": ozellik,
#                                                 "jarque_bera_stats" : jb_stats[0] ,
#                                                 "jarque_bera_p_value" : jb_stats[1] ,
#                                                 "normal_stats": norm_stats[0] ,
#                                                 "normal_p_value" : norm_stats[1]
#                                                }, ignore_index=True)
# print(dagilim_testleri)

##p values are 0 again

#-------------------------------------

#Verilerin nerede daha çok varyansı olduğunu görmek için standartlaştırıp normalleştiriyoruz
# doldurma_listesi = []
#
# for col in df.columns:
#     doldurma_listesi.append(col)
#
# doldurma_listesi = doldurma_listesi[9:]
#
# for colm in doldurma_listesi:
#     df[colm].fillna(df[colm].mean(), inplace=True)
# plt.figure(figsize=(18,5))
# plt.subplot(1,2,1)
#
# t = sns.regplot('PTS', 'PLUS_MINUS', df, x_jitter=.49, y_jitter=.49, fit_reg=False)
# t.axhline(0, color='k', linestyle='-', linewidth=2)
# t.axvline(0, color='k', linestyle='-', linewidth=2)
# t.axes.set_title('başlangıç verisi')
#
# plt.subplot(1,2,2)
#
# std_df = pd.DataFrame()
# std_df['PTS_z_score'] = (df['PTS'] - df['PTS'].mean()) / df['PTS'].std()
# std_df['PLUS_MINUS_z_score'] = (df['PLUS_MINUS'] - df['PLUS_MINUS'].mean()) / df['PLUS_MINUS'].std()
#
# t = sns.regplot('PTS_z_score','PLUS_MINUS_z_score',std_df, x_jitter=.49, y_jitter=.49, fit_reg=False )
# t.axhline(0, color='k', linestyle='-', linewidth=2)
# t.axvline(0, color='k', linestyle='-', linewidth=2)
# t.axes.set_title('Standartlaştırılmış Veri')
# plt.show()
#
# ### burası benim laptopumda çok kasıyor bence veri çok olduğu için olabilir.
#
# plt.figure(figsize=(18,5))
#
# plt.subplot(1,2,1)
#
# t = sns.regplot('PTS_z_score', 'PLUS_MINUS_z_score', std_df, x_jitter=.49, y_jitter=.49, fit_reg=False)
#
# t.axhline(0, color='k', linestyle='-', linewidth=2)
# t.axvline(0, color='k', linestyle='-', linewidth=2)
# t.axes.set_title('Standartlaştırılmış Veri')
#
# sns.regplot('PTS_z_score', 'PLUS_MINUS_z_score', std_df, scatter=False, color="red")
#
# plt.subplot(1,2,2)
#
# std_df['PTS_z_score_rotated'] = math.cos(40) * std_df['PTS_z_score'] - math.sin(40) * std_df['PTS_z_score']
# std_df['PLUS_MINUS_z_score_rotated'] = math.sin(40) * std_df['PLUS_MINUS_z_score'] + math.cos(40) * std_df['PLUS_MINUS_z_score']
#
# t = sns.regplot('PTS_z_score_rotated','PLUS_MINUS_z_score_rotated', std_df, x_jitter=.49, y_jitter=.49,fit_reg=False )
# t.axhline(0, color='k', linestyle='-', linewidth=2)
# t.axvline(0, color='k', linestyle='-', linewidth=2)
# t.axes.set_title('Döndürülmüş Standartlaştırılmış Veri')
# plt.show()

## eksenimiz x değerine çok yakın çıkıyor yani points değerine. Demek ki daha çok varyans içeriyor.




