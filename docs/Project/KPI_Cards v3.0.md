<!--‑‑‑
KPI_ID: KPI‑001
Name: Revenue
Domain: Sales
Owner: Governor
Refresh: Daily
Definition: Total sales revenue (Σ LineTotal).
Formula_SQL: SUM(FOI.LineTotal)
Formula_DAX: SUM(FactOrderItems[LineTotal])
Data_Sources: FactOrderItems.LineTotal
Dimensions: Date, Store, Product
Visual: Card + trend
‑‑‑>
### KPI‑001 – Revenue

Total gross revenue from all item lines. This is the primary driver for sales dashboards and is used in many derivative KPIs such as Gross Margin % and Average Order Value.

---

<!--‑‑‑
KPI_ID: KPI‑002
Name: Gross Margin %
Domain: Sales
Owner: Governor
Refresh: Daily
Definition: Profit after direct product costs, freight, markdowns, processing, restocking fees.
Formula_SQL: (Revenue – (StdUnitCost × Qty + ActUnitCost + AllocatedFreight + MarkdownAmount + ProcessingCost + RestockingFee)) / Revenue
Formula_DAX: DIVIDE([Revenue] – [Total Cost],[Revenue])
Data_Sources: FactOrderItems.StdUnitCost, FactOrderReturns.*
Dimensions: Date, Store, Product
Visual: Card + waterfall
‑‑‑>
### KPI‑002 – Gross Margin %

Measures profitability after all direct costs. A falling trend pinpoints eroding price discipline or rising COGS.

---

<!--‑‑‑
KPI_ID: KPI‑003
Name: Average Order Value
Domain: Sales
Owner: Governor
Refresh: Daily
Definition: Average revenue per distinct order.
Formula_SQL: SUM(LineTotal) / DISTINCTCOUNT(OrderID)
Formula_DAX: DIVIDE([Revenue],DISTINCTCOUNT(FactOrderHeader[OrderID]))
Data_Sources: FactOrderItems.LineTotal, FactOrderHeader.OrderID
Dimensions: Date, Store, Customer
Visual: Card
‑‑‑>
### KPI‑003 – Average Order Value

Tracks ticket size; rising AOV often implies better cross‑sell or price mix.

---

<!--‑‑‑
KPI_ID: KPI‑004
Name: Promo Uplift
Domain: Sales
Owner: Governor
Refresh: Weekly
Definition: Sales lift attributed to promotions.
Formula_SQL: (PromoRevenue – BaselineRevenue) / BaselineRevenue
Formula_DAX: DIVIDE([Promo Revenue] – [Baseline Revenue],[Baseline Revenue])
Data_Sources: FactOrderItemPromotion.PromoRevenue, FactOrderItems.LineTotal
Dimensions: Date, Store, Promotion
Visual: Clustered column vs baseline
‑‑‑>
### KPI‑004 – Promo Uplift

Shows % revenue increase versus non‑promo baseline. Used by marketing to decide which campaigns to repeat.

---

<!--‑‑‑
KPI_ID: KPI‑005
Name: Return %
Domain: Sales
Owner: Governor
Refresh: Weekly
Definition: Percentage of sold items returned.
Formula_SQL: SUM(QtyReturned)/SUM(Qty)
Formula_DAX: DIVIDE([Returned Qty],[Qty Sold])
Data_Sources: FactOrderReturns.QtyReturned, FactOrderItems.Qty
Dimensions: Date, Store, Product, ReturnReason
Visual: Line
‑‑‑>
### KPI‑005 – Return %

High return rates flag quality or fulfilment issues; drill by Return Reason for root cause.

---

<!--‑‑‑
KPI_ID: KPI‑006
Name: Net Profit %
Domain: Sales
Owner: Governor
Refresh: Monthly
Definition: Profit after all direct & indirect product‑related costs.
Formula_SQL: (Revenue – COGS – Freight – Markdown – ProcessingCost – RestockingFee) / Revenue
Formula_DAX: DIVIDE([Revenue] – [Total Cost],[Revenue])
Data_Sources: FactOrderItems, FactOrderReturns
Dimensions: Date, Store
Visual: Card
‑‑‑>
### KPI‑006 – Net Profit %

Ultimate bottom‑line metric before overhead allocation.

---

