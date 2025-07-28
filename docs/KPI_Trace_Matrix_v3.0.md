# Data ↔ KPI Trace Matrix · **v3.0**  
*(aligned with Data‑Spec v3.3.1 & KPI List v3.0 – 2025‑07‑23)*  

| KPI ID | KPI Name | Primary Fact Table(s) | Core Sliceable Dimensions¹ | Status |
|--------|----------|-----------------------|----------------------------|--------|
| KPI‑001 | Revenue | FactOrderItems | Date, Store, Product, Customer | mapped |
| KPI‑002 | Gross Margin % | FactOrderItems, FactOrderReturns | Date, Store, Product | mapped |
| KPI‑003 | Average Order Value | FactOrderItems, FactOrderHeader | Date, Store, Customer | mapped |
| KPI‑004 | Promo Uplift % | FactOrderItemPromotion, FactOrderItems | Date, Store, Product, Promotion | mapped |
| KPI‑005 | Return % | FactOrderReturns, FactOrderItems | Date, Store, Product, ReturnReason | mapped |
| KPI‑006 | Net Profit % | FactOrderItems, FactOrderReturns | Date, Store | mapped |
| KPI‑007 | Comp‑Store Sales % (YoY) | FactOrderItems | Date, Store | mapped |
| KPI‑008 | Stock on Hand | FactInventorySnapshot | Date, Store, Product | mapped |
| KPI‑009 | Re‑order Frequency | FactInventoryEvents | Date, Supplier, Product | mapped |
| KPI‑010 | Shrinkage % | FactInventoryEvents | Date, Store, Supplier | mapped |
| KPI‑011 | Delivery Lead‑Time | FactInventoryEvents | Supplier | mapped |
| KPI‑012 | Stock‑out Rate | FactInventorySnapshot | Date, Store, Product | mapped |
| KPI‑013 | GMROI | FactOrderItems, FactInventorySnapshot | ProductCategory | mapped |
| KPI‑014 | Inventory Age > 90 days % | FactInventorySnapshot | Date, Store, Product | mapped |
| KPI‑015 | Supplier Fill‑Rate % | FactInventoryEvents | Supplier | mapped |
| KPI‑016 | Weeks of Supply (WOS) | FactInventorySnapshot, FactOrderItems | Date, Store, Product | mapped |
| KPI‑017 | Lead‑to‑Customer % | DimCustomer (status fields) | Campaign, Region | mapped |
| KPI‑018 | High‑Value Share | DimCustomer | Segment, Region | mapped |
| KPI‑019 | Interactions per Customer | FactCustomerInteractions | InteractionType, Date | mapped |
| KPI‑020 | Churn Rate | DimCustomer | Segment | mapped |
| KPI‑021 | Customer Lifetime Value | FactOrderItems, DimCustomer | CustomerSegment | mapped |
| KPI‑022 | Customer Acquisition Cost | FactCampaignSpend, DimCustomer | Campaign | mapped |
| KPI‑023 | Sales per Sq Ft | FactOrderItems, DimStore | Date, Store | mapped |
| KPI‑024 | Sell‑Through Rate | FactOrderItems, FactInventorySnapshot | Date, ProductCategory | mapped |
| KPI‑025 | Campaign ROI | FactCampaignSpend, FactOrderItems | Campaign | mapped |
| KPI‑026 | Store Conversion Rate % | FactOrderHeader, FactFootTraffic | Date, Store | mapped |
| KPI‑027 | Promo Redemption Rate % | FactOrderItemPromotion, FactOrderHeader | Promotion, Store | mapped |
| KPI‑028 | Incremental Lift % | FactOrderItemPromotion, FactOrderItems | Promotion, Product | mapped |
| **KPI‑029** | Return Value % | FactOrderReturns, FactOrderItems | Date, Store, Product | mapped |
| **KPI‑030** | Promo Lift $ | FactOrderItemPromotion, FactOrderItems | Date, Store, Product, Promotion | mapped |
| **KPI‑031** | Cost per Lead | FactCampaignSpend, DimCustomer | Date, Campaign | mapped |
| **KPI‑032** | Avg Days in Status | FactOrderStatus | Date, Store, Status | mapped |

> **¹ Core sliceable dimensions** are the ones most commonly used in dashboards.  
> All tables also inherit the universal slicers *Date* and *Store* where applicable.

---

## Change‑log

| Version | Date | Notes |
|---------|------|-------|
| **v3.0** | 2025‑07‑23 | Added mappings for new KPIs 029‑032; ensured zero unmapped KPIs. |
