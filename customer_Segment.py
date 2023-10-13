import pandas as pd
import numpy as np
df=pd.read_csv(r'E:\Gayathri\Self_projects\bank_transactions.csv')

#%%

import matplotlib.pyplot as plt
import seaborn as sns
df.dropna(inplace=True)

df.drop(df[df['CustGender']=='T'].index,inplace=True)
df['CustomerDOB']=pd.DatetimeIndex(df['CustomerDOB'])


df['TransactionDate']=pd.DatetimeIndex(df['TransactionDate'])


#%%

df['CustomerAge']=df['TransactionDate'].dt.year-df['CustomerDOB'].dt.year

#%%

df.drop(columns=['CustomerDOB','TransactionTime'],inplace=True)
#%%


df['TransactionDate1']=df['TransactionDate']
df['TransactionDate2']=df['TransactionDate']



# Z - Score
# print((df['TransactionAmount (INR)']-df['TransactionAmount (INR)'].mean())/df['TransactionAmount (INR)'].std())



#%%


MRF_df = df.groupby("CustomerID").agg({
                                      "TransactionID" : "count",
                                      "CustGender" : "first",
                                      "CustLocation":"first",
                                      "CustAccountBalance"  : "mean",
                                      "TransactionAmount (INR)" : "mean",
                                      "CustomerAge" : "median",
                                      "TransactionDate2":"max",
                                      "TransactionDate1":"min",
                                      "TransactionDate":"median"
                      })

MRF_df = MRF_df.reset_index()
MRF_df.head()

#%%


MRF_df.drop(columns=["CustomerID"],inplace=True)

MRF_df.rename(columns={"TransactionID":"Frequency"},inplace=True)
MRF_df['Recency']=df["TransactionDate"].max()-MRF_df['TransactionDate2']

MRF_df['Recency']=MRF_df['Recency'].astype(str)

MRF_df['Recency']=MRF_df['Recency'].str.replace(' days','')



#%%

sns.scatterplot(x='TransactionAmount (INR)',y='CustAccountBalance',data=MRF_df)

#%%

MRF_df.drop(columns=["TransactionDate1","TransactionDate2",'TransactionDate'],inplace=True)

#%%
 
MRF_df['Recency']=MRF_df['Recency'].astype(int)
#%%

# Define the breakpoints and labels
breakpoints = [0, 90, 180, np.inf]
labels = [1, 2, 3]

# Create the 'Recency_Category' column using pandas.cut
MRF_df['Recency_Category'] = pd.cut(MRF_df['Recency'], bins=breakpoints, labels=labels, right=False)

# Print the resulting DataFrame
print(MRF_df)
#%%

MRF_df.drop(columns=["Recency"],inplace=True)

#%%
from sklearn import preprocessing

label_encoder = preprocessing.LabelEncoder()
# Encode labels in column 'species'.
MRF_df['CustGender']= label_encoder.fit_transform(MRF_df['CustGender'])

# MRF_df['CustLocation']= label_encoder.fit_transform(MRF_df['CustLocation'])
MRF_df.drop(columns=["CustLocation"],inplace=True)

from sklearn.cluster import KMeans

# Generate sample data for demonstration (replace this with your data)

# Calculate WCSS for different values of k (number of clusters)
wcss = []
for k in range(1, 11):  # Try different values of k
    kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(MRF_df.iloc[:,:-1])
    wcss.append(kmeans.inertia_)  # Inertia is the WCSS value
#%%
# Plot the elbow graph
plt.figure(figsize=(8, 6))
plt.plot(range(1, 11), wcss, marker='o', linestyle='--')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('WCSS')
plt.grid(True)
plt.show()

#%%

kmeans = KMeans(n_clusters=4, init='k-means++', max_iter=300, n_init=10, random_state=0)

#%%
kmeans.fit(MRF_df.iloc[:,:-2])


#%%

MRF_df['Customer Segmentation']=kmeans.labels_

#%%
plt.figure(num=None, figsize=(20, 20), facecolor='w', edgecolor='k')
plt.scatter(MRF_df['CustomerAge'], MRF_df['TransactionAmount (INR)'])


#%%

plt.scatter(MRF_df[MRF_df['Customer Segmentation']==2].iloc[:,3] , MRF_df[MRF_df['Customer Segmentation']==2].iloc[:,4] , color = 'red')
plt.scatter(MRF_df[MRF_df['Customer Segmentation']==1].iloc[:,3] , MRF_df[MRF_df['Customer Segmentation']==1].iloc[:,4] , color = 'black')
plt.scatter(MRF_df[MRF_df['Customer Segmentation']==0].iloc[:,3] , MRF_df[MRF_df['Customer Segmentation']==0].iloc[:,4] , color = 'green')
plt.scatter(MRF_df[MRF_df['Customer Segmentation']==3].iloc[:,3] , MRF_df[MRF_df['Customer Segmentation']==3].iloc[:,4] , color = 'pink')
plt.show()


#%%
u_labels = MRF_df['Customer Segmentation'].unique().tolist()
 
#plotting the results:
 
for i in u_labels:
    plt.scatter(MRF_df['Customer Segmentation' == i , 3] , MRF_df['Customer Segmentation' == i , 4])
plt.legend()
plt.show()