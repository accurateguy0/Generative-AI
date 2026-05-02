import pandas as pd   
df = pd.read_csv('https://raw.githubusercontent.com/justmarkham/DAT8/master/data/chipotle.tsv', sep='\t')
print(df.head())

#Cleaning the data
df['item_price'] = df['item_price'].str.replace('$', '').astype(float)
df['quantity'] = df['quantity'].astype(int)
df.to_sqlite('chipotle.db', index=False, if_exists='replace')