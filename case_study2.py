#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn  as sns
import plotly.express as px
import altair as alt


df = pd.read_csv("casestudy.csv")
df.rename(columns = {"Unnamed: 0":"id"}, inplace = True)

######## Total revenue for the current year
cs_df = df.groupby("year").sum().rename(columns = {"net_revenue":"total_revenue"}).drop(["id"],axis = 1)

######## New Customer Revenue e.g. new customers not present in previous year only & New Customers
df_new_cus = df.groupby('customer_email').min()
df_new_cus["new_customer"] = True

cs_df = pd.concat([cs_df, 
                   df_new_cus.groupby("year").sum().rename(columns = {"net_revenue":"new_customer_revenue"})],
                  axis = 1).drop(["id"],axis = 1)


####### Existing Customer Revenue Current Year & Existing Customer Growth. 
df = pd.merge(df, df_new_cus[["id","new_customer"]], how="left",on = "id")
df.new_customer = df.new_customer.fillna(False)

cs_df["revenue_exisitng_customer"] = cs_df["total_revenue"] - cs_df["new_customer_revenue"]
cs_df["exisitng_customer_growth"] = cs_df["revenue_exisitng_customer"] - cs_df["revenue_exisitng_customer"].shift(1)


###### Revenue lost from attrition
cs_df["revenue_lost_attrition"] = cs_df["total_revenue"].shift(1) - cs_df["revenue_exisitng_customer"]

###### Existing Customer Revenue Prior Year
cs_df["revenue_exisitng_customer_prior"] = cs_df["revenue_exisitng_customer"].shift(1)


###### Total Customers Current Year
cs_df["total_customer"] = df.groupby("year").count().id


###### Total Customers Previous Year
cs_df["total_customer_prior"] = cs_df["total_customer"].shift(1)


##### Lost Customers
cs_df["lost_customers"] = cs_df["total_customer"].shift(1) - (cs_df["total_customer"]-cs_df["new_customer"])


# In[6]:


cs_df


# In[24]:


plt.bar(cs_df.reset_index()["year"], cs_df.new_customer_revenue, color='r')
plt.bar(cs_df.reset_index()["year"], cs_df.revenue_exisitng_customer, color='b')
plt.xlabel("Year")
plt.ylabel("value")
plt.legend(["new_customer_revenue", "revenue_exisitng_customer"])
plt.show()


# This plot above has shown the composition of total revenue over 3 years. According to the plot, year 2017 has the highest total revenue, year 2015 ranks the second and year 2016 ranks the last. The new customer revenue has the similar trend as the total revenue. 

# In[29]:


plt.bar(cs_df.reset_index()["year"], cs_df.new_customer)
plt.xlabel("Year")
plt.ylabel("number of new customers")
plt.show()


# According to the plot above, it shows that year 2015 has the highest number of the new customers. 