<!--‑‑‑
KPI_ID: KPI‑007
Name: Comp‑Store Sales % (YoY)
Domain: Sales
Owner: Governor
Refresh: Monthly
Definition: Same‑store sales growth YoY.
Formula_SQL: (CY Rev – PY Rev)/PY Rev
Formula_DAX: DIVIDE([CY Revenue] – [PY Revenue],[PY Revenue])
Data_Sources: FactOrderItems, DimStore, DimDate
Dimensions: Store
Visual: Bar + YoY arrow
‑‑‑>
### KPI‑007 – Comp‑Store Sales % (YoY)

Strips out new‑store noise to gauge organic growth.

---

<!--‑‑‑
KPI_ID: KPI‑008
Name: Stock on Hand
Domain: Operations
Owner: Governor
Refresh: Daily
Definition: Latest snapshot quantity of stock per product and store.
Formula_SQL: SUM(ClosingQty)
Formula_DAX: SUM(FactInventorySnapshot[ClosingQty])
Data_Sources: FactInventorySnapshot.ClosingQty
Dimensions: Date, Store, Product
Visual: Matrix
‑‑‑>
### KPI‑008 – Stock on Hand

Core inventory balance used by Ops & Merchandising.

---

<!--‑‑‑
KPI_ID: KPI‑009
Name: Re‑order Frequency
Domain: Operations
Owner: Governor
Refresh: Monthly
Definition: Frequency of reordering products.
Formula_SQL: COUNT(ReorderEvent)/Period
Formula_DAX: COUNTROWS(Filter(FactInventoryEvents,EventTypeID=Reorder))
Data_Sources: FactInventoryEvents.EventTypeID
Dimensions: Date, Supplier, Product
Visual: Line
‑‑‑>
### KPI‑009 – Re‑order Frequency

Too frequent reorders signal poor EOQ settings.

---

<!--‑‑‑
KPI_ID: KPI‑010
Name: Shrinkage %
Domain: Operations
Owner: Governor
Refresh: Monthly
Definition: Percentage of inventory lost or damaged.
Formula_SQL: DamagedQty/ReceivedQty
Formula_DAX: DIVIDE([Damaged Qty],[Received Qty])
Data_Sources: FactInventoryEvents.Qty
Dimensions: Date, Store, Supplier
Visual: Area chart
‑‑‑>
### KPI‑010 – Shrinkage %

Tracks loss through damage, theft, or admin error.

---

<!--‑‑‑
KPI_ID: KPI‑011
Name: Delivery Lead‑Time
Domain: Operations
Owner: Governor
Refresh: Monthly
Definition: Average days from reorder to delivery.
Formula_SQL: AVG(DeliveryDate – ReorderDate)
Formula_DAX: AVERAGE(FactInventoryEvents[LeadTimeDays])
Data_Sources: FactInventoryEvents
Dimensions: Supplier
Visual: Scatter
‑‑‑>
### KPI‑011 – Delivery Lead‑Time

Monitors supplier performance and logistics efficiency.

---

<!--‑‑‑
KPI_ID: KPI‑012
Name: Stock‑out Rate
Domain: Operations
Owner: Governor
Refresh: Monthly
Definition: Rate at which stock‑outs occur.
Formula_SQL: Days ClosingQty=0 / Total Days
Formula_DAX: DIVIDE([Days Out Of Stock],[Total Days])
Data_Sources: FactInventorySnapshot.ClosingQty
Dimensions: Product, Store
Visual: Heatmap
‑‑‑>
### KPI‑012 – Stock‑out Rate

Highlights availability gaps that affect sales directly.

---

<!--‑‑‑
KPI_ID: KPI‑013
Name: GMROI
Domain: Operations
Owner: Governor
Refresh: Monthly
Definition: Gross Margin Return on Inventory Investment.
Formula_SQL: GrossMargin / AvgInventoryCost
Formula_DAX: DIVIDE([Gross Margin],[Avg Inventory Cost])
Data_Sources: FactOrderItems, FactInventorySnapshot
Dimensions: Product Category
Visual: Column
‑‑‑>
### KPI‑013 – GMROI

Measures inventory productivity; >1.5 is often benchmark.

---

<!--‑‑‑
KPI_ID: KPI‑014
Name: Inventory Age > 90 days %
Domain: Operations
Owner: Governor
Refresh: Monthly
Definition: Percentage of inventory unsold for over 90 days.
Formula_SQL: Qty>90 / TotalQty
Formula_DAX: DIVIDE([Qty >90],[Total Qty])
Data_Sources: FactInventorySnapshot
Dimensions: Product, Store
Visual: Stacked bar
‑‑‑>
### KPI‑014 – Inventory Age > 90 days %

Helps reduce capital locked in slow‑moving items.

---

<!--‑‑‑
KPI_ID: KPI‑015
Name: Supplier Fill‑Rate %
Domain: Operations
Owner: Governor
Refresh: Monthly
Definition: Supplier fulfillment performance.
Formula_SQL: QtyDelivered/QtyOrdered
Formula_DAX: DIVIDE([Qty Delivered],[Qty Ordered])
Data_Sources: FactInventoryEvents
Dimensions: Supplier
Visual: Line
‑‑‑>
### KPI‑015 – Supplier Fill‑Rate %

Tracks how reliably suppliers meet order quantities.

---

<!--‑‑‑
KPI_ID: KPI‑016
Name: Weeks of Supply (WOS)
Domain: Operations
Owner: Governor
Refresh: Weekly
Definition: Forecast of weeks current inventory will last.
Formula_SQL: ClosingQty / AvgWeeklySales
Formula_DAX: DIVIDE([Closing Qty],[Avg Weekly Sales Qty])
Data_Sources: FactInventorySnapshot, FactOrderItems
Dimensions: Product, Store
Visual: Gauge
‑‑‑>
### KPI‑016 – Weeks of Supply (WOS)

Forecasts stock runway; <3 weeks triggers reorder review.

---

<!--‑‑‑
KPI_ID: KPI‑017
Name: Lead‑to‑Customer %
Domain: CRM
Owner: Governor
Refresh: Monthly
Definition: Conversion rate from leads to customers.
Formula_SQL: COUNT(NewCust)/COUNT(Leads)
Formula_DAX: DIVIDE([New Customers],[Total Leads])
Data_Sources: DimCustomer
Dimensions: Campaign, Region
Visual: Funnel
‑‑‑>
### KPI‑017 – Lead‑to‑Customer %

Measures marketing conversion efficiency.

---

<!--‑‑‑
KPI_ID: KPI‑018
Name: High‑Value Share
Domain: CRM
Owner: Governor
Refresh: Monthly
Definition: Share of customers classified as high‑value.
Formula_SQL: COUNT(HighValue)/COUNT(AllCust)
Formula_DAX: DIVIDE([HighValue Cust],[Total Cust])
Data_Sources: DimCustomer.HighValue
Dimensions: Segment, Region
Visual: Donut
‑‑‑>
### KPI‑018 – High‑Value Share

Indicates quality of customer base and loyalty.

---

<!--‑‑‑
KPI_ID: KPI‑019
Name: Interactions per Customer
Domain: CRM
Owner: Governor
Refresh: Monthly
Definition: Average interactions per customer.
Formula_SQL: COUNT(Interactions)/DISTINCTCOUNT(CustomerID)
Formula_DAX: [Total Interactions] / DISTINCTCOUNT(FactCustomerInteractions[CustomerID])
Data_Sources: FactCustomerInteractions
Dimensions: InteractionType
Visual: Column with trend
‑‑‑>
### KPI‑019 – Interactions per Customer

CRM engagement depth metric; supports churn analysis.

---

<!--‑‑‑
KPI_ID: KPI‑020
Name: Churn Rate
Domain: CRM
Owner: Governor
Refresh: Monthly
Definition: Rate at which customers become inactive or churn.
Formula_SQL: COUNT(AtRisk)/COUNT(TotalCust)
Formula_DAX: DIVIDE([At Risk Cust],[Total Cust])
Data_Sources: DimCustomer.AtRisk
Dimensions: Segment
Visual: Line
‑‑‑>
### KPI‑020 – Churn Rate

Signals retention health; rising trend = immediate action.

---

