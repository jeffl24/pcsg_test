
# coding: utf-8

# ### Source: 
# http://www.gregreda.com/2015/08/23/cohort-analysis-with-python/
# 
# Dataset Needed: D:\Code\pcsg_test\relay-foods.xlsx

# In[1]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

pd.set_option('max_columns', 50)
mpl.rcParams['lines.linewidth'] = 2

get_ipython().magic('matplotlib inline')
df = pd.read_excel('relay-foods.xlsx')


# In[2]:

# Create a period column based on the OrderDate
df['OrderPeriod'] = df.OrderDate.apply(lambda x: x.strftime('%Y-%m'))
df.head()


# ## 2. Determine the user's cohort group (based on their first order)
# 
# Create a new column called CohortGroup, which is the year and month in which the user's first purchase occurred.

# In[3]:

df.set_index('UserId', inplace=True)

df['CohortGroup'] = df.groupby(level=0)['OrderDate'].min().apply(lambda x: x.strftime('%Y-%m'))
df.reset_index(inplace=True)
df.head()


# In[4]:

grouped = df.groupby(['CohortGroup', 'OrderPeriod'])

cohorts = grouped.agg({'UserId': pd.Series.nunique,
                      'OrderId': pd.Series.nunique,
                      'TotalCharges': np.sum})

cohorts.rename(columns={'UserId': 'TotalUsers',
                       'OrderId': 'TotalOrders'},
              inplace=True)

cohorts.head(10)


# ### 4. Label the CohortPeriod for each CohortGroup
# We want to look at how each cohort has behaved in the months following their first purchase, so we'll need to *index each cohort to their first purchase month.* For example, CohortPeriod = 1 will be the cohort's first month, CohortPeriod = 2 is their second, and so on.
# 
# This allows us to compare cohorts across various stages of their lifetime.

# In[5]:

cohorts_2 = cohorts.groupby(level=1)

for key, item in cohorts_2:
    print(cohorts_2.get_group(key), '\n\n')


# In[6]:

cohorts_2.describe()


# In[7]:

def cohort_period(df):
    """
    Creates a `CohortPeriod` column, which is the Nth period based on the user's first purchase.
    
    Example
    -------
    Say you want to get the 3rd month for every user:
        df.sort(['UserId', 'OrderTime', inplace=True)
        df = df.groupby('UserId').apply(cohort_period)
        df[df.CohortPeriod == 3]
    """
    df['CohortPeriod'] = np.arange(len(df)) + 1
    return df

cohorts = cohorts.groupby(level=0).apply(cohort_period)
cohorts.head()


# ### 5. Make sure we did all that right
# Let's test data points from the original DataFrame with their corresponding values in the new cohorts DataFrame to make sure all our data transformations worked as expected. As long as none of these raise an exception, we're good.

# x = df[(df.CohortGroup == '2009-01') & (df.OrderPeriod == '2009-01')]
# y = cohorts.loc[('2009-01', '2009-01')]
# 
# assert(x['UserId'].nunique() == y['TotalUsers'])
# assert(x['TotalCharges'].sum().round() == y['TotalCharges'].round())
# assert(x['OrderId'].nunique() == y['TotalOrders'])
# 
# x = df[(df.CohortGroup == '2009-01') & (df.OrderPeriod == '2009-09')]
# y = cohorts.loc[('2009-01', '2009-09')]
# 
# assert(x['UserId'].nunique() == y['TotalUsers'])
# assert(x['TotalCharges'].sum().round() == y['TotalCharges'].round())
# assert(x['OrderId'].nunique() == y['TotalOrders'])
# 
# x = df[(df.CohortGroup == '2009-05') & (df.OrderPeriod == '2009-09')]
# y = cohorts.loc[('2009-05', '2009-09')]
# 
# assert(x['UserId'].nunique() == y['TotalUsers'])
# assert(x['TotalCharges'].sum().round() == y['TotalCharges'].round())
# assert(x['OrderId'].nunique() == y['TotalOrders'])

# ### User Retention by Cohort Group
# We want to look at the percentage change of each CohortGroup over time -- not the absolute change.
# 
# To do this, we'll first need to create a pandas Series containing each CohortGroup and its size.

# In[9]:

#  reindex the DataFrame
cohorts.reset_index(inplace=True)
cohorts.set_index(['CohortGroup', 'CohortPeriod'], inplace=True)

# create a Series holding the total size of each CohortGroup
cohort_group_size = cohorts['TotalUsers'].groupby(level=0).first()
cohort_group_size.head()


# Now, we'll need to divide the TotalUsers values in cohorts by cohort_group_size. Since DataFrame operations are performed based on the indices of the objects, we'll use unstack on our cohorts DataFrame to create a matrix where each column represents a CohortGroup and each row is the CohortPeriod corresponding to that group.
# 
# To illustrate what unstack does, recall the first five TotalUsers values:

# In[10]:

cohorts['TotalUsers'].head()


# And here's what they look like when we unstack the CohortGroup level from the index:

# In[11]:

cohorts['TotalUsers'].unstack(0).head(10)


# Now, we can utilize **broadcasting** to divide each column by the corresponding cohort_group_size.
# 
# The resulting DataFrame, user_retention, contains the percentage of users from the cohort purchasing within the given period. For instance, 38.4% of users in the 2009-03 purchased again in month 3 (which would be May 2009).

# In[12]:

user_retention = cohorts['TotalUsers'].unstack(0).divide(cohort_group_size, axis=1)
user_retention.head(10)


# Finally, we can plot the cohorts over time in an effort to spot behavioral differences or similarities. Two common cohort charts are line graphs and heatmaps, both of which are shown below.
# 
# Notice that the first period of each cohort is 100% -- this is because our cohorts are based on each user's first purchase, meaning everyone in the cohort purchased in month 1.

# In[13]:

user_retention[['2009-06', '2009-07', '2009-08']].plot(figsize=(10,5))
plt.title('Cohorts: User Retention')
plt.xticks(np.arange(1, 12.1, 1))
plt.xlim(1, 12)
plt.ylabel('% of Cohort Purchasing');


# In[14]:

import seaborn as sns
sns.set(style='white')

plt.figure(figsize=(12, 8))
plt.title('Cohorts: User Retention')
sns.heatmap(user_retention.T, mask=user_retention.T.isnull(), annot=True, fmt='.0%');


# we can see from the above chart that fewer users tend to purchase as time goes on.
# 
# However, we can also see that the 2009-01 cohort is the strongest, which enables us to ask targeted questions about this cohort compared to others: 
# 
# what other attributes (besides first purchase month) do these users share which might be causing them to stick around? How were the majority of these users acquired? Was there a specific marketing campaign that brought them in? Did they take advantage of a promotion at sign-up? The answers to these questions would inform future marketing and product efforts.
