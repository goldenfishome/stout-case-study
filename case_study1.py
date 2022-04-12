#!/usr/bin/env python
# coding: utf-8

# In[11]:


import matplotlib.pyplot as plt
import seaborn  as sns
import pandas   as pd
import numpy    as np
import klib
import plotly.express as px

original_df = pd.read_csv("loans_full_schema.csv")


# In[20]:


##### plot 3
###missing figures
klib.missingval_plot(original_df)

na_col = ["emp_title","annual_income_joint","verification_income_joint",
          "debt_to_income_joint","months_since_last_delinq","months_since_90d_late",
          "months_since_last_credit_inquiry","num_accounts_120d_past_due"]
df = original_df.drop(na_col, axis = 1)
df = df.dropna()


# In[21]:


drop_col = ["emp_title","state","homeownership","verified_income", "annual_income_joint",
            "verification_income_joint","debt_to_income_joint","months_since_last_delinq",
            "earliest_credit_line","months_since_90d_late","months_since_last_credit_inquiry",
            "num_accounts_120d_past_due","loan_purpose","application_type","grade", "sub_grade",
            "issue_month","loan_status","initial_listing_status","disbursement_method"]

numeric_df = original_df.drop(drop_col, axis = 1)

sns.heatmap(numeric_df.corr())


# In[23]:


### plot 1
# how annual income and home ownership affect the interest rate
sns.set_theme()
sns.displot(
    data=df,
    x="interest_rate", 
    #col="time",
    kde=True
    ).set(title='Distribution of Interest rate')
plt.show()


# In[24]:


#### plot 4
sns.set_palette("Pastel1")
sns.set_style("whitegrid")
sns.catplot(
    data=df, 
    kind="violin", 
    x="homeownership", 
    y="interest_rate", 
    hue="application_type", 
    split=True
).set(title='Interest Rate VS Homeownership in Application Type')
plt.show()


# In[25]:


#### plot 5
fig = px.box(
    df,
    x="loan_purpose",
    y="interest_rate",
    labels={"loan_purpose": "Purpose of loan",
           "interest_rate": "Interest rate"},
    title = "Interest Rate in Purpose of loan",
    color = "loan_purpose",
    width=600,
    height=600,
)
fig.show()
#fig.write_html("plot5.html")


# case study 2

# In[1]:


import pandas as pd
import numpy as np

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


# In[2]:


cs_df


# In[7]:


import matplotlib.pyplot as plt
import seaborn  as sns
import plotly.express as px
import altair as alt

df_test = cs_df[["new_customer_revenue","revenue_exisitng_customer"]]
df_test.reset_index(inplace=True)

df_long = pd.melt(df_test,
        id_vars = "year",
       var_name = "revenue_type",
       value_name = "value")

df_long.year = df_long.year.astype('category')

px.bar(df_long, x="year", y="value", color="revenue_type", title="Composition of Total Revenue over 3 Years")


# In[9]:


fig2 = px.bar(
    cs_df.reset_index(),
    x="year",
    y="new_customer",
    width=500,
    height=500,
    labels={"new_customer": "number of new customers"},
     title="Number of New Customers 3 Years"
)
fig2.show()


# In[ ]:




