# KPI List v1.0 

Domain
KPI
Final Definition / Notes
Source Tables
Sales
Revenue
Σ OrderItem.LineTotal
FactOrderItems

Gross Margin %
(Revenue – Σ (UnitCost × Qty)) / Revenue
FactOrderItems, DimProduct

Average Order Value
Revenue / Distinct Orders
FactOrderItems, OrderHeader

Promo Uplift
(Revenue with Promo – Revenue without) / Revenue without
FactOrderItems, DimPromotion

Return %
Σ Return.Qty / Σ Sold.Qty
FactOrderReturns, FactOrderItems
Operations
Stock on Hand
Latest inventory qty per Product⋅Store
FactInventoryEvents

Re-order Frequency
Count(ReorderRequest) per Product-month
FactInventoryEvents

Shrinkage %
DamagedQty / TotalReceivedQty
FactInventoryEvents

Delivery Lead-Time
Avg(DeliveryDate – ReorderDate)
FactInventoryEvents

Stock-out Rate
DaysOutOfStock / TotalDays
Derived via running balance
CRM / Customer
Lead-to-Customer %
NewCustomers / NewLeads
DimCustomer

High-Value Share
HighValueCustomers / AllCustomers
DimCustomer

Interactions per Customer
Count(Interactions) / Distinct Customers
FactCustomerInteractions

Churn Rate
AtRiskCustomers / TotalCustomers
DimCustomer
Cross-Domain
Sales per Sq Ft
Revenue / Store.SquareFootage
FactOrderItems, DimStore

Sell-Through Rate
QtySold / (QtySold + EndingInventory)
FactOrderItems, FactInventoryEvents

Campaign ROI
(Revenue from Promo – PromoCost) / PromoCost
FactOrderItems, DimPromotion
