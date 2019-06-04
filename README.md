Executive Summary

•	The considered online retail dataset contains different attributes about each transaction like product code, number of units purchased, customer etc.
•	Each transactional data contains details of products and customers.
•	As a group of data analysts, we have segmented customer and products of the online retail store based on the similarities observed between the customers and products respectively. This would help the client (business owner, business analyst) to make in detail decisions about the behaviour of customers and selling strategy of products.
•	After validating the convergence of cluster analysis, we identified behavior of each cluster.
•	After having a good understanding of portfolio, we made recommendations to online retailer.

Objective

•	To perform meaningful segmentation of customers and products based on the characterises drawn out on the given transactional data.
•	To successfully perform customer and product segmentation the following steps have been taken:
o	Removal of invalid data.
o	Transforming Transaction data to analytical data for analysis.
o	Removal of outliers
o	Preparing data for K-Means clustering
o	Identifying the perfect k value for each entity i.e. (customer or product)
o	Confirming the best K value by using silhouette method
o	Performing K-Means to form clusters.
o	Visualizing the cluster to analyze the behaviour of each cluster
o	Profiling clusters

Data Summary

About Data

Online Retail Transactional data is given as a relational table in MySQL database. Below are the attributes available.

•	InvoiceNo: Invoice number for the transaction.
•	StockCode: It is the generally the product code in the transaction.
•	Description: Product description.
•	Quantity: Quantity purchased in that transaction.
•	InvoiceDate: Date of transaction.
•	UnitPrice: Price of the single unit i.e., product unit price.
•	CustomerID: Id of the customer in that transaction.
•	Country: Transaction in country.
•	InvoiceDateTime: Date and time of the transaction.

Data Cleaning & Extraction

To perform segmentation of customers and products from the given dataset, the steps followed are:

Selecting the appropriate data: [removal of unclear data]

•	Invoice no equal to 0 data removed as the data was untracked.
•	Negative quantity data was removed as the data description for each of these data was inconsistent and contained missing, damaged and null values too which ideally cannot be considered.
o	It cannot be considered as returned item as its not specifically mentioned and could lead to assumptions statements.
o	Even if the data is removed there is neither any impact as the data constitutes to just about 1% of entire data.
•	Thera is a 2% decrease in the transactional data as a process of data cleaning had been done. (541909 to 531281)

 

Transforming the data as per requirements
•	The cleaned data is stored in a view “tran” which is used as a source to perform data transformations.
•	Performed transformations on the cleaned data to obtain number of customers and the number of products with their respective features. These features have been detailly explained in the feature selection section of the report.
•	After transforming the data, the data for customers and products is exported as csv to perform analysis. 
•	The analysis is done on 4340 customers and 3820 products.

Customers Dataset

The final analysis is performed on the 4340 customers as shown below.
 

Products Dataset

The final analysis is performed on the 3820 products as shown below.

Design/Method/Approach

To perform segmentation of customers and products from the given online retail dataset, we have followed the following steps:

•	Selecting the appropriate data
•	Feature selection to support the analysis
•	Transforming the data as per requirements
•	Clean the data and remove outliers 
•	Normalize data
•	Determine the appropriate number of clusters and perform clustering
•	De-normalize data
•	Use metadata from the original dataset to create customer and product profile based on clustering results
Feature Selection

Customer Data Attributes

•	To transform the data from transaction to analytical model we have used RFM customer segmentation model where:[6]
o	R stands for recency-customers distinct purchase of products
o	F stands for frequency-Customers frequency of visit
o	M stands for Monetary- Impact of price value on customers.
o	The attributes used for customers are:
	Total Purchase: Total purchase of all the products by single customer.
	NoDistinctProdBought: Number of distinct products by single customer.
	NoProdBought: Total number of products by single customer.
	NoVisits: Number of visits made by customer.
	Frequency of visits in the total time