<!--‑‑‑
KPI_ID: KPI‑021
Name: Customer Lifetime Value
Domain: CRM
Owner: Governor
Refresh: Monthly
Definition: Avg total revenue per customer over their lifetime.
Formula_SQL: ΣRevenue per Customer
Formula_DAX: CALCULATE([Revenue],ALLEXCEPT(DimCustomer,DimCustomer[CustomerID]))
Data_Sources: FactOrderItems, DimCustomer
Dimensions: Customer Segment
Visual: Scatter high‑value
‑‑‑>
### KPI‑021 – Customer Lifetime Value

Combines revenue history to evaluate acquisition spend threshold.

---

<!--‑‑‑
KPI_ID: KPI‑022
Name: Customer Acquisition Cost
Domain: CRM
Owner: Governor
Refresh: Monthly
Definition: Campaign spend per new customer acquired.
Formula_SQL: ΣSpend/ΣNewCust
Formula_DAX: DIVIDE([Campaign Spend],[New Cust])
Data_Sources: FactCampaignSpend, DimCustomer
Dimensions: Campaign
Visual: KPI card
‑‑‑>
### KPI‑022 – Customer Acquisition Cost (CAC)

Used by marketing to monitor efficiency of ad spend.

---

<!--‑‑‑
KPI_ID: KPI‑023
Name: Sales per Sq Ft
Domain: Cross‑Domain
Owner: Governor
Refresh: Monthly
Definition: Revenue / Store Square Footage.
Formula_SQL: Revenue/StoreSqFt
Formula_DAX: DIVIDE([Revenue],[Store SqFt])
Data_Sources: FactOrderItems, DimStore
Dimensions: Store
Visual: Column
‑‑‑>
### KPI‑023 – Sales per Sq Ft

Key retail productivity measure for property decisions.

---

<!--‑‑‑
KPI_ID: KPI‑024
Name: Sell‑Through Rate
Domain: Cross‑Domain
Owner: Governor
Refresh: Monthly
Definition: Units Sold / (Units Sold + Ending Inventory).
Formula_SQL: UnitsSold/(UnitsSold+EndingInv)
Formula_DAX: DIVIDE([Units Sold],[Units Sold]+[Ending Inv])
Data_Sources: FactOrderItems, FactInventorySnapshot
Dimensions: Product Category
Visual: Area
‑‑‑>
### KPI‑024 – Sell‑Through Rate

Shows velocity of product movement; high rate reduces holding cost.

---

<!--‑‑‑
KPI_ID: KPI‑025
Name: Campaign ROI
Domain: Cross‑Domain
Owner: Governor
Refresh: Monthly
Definition: (Promo Revenue – Promo Cost) / Promo Cost.
Formula_SQL: (PromoRev-PromoCost)/PromoCost
Formula_DAX: DIVIDE([Promo Revenue] – [Promo Cost],[Promo Cost])
Data_Sources: FactCampaignSpend, FactOrderItems
Dimensions: Campaign
Visual: Bar by campaign
‑‑‑>
### KPI‑025 – Campaign ROI

Core marketing effectiveness metric.

---

<!--‑‑‑
KPI_ID: KPI‑026
Name: Store Conversion Rate %
Domain: Cross‑Domain
Owner: Governor
Refresh: Daily
Definition: Store transactions / store visits.
Formula_SQL: Transactions/Visits
Formula_DAX: DIVIDE([Transactions],[Visits])
Data_Sources: FactOrderHeader, FactFootTraffic
Dimensions: Store
Visual: KPI card
‑‑‑>
### KPI‑026 – Store Conversion Rate %

Indicates how effectively foot traffic converts to sales.

---

<!--‑‑‑
KPI_ID: KPI‑027
Name: Promo Redemption Rate %
Domain: Cross‑Domain
Owner: Governor
Refresh: Weekly
Definition: % of transactions using a promo.
Formula_SQL: PromoTx/TotalTx
Formula_DAX: DIVIDE([Promo Tx],[Total Tx])
Data_Sources: FactOrderItemPromotion, FactOrderHeader
Dimensions: Promotion, Store
Visual: Donut
‑‑‑>
### KPI‑027 – Promo Redemption Rate %

Shows adoption of discount codes; too high may erode margin.

---

