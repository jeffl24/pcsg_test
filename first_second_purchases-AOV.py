
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
pd.set_option('max_columns', 100)


# In[2]:

sales_data = pd.read_csv("pcsg_test/shopify_orders_export_20180227.csv", header=0, low_memory=False)
sales_data['Email'].ffill(inplace=True)
sales_data.head()


# In[3]:

sales_data.info()


# In[4]:

sales_data_clean = sales_data.drop(sales_data.columns.to_series()[-11:-1], axis=1)
sales_data_clean


# In[5]:

sales_data['Paid at'] = pd.to_datetime(sales_data['Paid at'])
sales_data['Fulfilled at'] = pd.to_datetime(sales_data['Fulfilled at'])
sales_data['Created at'] = pd.to_datetime(sales_data['Created at'])
sales_data['Fulfilled at'][:15]


# In[6]:

# sales_data_no_na = sales_data[sales_data['Paid at'].notnull()]
sales_data_no_na = sales_data.dropna(subset = ['Paid at'])
sales_data_no_na


# In[57]:

# use df.copy() to avoid altering the source dataframe
unique_customers = sales_data_no_na[['Email', 'Created at', 'Subtotal']].copy()
unique_customers.sort_values(by='Created at', ascending=True, inplace=True)
unique_customers.drop_duplicates(inplace=True)
unique_customers['Rank'] = unique_customers.groupby(['Email'])['Created at'].cumcount()+1
unique_customers.head(20)


# ## unique_customers_adjusted  => Subtotals of more than 10 SGD

# In[8]:

unique_customers_adjusted = unique_customers[unique_customers['Subtotal']>10]
unique_customers_adjusted['Rank'] = unique_customers_adjusted.groupby(['Email'])['Created at'].cumcount()+1


# In[9]:

# To find out what is the highest number of purchases a customer has made
unique_customers_adjusted['Rank'].max()


# ### The customer who's purchased the most frequently is lavie_ind
# ### this gives us a sense of how much an extreme customer would spend throughout
# unique_customers_adjusted[unique_customers_adjusted['Email']=="lavie_ind@yahoo.com"]

# print("unique_customers_first", unique_customers_first['Subtotal'].mean())
# print("unique_customers_adjusted_first", unique_customers_adjusted_first['Subtotal'].mean())
# print("unique_customers_second", unique_customers_second['Subtotal'].mean())
# print("unique_customers_adjusted_second", unique_customers_adjusted_second['Subtotal'].mean())

# In[54]:

right = sales_data[['Email', 'Created at', 'Lineitem sku', 'Lineitem price']].copy()
right['Email'].ffill(inplace=True)
right.head(30)


# In[59]:

sales_with_rank = pd.merge(left=unique_customers_adjusted,
                           right=right,
                           how="left",
                           on=['Email', 'Created at'])
sales_with_rank


# In[60]:

import matplotlib.pyplot as plt
import seaborn as sb
get_ipython().magic('matplotlib inline')
fig, ax = plt.subplots()
fig.set_size_inches(10,5)
# change the rank for different analysis
sales_chart = sales_with_rank[sales_with_rank['Rank'] == 2]['Lineitem sku'].astype(str)
sales_chart.value_counts()[:20].plot(ax=ax, kind='barh').invert_yaxis()

plt.title('Top 20 SKUs in Second Time Purchases')
plt.savefig('Top 20 SKUs in Second Time Purchases.png')
plt.show()
