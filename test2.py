import numpy as np
import pandas as pd
pd.set_option('max_columns', 100)
sales_data = pd.read_csv("D:\Code\pcsg_test\cust_orders_sanitised.csv", header=0, low_memory=False)
sales_data['Email'].ffill(inplace=True)
sales_data.head()