<!--‑‑‑
KPI_ID: KPI‑028
Name: Incremental Lift %
Domain: Cross‑Domain
Owner: Governor
Refresh: Weekly
Definition: Incremental sales driven by promotions.
Formula_SQL: (PromoUnits – BaselineUnits)/BaselineUnits
Formula_DAX: DIVIDE([Promo Units] – [Baseline Units],[Baseline Units])
Data_Sources: FactOrderItemPromotion, FactOrderItems
Dimensions: Promotion, Product
Visual: Line
‑‑‑>
### KPI‑028 – Incremental Lift %

Validates effectiveness of promo beyond cannibalisation.

---


<!--‑‑‑
KPI_ID: KPI‑029
Name: Return Value %
Domain: Sales
Owner: Governor
Refresh: Monthly
Definition: Proportion of revenue refunded through product returns.
Formula_SQL: SUM(FOR.ReturnAmount) / SUM(FOI.LineTotal)
Formula_DAX: DIVIDE([Return Revenue],[Revenue])
Data_Sources:
  - FactOrderReturns.ReturnAmount
  - FactOrderItems.LineTotal
Dimensions: Date, Store, Product, Customer, ReturnReason
Visual: Card + trend sparkline, drill‑through to Return Reason
‑‑‑>
### KPI‑029 – Return Value %

Returned dollars erode top‑line growth more than unit‑based return percent alone.  
Tracking this KPI highlights categories or stores where refunds bite hardest and signals process or quality issues early.

---

<!--‑‑‑
KPI_ID: KPI‑030
Name: Promo Lift $
Domain: Sales
Owner: Governor
Refresh: Weekly
Definition: Absolute revenue generated by a promotion above baseline.
Formula_SQL: SUM(FOP.PromoRevenue) – SUM(FOI.BaselineRevenue)
Formula_DAX: [Promo Revenue] – [Baseline Revenue]
Data_Sources:
  - FactOrderItemPromotion.PromoRevenue
  - FactOrderItems.LineTotal AS BaselineRevenue
Dimensions: Date, Store, Product, Promotion
Visual: Clustered bar by promo with baseline overlay
‑‑‑>
### KPI‑030 – Promo Lift ($)

Shows whether a promotion drives meaningful incremental revenue or merely shifts timing.  
Use alongside *Promo Uplift %* for a balanced view of efficiency.

---

<!--‑‑‑
KPI_ID: KPI‑031
Name: Cost per Lead
Domain: Marketing
Owner: Governor
Refresh: Monthly
Definition: Average campaign spend required to acquire one lead.
Formula_SQL: SUM(FCS.SpendAmount) / COUNT(DC.LeadID)
Formula_DAX: DIVIDE([Campaign Spend],[New Leads])
Data_Sources:
  - FactCampaignSpend.SpendAmount
  - DimCustomer.IsNewLead = 1
Dimensions: Date, Campaign, Channel
Visual: KPI card with goal threshold
‑‑‑>
### KPI‑031 – Cost per Lead

Provides a hard dollar benchmark for marketing efficiency.  
Compare against *Customer Acquisition Cost* and *Campaign ROI* to optimise budget allocation.

---

<!--‑‑‑
KPI_ID: KPI‑032
Name: Average Days in Status
Domain: Operations
Owner: Governor
Refresh: Weekly
Definition: Mean number of days orders spend in their current status.
Formula_SQL: AVG(FOS.DaysInStatus)
Formula_DAX: AVERAGE(FactOrderStatus[DaysInStatus])
Data_Sources:
  - FactOrderStatus.DaysInStatus
Dimensions: Date, Status, Store
Visual: Heatmap by status vs store
‑‑‑>
### KPI‑032 – Average Days in Status

Highlights bottlenecks in the fulfilment pipeline (e.g., “Pending Pick”, “Awaiting Payment”).  
Ops teams target outliers to reduce cycle time and improve customer experience.

---

## Change‑log

| Version | Date | Notes |
|---------|------|-------|
| **v3.0** | 2025‑07‑23 | Added KPI‑029 (Return Value %), KPI‑030 (Promo Lift $), KPI‑031 (Cost per Lead), KPI‑032 (Avg Days in Status). |


## Change‑log

| Version | Date | Notes |
|---------|------|-------|
| **v2.0** | 2025‑07‑23 | Initial 28 KPI cards covering Sales, Operations, CRM & Cross‑Domain metrics. |
| **v2.0** | 2025‑07‑?23 | Initial 28 KPI cards covering Sales, Operations, CRM & Cross‑Domain metrics. |