•	Frequency of customer visits from the known time is considered as the extra attribute for customer cluster. It is derived by taking the transactional data difference between last transaction and the initial transaction which defines that number of days a customer has known the online store, dividing this by the number of visits gives the average frequency of visits done by a customer over a period.
Product Data Attributes

•	For products the transformation is performed based on the below measure:
o	TotalRevenue: Total revenue generated by single product.
o	Baskets: In how many baskets the product was in.
o	DistinctCustomers: Number of distinct customers purchased that product
o	Average unit price of the product is considered as an extra attribute in the product entity. As it would be helpful to determine whether the range of sales of product is dependent on the unit price too.
Data Cleansing/Outlier Removal

After the formation of analytical cube, we have plotted the data using ggpairs in R, below is the code to plot the data.
 
Finding the outliers for Customer

•	Plotted a scatter plot matrix for customers (columns 2 – 6 are used) to identify the outliers present in the data.

custData<-read.csv (file="customer.csv", header=TRUE, sep=",") 
library(ggplot2)
library(GGally)
library(DMwR)
ggpairs(CustData[,2:6], upper=list(continuous=ggally_points), lower=list(continuous = "points"),title="Customer Data Before outlier removal")

•	b) As we can observe that data points in first column Total purchase greater than 80000 can be considered as outliers as these points are dispersed very far from all the other points.

•	c) We can also observe that data points number of products bought greater than 4000 can also be considered as outliers.

Removing outliers for Customer

To remove the outliers for the conditions total purchase greater than 80000 and number of products bought greater than 4000 we have used below R command.

CustData <- CustData[custData$TotalPurchase < 80000 & CustData$NoProdBought < 4000]
ggpairs(CustData[,2:6],upper=list(continuous=ggally_points),lower=list(continuous="points"),title="Customer Data after outlier removal")

 
Finding outliers for Product

We have followed the same process of removing of outliers for the product data, we have observed that revenue greater than 8000 are outliers as we can observed it from the column revenue.

prodData<-read.csv (file="product.csv", header=TRUE, sep=",")
ggpairs(prodData[,2:6],upper=list(continuous=ggally_points),lower=list(continuous="points"),title="Product Data Before outlier removal")

            

Removing outliers for Product

To remove the outliers for the conditions total purchase greater than 80000 

prodData<- prodData[prodData$TotalPurchase < 80000]

ggpairs(prodData[,2:5],upper=list(continuous=ggally_points),lower=list(continuous="points"),title="Product Data after outlier removal")

 
 
Cluster Analysis

Identifying the exact K values

•	Firstly, transform the data frame by placing the variables that you want the cluster to be built on and remove the remaining attributes like customerid in customers data and stock code in products data.
•	Then we have performed scaling on the data so that, all the data is present in the same scale. Scaling is done to:
i.	Decrease the mean square error between the points
ii.	Reduces the chances of data getting trapped into local minima when it is in search of global min
•	Developed user defines function “withinssrange” that iteratively performs K-means and plotted the results to identify the K value by elbow curve method.
•	With elbow curve method, plotted the number of clusters in x axis and the relative total withinss on y axis. This gives a graph in the shape of an elbow. To identify the exact elbow point we identified the values with highest slop. The value for number of clusters is identified with 8 clusters for customers and 6 clusters for products.

Customer Cluster

Elbow curve for the customers dataset is shown as below
 

Product Cluster

Elbow curve for the products dataset is shown as below

 


•	To confirm on our decision made in elbow method. We used silhouette method to double check the number of clusters i.e. k=8 for customers and k=6 for products.
o	A user defined function “Silh_score” has been created to find the silhouette score of a range of k values. Silhouette score is the ratio of difference between datapoints in one cluster to the nearest cluster and distance between datapoints in the same cluster [1].
o	Taken the top 3 highest silhouette scores and identified if the K value obtained from elbow method lies in one of these. In over case, k=8 and k=6 are justified for customers and products respectively. Thus, the K values for customers is 8 and for products its 6 [1].

