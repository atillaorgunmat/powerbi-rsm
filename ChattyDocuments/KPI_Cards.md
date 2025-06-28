# Sales KPIs

## Revenue
**Domain:** Sales  
**Definition:** Σ OrderItem.LineTotal  
**Source Tables & Fields:** FactOrderItems.LineTotal  
**Calculation Logic:** SUM(LineTotal)  
**Owner:** Governor  
**Refresh Cadence:** Daily  

## Gross Margin %
**Domain:** Sales  
**Definition:** (Revenue – Σ (UnitCost × Qty)) / Revenue  
**Source Tables & Fields:** FactOrderItems, DimProduct  
**Calculation Logic:** (SUM(LineTotal) - SUM(UnitCost * Quantity)) / SUM(LineTotal)  
**Owner:** Governor  
**Refresh Cadence:** Daily  

## Average Order Value
**Domain:** Sales  
**Definition:** Revenue / Distinct Orders  
**Source Tables & Fields:** FactOrderItems, OrderHeader  
**Calculation Logic:** SUM(LineTotal) / DISTINCTCOUNT(OrderID)  
**Owner:** Governor  
**Refresh Cadence:** Daily  

## Promo Uplift
**Domain:** Sales  
**Definition:** (Revenue with Promo – Revenue without) / Revenue without  
**Source Tables & Fields:** FactOrderItems, DimPromotion  
**Calculation Logic:** (PromoRevenue - NonPromoRevenue) / NonPromoRevenue  
**Owner:** Governor  
**Refresh Cadence:** Weekly  

## Return %
**Domain:** Sales  
**Definition:** Σ Return.Qty / Σ Sold.Qty  
**Source Tables & Fields:** FactOrderReturns, FactOrderItems  
**Calculation Logic:** SUM(ReturnQty) / SUM(SoldQty)  
**Owner:** Governor  
**Refresh Cadence:** Weekly  

# Operations KPIs

## Stock on Hand
**Domain:** Operations  
**Definition:** Latest inventory qty per Product⋅Store  
**Source Tables & Fields:** FactInventoryEvents  
**Calculation Logic:** Latest Quantity per Product-Store combination  
**Owner:** Governor  
**Refresh Cadence:** Daily  

## Re-order Frequency
**Domain:** Operations  
**Definition:** Count(ReorderRequest) per Product-month  
**Source Tables & Fields:** FactInventoryEvents  
**Calculation Logic:** COUNT(ReorderRequest) by Product per Month  
**Owner:** Governor  
**Refresh Cadence:** Monthly  

## Shrinkage %
**Domain:** Operations  
**Definition:** DamagedQty / TotalReceivedQty  
**Source Tables & Fields:** FactInventoryEvents  
**Calculation Logic:** SUM(DamagedQty) / SUM(ReceivedQty)  
**Owner:** Governor  
**Refresh Cadence:** Monthly  

## Delivery Lead-Time
**Domain:** Operations  
**Definition:** Avg(DeliveryDate – ReorderDate)  
**Source Tables & Fields:** FactInventoryEvents  
**Calculation Logic:** AVG(DeliveryDate - ReorderDate)  
**Owner:** Governor  
**Refresh Cadence:** Monthly  

## Stock-out Rate
**Domain:** Operations  
**Definition:** DaysOutOfStock / TotalDays  
**Source Tables & Fields:** Derived via running balance  
**Calculation Logic:** SUM(DaysOutOfStock) / TotalDays  
**Owner:** Governor  
**Refresh Cadence:** Monthly  

# Executive & CRM KPIs

## Lead-to-Customer %
**Domain:** CRM/Executive  
**Definition:** NewCustomers / NewLeads  
**Source Tables & Fields:** DimCustomer  
**Calculation Logic:** COUNT(NewCustomers) / COUNT(NewLeads)  
**Owner:** Governor  
**Refresh Cadence:** Monthly  

## High-Value Share
**Domain:** CRM/Executive  
**Definition:** HighValueCustomers / AllCustomers  
**Source Tables & Fields:** DimCustomer  
**Calculation Logic:** COUNT(HighValueCustomers) / COUNT(AllCustomers)  
**Owner:** Governor  
**Refresh Cadence:** Monthly  

## Interactions per Customer
**Domain:** CRM/Executive  
**Definition:** Count(Interactions) / Distinct Customers  
**Source Tables & Fields:** FactCustomerInteractions  
**Calculation Logic:** COUNT(Interactions) / DISTINCTCOUNT(CustomerID)  
**Owner:** Governor  
**Refresh Cadence:** Monthly  

## Churn Rate
**Domain:** CRM/Executive  
**Definition:** AtRiskCustomers / TotalCustomers  
**Source Tables & Fields:** DimCustomer  
**Calculation Logic:** COUNT(AtRiskCustomers) / COUNT(TotalCustomers)  
**Owner:** Governor  
**Refresh Cadence:** Monthly  

## Sales per Sq Ft
**Domain:** CRM/Executive  
**Definition:** Revenue / Store.SquareFootage  
**Source Tables & Fields:** FactOrderItems, DimStore  
**Calculation Logic:** SUM(Revenue) / SUM(StoreSquareFootage)  
**Owner:** Governor  
**Refresh Cadence:** Monthly  

## Sell-Through Rate
**Domain:** CRM/Executive  
**Definition:** QtySold / (QtySold + EndingInventory)  
**Source Tables & Fields:** FactOrderItems, FactInventoryEvents  
**Calculation Logic:** SUM(QtySold) / (SUM(QtySold) + SUM(EndingInventory))  
**Owner:** Governor  
**Refresh Cadence:** Monthly  

## Campaign ROI
**Domain:** CRM/Executive  
**Definition:** (Revenue from Promo – PromoCost) / PromoCost  
**Source Tables & Fields:** FactOrderItems, DimPromotion  
**Calculation Logic:** (SUM(RevenueFromPromo) - SUM(PromoCost)) / SUM(PromoCost)  
**Owner:** Governor  
**Refresh Cadence:** Monthly  
