#Plotting Correlation matrix after clustering for customers and products

#import required libraraies

import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

#reading the csv which has been exported after performing clustering
#Both customers and products are imported to Dataframes

cust=pd.read_csv("~/CustomerClusterfinal.csv ")
prod=pd.read_csv("~/ProductClusterfinal.csv ")


#removing the customerid and StockCode in customers and products clusters
#To visualize the dataframes based on their clusters.
custvi=cust.iloc[:,2:8]
prodvi=prod.iloc[:,2:7]
#visualizing the data using correlation matrix for both customers and products
plot=sns.pairplot(custvi,hue="custcluster$cluster",palette="husl")
plot=sns.pairplot(prodvi,hue="pkmcluster$cluster",palette="hls")

//Random Forest Classification modeling with code for heatmap of confusion matrix

#Identifying the size of each cluster in customers and products
def size_of_clusters(data,n):
    for i in range(1,n+1):
        print(str(i)+":"+str(len(data[data.iloc[:,-1]==i])))

size_of_clusters(product_sample,6)
#forming a sample dataframe which has all clusters in same ratio
def split_cluster(data,n,split_range,Max_nvalue,min_nvalue):
    df=pd.DataFrame()
    for i in range(1,n+1):
        if len(data[data.iloc[:,-1]==i])>split_range:
            df=df.append(data[data.iloc[:,-1]==i].sample(n=Max_nvalue))
            df=df.sample(frac=1).reset_index(drop=True)
        elif len(data[data.iloc[:,-1]==i])<=split_range:
            df=df.append(data[data.iloc[:,-1]==i].sample(n=min_nvalue))
            df=df.sample(frac=1).reset_index(drop=True)
    return df

customer_sample=split_cluster(cust,8,25,25,10)
product_sample=split_cluster(prod,6,40,50,50)


#Dividing the data into Train data, Test Data and validation data
xcust_train=customer_sample.iloc[:,2:7]
ycust_train=customer_sample.iloc[:,-1]
xprod_train=product_sample.iloc[:,2:6]
yprod_train=product_sample.iloc[:,-1]
xcust_test,xcust_validate,ycust_test,ycust_validate=train_test_split(cust.iloc[:,2:7],cust.iloc[:,-1],test_size=0.3)
xprod_test,xprod_validate,yprod_test,yprod_validate=train_test_split(prod.iloc[:,2:6],prod.iloc[:,-1],test_size=0.5)


#Devloping a Random Forest model for customers and trainning the model.testing it using test data.
modelcustomer=RandomForestClassifier(n_estimators=12)
modelcustomer.fit(xcust_train,ycust_train)
modelcustomer.score(xcust_test,ycust_test)


#Validating the model using the validate data to ensure that the model is not overfitted.
modelcustomer.score(xcust_validate,ycust_validate)


#Devloping a Random Forest model for Products and trainning the model.testing it using test data.
modelproduct=RandomForestClassifier(n_estimators=10)
modelproduct.fit(xprod_train,yprod_train)
modelproduct.score(xprod_test,yprod_test)


#Validating the model using the validate data to ensure that the model is not overfitted.
modelproduct.score(xprod_validate,yprod_validate)


#Predicting the labels or cluster numbers for the validation data for both customers and products
ycust_predict=modelcustomer.predict(xcust_validate)
yprod_predict=modelproduct.predict(xprod_validate)


#Constructing a heatmap to view the confusion matrix of customers validation data.
cust_heat=confusion_matrix(ycust_validate, ycust_predict)
sns.heatmap(cust_heat,annot=True,cmap="RdBu_r",xticklabels=[1,2,3,4,5,6,7,8],yticklabels=[1,2,3,4,5,6,7,8])

#Constructing a heatmap to view the confusion matrix of Products validation data.
prod_heat=confusion_matrix(yprod_validate, yprod_predict)
sns.heatmap(prod_heat,annot=True,cmap="BuGn_r",xticklabels=[1,2,3,4,5,6],yticklabels=[1,2,3,4,5,6])