Customer Silhouette

Silhouette curve for the customers dataset is shown as below

 

Product Silhouette

Silhouette curve for the products dataset is shown as below

 

Performing K-means clustering

•	K-Means models have been developed for customers and products with a cluster size of 8 and 6 respectively.
•	Identified the withinss for each of the clusters with their sizes and these have been displayed below for both customer and products.[5]
•	The clusters are verified as the best fit for the given dataset by the following conditions:
o	Checked that the ratio of betweenss and tot. withinss when compared to the consequent clusters is not too variant.[1]
o	Ensured that the variance in withinss and betweenss is less when compared to consequent clusters.
o	Considered the clusters with maximum size and ensured the withinss of these clusters are relatively less compared to other K values[2][4].
•	The cluster sizes and the withinss for the customer & product clusters are depicted as below[5]

Customer cluster

 

Product Cluster
 

Cluster Profiling

Customers

Column Binding

After the clusters are formed, we bind the cluster data as a new column to the cleaned customer data using the R command “custDatacluster<-cbind (custData, custcluster$cluster)”[5]. Scatter plot of these clusters is shown as below.[

 



Visualization

Next, we visualized the data using Tableau to assess the weight of each attribute in the clusters.

 

Heat Map
From the visualization, data is categorized and represented as a heat map as shown below.

 

Based on the patterns observed from the numbers in visualization, attribute weightage is split into namely 4 categories. They are as follows:
•	High
•	Average
•	Below Average
•	Low

From the heat map, clusters are named based on the behaviour of the attributes.

Cluster 1 – Regular Loyal Customers
This cluster is named “Regular loyal customers” as the customers in this group are observed to be making highest number of transactions which also includes the highest number if products with a relatively less gap between transactions. This shows they are visiting regularly and generating good income.

Cluster 2 – Window Shopping Customers
This cluster is named “Window shopping customers” as the gap between the transactions is the highest and haven’t done many transactions with a relatively less revenue generated. Most number of the customers fall under this category as this cluster takes the majority share.
Recommendation:
As the greatest number of customers are not providing good returns, measures can be taken to advertise about various products and offers available in the store every day. This may also increase sales as this set of people can spread the mouth-talk to others.

Cluster 3 – Frequent-Low Revenue Customers
This cluster is named “Frequent-low revenue customers” as this group contains the second highest number of customers whose visiting frequency is the highest but generating the lowest revenue.
Recommendation:
After identifying the products bought by these customers, it would be effective to advertise about various products and offers near or around the aisles that these products are placed.

Cluster 4 – Daily Customers
This cluster is named “Daily customers” as the customers in this group are visiting very frequently and even generating a gradual revenue along with willingness to try distinct products.
Recommendation:
Based on the shopping frequency of these customers, incentives or discounts can be provided to these customers.

Cluster 5 – Casual Customers
This cluster is named “Casual customers” as the customers in this group are visiting the store quite frequently and are also willing to try various distinct products along with maintaining a good total purchase amount.

Cluster 6 – Big Customers
This cluster is named “Big customers” as the total purchase amount is the highest with a relatively low number of products being involved in the transaction.

Cluster 7 – Customers on Mission
This cluster is named “Customers on mission” as this set of people are targeting only few products which are not very distinct. As we can observe from the heat map, the gap between transactions as well as the total purchase price is relatively less.
Recommendation:
Company can offer some discounts on these products in order to retain the customers.

Cluster 8 - Wandering Customers
This cluster is named “Wandering customers” as this group of customers are visiting frequently but transactions made by them are the least and they contain the least number of products as well.

Products

Column Binding

After the clusters are formed, we bind the cluster data as a new column to the cleaned customer data using the R command “prodDatacluster<-cbind (prodData, pkmcluster$cluster)”. Scatter plot of these clusters is shown as below.
 

Visualization

Next, we visualized the data using Tableau to assess the weight of each attribute in the clusters.


Heat Map
From the visualization, we categorized the data and represented as a heat map as shown below.

 
Based on the patterns observed from the numbers in visualization, attribute weightage is split into namely 3 categories. They are as follows:
•	High
•	Average
•	Low

From the heat map, clusters are named based on the behaviour of the attributes. Description for the clusters is as follows:

Cluster 1 – Costly Products
This cluster is named “Costly products” as it is observed that the average unit price of the products is highest and very few customers are interested in purchasing them. This behaviour can be seen from the heat map where the number of transactions these products are involved is very less.
Recommendation:
Company can try to create interest for customers in these products to increase revenue.

Cluster 2 – Highly Moving Products
This cluster is named “Highly moving products” as the products in this cluster appeared in high number of transactions and are being bought by a very high number of customers which explains these are moving very fast.
Recommendation:
It is advisable to maintain good stock of these items on all days.

Cluster 3 – Stagnant Products
This cluster is named “Stagnant products” as revenue generated on these products and the number of transactions in which it is present is very low which clearly explains customers has less interest on these products.
Recommendation:
It is not advisable to maintain huge stocks.

Cluster 4 – Low Revenue Generators
This cluster is named “Low revenue generators” as the revenue generated from the products in this group is the lowest in spite of the average unit price being the lowest.

Cluster 5 – High Revenue Generators
This cluster is named “High revenue generators” as these products have appeared in highest number of transactions and the revenue generated is also the highest which also shows that more customers are inclined towards these products.

Cluster 6 – Cheap & Best Products
This cluster is named “Cheap & best products” as it consists of the majority share of the products which are generating a good revenue along with a steady movement.




Conclusion & Next Steps

Customer cluster purchasing statistics on product category

 
Each customer cluster had bought low revenue products on a high scale.
Cheap and best products are not being entertained much by the customers.
Overall, the company can do better in attracting the customers by advertising the products in-order to increase the sales.

As part of further developments, we have Constructed a classification model that classifies the newly given data into its respective clusters. To develop this classification model:
•	we have used random forest algorithm. With this model a customer can be classified into different clusters in with an accuracy of 88%. Similarly, for products the model could predict a new data with an accuracy of 95%.
•	Sample data with same number of data points have been taken for each individual cluster in both products and customers. So as to prevent overfitting of the model while training it.
•	Further to test and validate the model, the remaining data apart from trained data has been split into test and validation data with a test size of 0.3 and 0.4 for customers and products respectively.
•	Heat maps are plotted for both customers and products from the confusion matrix obtained by the prediction done by models   on validation data.




Customers Random Forest model classification heatmap:

The accuracy of the predicted data is 91%.


Products Random Forest model Classification heatmap:

The accuracy of the predicted data is 96%


•	These validations helped us to verify that the model is not over fitted. As the accuracy predicted by the new data is greater than the test accuracy.
•	The further explanation of model is explained near the code.



References

[1] Cluster. (n.d.). Retrieved from https://www.rdocumentation.org/packages/cluster/versions/2.0.9/topics/silhouette
[2]Memisc. (n.d.). Retrieved from
 https://www.youtube.com/watch?v=5TPldC_dC0s
[3]Udacity. (2015, February 23). Some challenges of k-means. Retrieved from https://www.youtube.com/watch?v=e2CdlG5P4WA
[4]Tuitions, L. M. (2017, April 25). K mean clustering algorithm with solve example. Retrieved from https://www.youtube.com/watch?v=YWgcKSa_2ag
[5](n.d.). Retrieved from https://smu.brightspace.com/d2l/le/content/68937/viewContent/494127/View
[6](n.d.). Retrieved from 
https://www.google.com/search?client=safari&rls=en&q=rfm customer segmentation&ie=UTF-8&oe=UTF-8



