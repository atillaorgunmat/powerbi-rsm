# Data_KPI_Trace Matrix · v3.0  
*Aligned with KPI List v3.0 & Data‑Spec Sheet v3.3.1 (July 2025)*  

| Domain | KPI | Required Fields & Logic | Source Tables | Status | Transform / Aggregation | SCD Impact? | Notes |
|--------|-----|-------------------------|---------------|--------|-------------------------|-------------|-------|
| Sales | Revenue | LineTotal | FactOrderItems | Covered (v3.3.1) | SUM(LineTotal) | No | – |
| Sales | Gross Margin % | StdUnitCost, AllocatedFreight, MarkdownAmount, ProcessingCost, RestockingFee, LineTotal | FactOrderItems; FactOrderReturns | Covered (v3.3.1) | (Revenue – all costs)/Revenue | **Yes (UnitCost)** | Uses Type‑2 product cost |
| Sales | Average Order Value | LineTotal, OrderID | FactOrderItems; FactOrderHeader | Covered (v3.3.1) | SUM(LineTotal) / DISTINCTCOUNT(OrderID) | No | – |
| Sales | Promo Uplift | PromoRevenue, BaselineRevenue | FactOrderItemPromotion; FactOrderItems | Covered (v3.3.1) | (PromoRev – Baseline)/Baseline | No | Baseline via non‑promo filter |
| Sales | Return % | QtyReturned, Qty | FactOrderReturns; FactOrderItems | Covered (v3.3.1) | SUM(QtyReturned)/SUM(Qty) | No | – |
| Sales | Net Profit % | All costs (see Gross Margin) + Freight | FactOrderItems; FactOrderReturns | Covered (v3.3.1) | (Revenue – TotalCost)/Revenue | **Yes** | – |
| Sales | Comp‑Store Sales % (YoY) | LineTotal, StoreID, DateID | FactOrderItems; DimStore; DimDate | Covered (v3.3.1) | YoY calc (same Store) | No | Needs comp‑store flag |
| Operations | Stock on Hand | ClosingQty | FactInventorySnapshot | Covered (v3.3.1) | SUM(ClosingQty) | No | Snapshot fact |
| Operations | Re‑order Frequency | EventTypeID = Reorder | FactInventoryEvents | Covered (v3.3.1) | COUNT(Reorder)/Period | No | – |
| Operations | Shrinkage % | EventTypeID = Damaged/Lost, Qty | FactInventoryEvents | Covered (v3.3.1) | DamagedQty/ReceivedQty | No | – |
| Operations | Delivery Lead‑Time | DateID, RelatedEventID | FactInventoryEvents | Covered (v3.3.1) | AVG(DeliveryDate – ReorderDate) | No | Self‑join by RelatedEventID |
| Operations | Stock‑out Rate | ClosingQty | FactInventorySnapshot | Covered (v3.3.1) | Days ClosingQty=0 / Days | No | – |
| Operations | GMROI | Gross Margin, AvgInventoryCost | FactOrderItems; FactInventorySnapshot | Covered (v3.3.1) | GrossMargin / AvgInvCost | **Yes (UnitCost)** | – |
| Operations | Inventory Age > 90 days % | AgingDays, ClosingQty | FactInventorySnapshot | Covered (v3.3.1) | Qty>90 / TotalQty | No | – |
| Operations | Supplier Fill‑Rate % | Qty, ExpectedQty | FactInventoryEvents | Covered (v3.3.1) | SUM(Qty)/SUM(ExpectedQty) | No | Uses new ExpectedQty column |
| Operations | Weeks of Supply (WOS) | ClosingQty, WeeklySalesQty | FactInventorySnapshot; FactOrderItems | Covered (v3.3.1) | ClosingQty / AvgWeeklySales | No | – |
| CRM | Lead‑to‑Customer % | IsNewLead, IsNewCustomer | DimCustomer | Covered (v3.3.1) | COUNT(NewCust)/COUNT(Leads) | No | Derived flags |
| CRM | High‑Value Share | HighValue | DimCustomer | Covered (v3.3.1) | COUNT(HighValue)/COUNT(AllCust) | No | – |
| CRM | Interactions per Customer | InteractionID, CustomerID | FactCustomerInteractions | Covered (v3.3.1) | COUNT(Interactions)/DISTINCTCOUNT(Cust) | No | – |
| CRM | Churn Rate | AtRisk | DimCustomer | Covered (v3.3.1) | COUNT(AtRisk)/COUNT(TotalCust) | No | – |
| CRM | Customer Lifetime Value (CLTV) | LineTotal, CustomerID | FactOrderItems; DimCustomer | Covered (v3.3.1) | ΣRevenue per Customer | No | – |
| CRM | Customer Acquisition Cost (CAC) | SpendAmount, NewCustomers | FactCampaignSpend; DimCustomer | Covered (v3.3.1) | ΣSpend/ΣNewCust | No | – |
| Cross‑Domain | Sales per Sq Ft | LineTotal, SquareFootage | FactOrderItems; DimStore | Covered (v3.3.1) | Revenue/StoreSqFt | **Yes (SquareFootage)** | – |
| Cross‑Domain | Sell‑Through Rate | UnitsSold, ClosingQty | FactOrderItems; FactInventorySnapshot | Covered (v3.3.1) | UnitsSold/(UnitsSold+EndingInv) | No | – |
| Cross‑Domain | Campaign ROI | PromoRevenue, PromoCost | FactOrderItemPromotion; DimPromotion | Covered (v3.3.1) | (Rev‑Cost)/Cost | No | – |
| Cross‑Domain | Store Conversion Rate % | OrderID, VisitCount | FactOrderHeader; FactFootTraffic | Covered (v3.3.1) | Transactions/Visits | No | Needs FootTraffic fact |
| Cross‑Domain | Promo Redemption Rate % | PromoTransactions, TotalTransactions | FactOrderItemPromotion; FactOrderHeader | Covered (v3.3.1) | Transactions w/ Promo / Total | No | – |
| Cross‑Domain | Incremental Lift % | PromoUnits, BaselineUnits | FactOrderItemPromotion; FactOrderItems | Covered (v3.3.1) | (PromoUnits – Baseline)/Baseline | No | – |
