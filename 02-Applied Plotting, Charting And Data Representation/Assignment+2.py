import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

hashid = "fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89"
df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/{}.csv'.format(hashid))
df.sort(['ID','Date'])
df['Year'], df['Month-Date'] = zip(*df['Date'].apply(lambda x: (x[:4], x[5:])))
df = df[df['Month-Date'] != '02-29']
df['Date'] = pd.to_datetime(df['Date'])

df_max = (df[(df['Element'] == "TMAX") & (df["Date"]>='2005-01-01') & (df["Date"]<='2014-12-31')]
          .groupby(["Month-Date"])
          .aggregate({'Data_Value':np.max})
          )
df_min = (df[(df['Element'] == "TMIN") & (df["Date"]>='2005-01-01') & (df["Date"]<='2014-12-31')]
          .groupby(["Month-Date"])
          .aggregate({'Data_Value':np.min})
          )

temp_min_15 = df[(df['Element'] == 'TMIN') & (df['Year'] == '2015')].groupby('Month-Date').aggregate({'Data_Value':np.min})
temp_max_15 = df[(df['Element'] == 'TMAX') & (df['Year'] == '2015')].groupby('Month-Date').aggregate({'Data_Value':np.max})

broken_min = np.where(temp_min_15['Data_Value'] < df_min['Data_Value'])[0]
broken_max = np.where(temp_max_15['Data_Value'] > df_max['Data_Value'])[0]

plt.rcParams.update({'font.size': 8})

plt.figure()
plt.plot(df_max.values, ".-", color="orange")
plt.plot(df_min.values, ".c-")
plt.scatter(broken_max, temp_max_15.iloc[broken_max], s = 10, c = 'r')
plt.scatter(broken_min, temp_min_15.iloc[broken_min], s = 10, c = 'b')
plt.xlabel('Day of the year')
plt.ylabel('Temperature (Tenths of Degrees C)')
plt.title('Daily climate records')
plt.legend(['2005-2014 record max', '2005-2014 record min','2015 broken high', '2015 broken low'], loc=1,bbox_to_anchor=(1.1, 1.15))
plt.xticks(range(0, len(df_min), 20), df_min.index[range(0, len(df_min), 20)], rotation = '45')
plt.subplots_adjust(bottom=0.25)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().fill_between(range(len(df_min)), df_min["Data_Value"], df_max["Data_Value"], facecolor = 'lightcyan', alpha = 0.5)
plt.show()



