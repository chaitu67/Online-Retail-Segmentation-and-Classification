/* Create view with cleaned Transactional data*/

CREATE  ALGORITHM = UNDEFINED
DEFINER = `root`@`localhost`
SQL SECURITY DEFINER
VIEW `tran` AS
 SELECT
        `dataset04.OnlineRetail`.`InvoiceNo` AS `InvoiceNo`,
        `dataset04.OnlineRetail`.`StockCode` AS `StockCode`,
        `dataset04.OnlineRetail`.`Description` AS `Description`,
        `dataset04.OnlineRetail`.`Quantity` AS `Quantity`,
        `dataset04.OnlineRetail`.`InvoiceDate` AS `InvoiceDate`,
        `dataset04.OnlineRetail`.`UnitPrice` AS `UnitPrice`,
        `dataset04.OnlineRetail`.`CustomerID` AS `CustomerID`,
        `dataset04.OnlineRetail`.`Country` AS `Country`,
        `dataset04.OnlineRetail`.`InvoiceDateTime` AS `InvoiceDateTime`
    FROM
        `dataset04.OnlineRetail`
    WHERE
        ((`dataset04.OnlineRetail`.`InvoiceNo` <> 0)
            AND (`dataset04.OnlineRetail`.`Quantity` > 0))

/*Transform data based on customers and products*/

/*Customers:*/

SELECT
CustomerID,
sum(Quantity*UnitPrice) as TotalPurchase,
count(distinct StockCode) as NoDistProductsBought,
count(StockCode) as NoProductsBought,
count(distinct Invoiceno) as NoDistTransactions,
DATEDIFF(max(InvoiceDateTime), min(InvoiceDateTime))/count(distinct Invoiceno)as gapbetweentransactions
FROM dataset04.tran
GROUP BY CustomerID ;

/*Products:*/

SELECT StockCode,
COUNT(DISTINCT CustomerID) as "number of customers",
SUM(Quantity*UnitPrice)"revenue",
COUNT(distinct Invoiceno) "no of visits/Transactions",
avg(UnitPrice) as 'avg product price'
FROM dataset04.tran GROUP by  stockcode
