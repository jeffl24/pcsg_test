
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
pd.set_option('max_columns', 100)


# In[3]:

sales_data = pd.read_csv("shopify_orders_export_20180129.csv", header = 0, low_memory=False)
sales_data['Email'].ffill(inplace=True)
sales_data


# In[4]:

sales_data.info()


# In[5]:

sales_data_clean = sales_data.drop(sales_data.columns.to_series()[-11:-1], axis=1)
sales_data_clean


# In[6]:

sales_data['Paid at'] = pd.to_datetime(sales_data['Paid at'])
sales_data['Fulfilled at'] = pd.to_datetime(sales_data['Fulfilled at'])
sales_data['Created at'] = pd.to_datetime(sales_data['Created at'])
# sales_data['Combined Time Serial'] = pd.to_datetime(sales_data['Combined Time Serial'])
sales_data['Fulfilled at'][:15]


# In[11]:

transaction_sample = sales_data[['Name', 'Email']]
transaction_count = transaction_sample.groupby('Name').count()
transaction_count['Email'].mean()


# In[20]:

import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
transaction_count.plot.hist(bins=100)
plt.title("Number of SKUs purchased in each transaction")
plt.savefig("Number of SKUs purchased in each transaction.png")
plt.show()


# In[6]:

'''unique_cust_group = pd.DataFrame(unique_customers.groupby(['Email']))
unique_cust_group['TranCode'] = unique_cust_group.cumcount()+1
unique_cust_group
# unique_customers['TranCode']=unique_customers.groupby('Email').cumcount()+1
# unique_customers
'''
'''unique_customers['Email'].ffill(axis=0,inplace=True )
unique_customers.drop_duplicates(inplace=True)
unique_customers.sort_values(by='Created at', ascending=False, inplace=True)
pd.DataFrame(unique_customers.groupby('Email').cumcount())
'''
unique_customers = sales_data[['Email', 'Created at']].copy()
unique_customers['Email'].ffill(axis=0,inplace=True )
unique_customers.sort_values(by='Created at', ascending=True, inplace=True)
unique_customers.drop_duplicates(inplace=True)
# unique_pivot = pd.DataFrame(unique_customers.groupby(['Email']).cumcount()+1)
unique_customers


# In[7]:

unique_customers['Rank'] = unique_customers.groupby(['Email'])['Created at'].cumcount()+1
unique_customers


# In[8]:

right = sales_data[['Email', 'Created at', 'Lineitem sku', 'Lineitem price']].copy()
right['Email'].ffill(inplace=True)
right.head()


# In[ ]:




# In[9]:

# sales_with_rank = pd.merge(unique_customers, right, how='left', left_on=['Email', 'Created at'], right_on=['Email', 'Created at'])
sales_with_rank = pd.merge(unique_customers, right, how="left", on=['Email', 'Created at'])
sales_with_rank


# In[10]:

sales_with_rank[sales_with_rank['Rank']==1]


# In[19]:

'''first_sales = sales_with_rank[sales_with_rank['Rank']==1].copy() #
first_sales.drop(['Rank', "Lineitem price"], inplace=True, axis=1)
#first_sales_dummy = pd.get_dummies(first_sales, ['Lineitem sku'])
#first_sales_dummy
first_sales
first_sales.to_excel("First Purchases.xlsx")'''

second_sales = sales_with_rank[sales_with_rank['Rank']==2].copy() #
second_sales.drop(['Rank', "Lineitem price"], inplace=True, axis=1)
#first_sales_dummy = pd.get_dummies(first_sales, ['Lineitem sku'])
#first_sales_dummy
second_sales
second_sales.to_excel("Second Purchases.xlsx")


# In[12]:

'''first_sales_dummy = pd.get_dummies(first_sales, columns=['Lineitem sku'], prefix="",  prefix_sep="")
first_sales_dummy'''
second_sales_dummy = pd.get_dummies(second_sales, columns=['Lineitem sku'], prefix="",  prefix_sep="")
second_sales_dummy


# In[13]:

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
first_sales['Lineitem sku'].value_counts().plot(ax=ax, kind='bar', figsize=(50, 5))
plt.savefig("second_purchases.pdf", dpi=300)
plt.show()

get_ipython().magic('matplotlib inline')

# data['Points'].value_counts().plot(ax=ax, kind='bar')


# In[ ]:



