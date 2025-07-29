# Retail Data Model · **v2.1**  
*(aligned with Data‑Spec v3.3.1 – 2025‑07‑23)*  

## 1 | Star‑Schema Overview  

The model is a **constellation** of star schemas sharing conformed dimensions:

| Domain        | Fact Tables                                          | Primary Purpose |
|---------------|------------------------------------------------------|-----------------|
| **Sales**     | `FactOrderHeader`, `FactOrderItems`, `FactSales`, `FactOrderItemPromotion` | Revenue, promo uplift, basket analysis |
| **Returns**   | `FactOrderReturns`                                   | Return %, root‑cause |
| **Operations**| `FactInventoryEvents`, `FactInventorySnapshot`, `FactCostOfGoods` | Stock health, COGS, GMROI |
| **Order Flow**| `FactOrderStatus` (snapshot)                         | Pipeline ageing / SLA |
| **CRM**       | `FactCustomerInteractions`, `FactLeadLifecycle` (opt.) | Engagement & conversion |
| **Marketing** | `FactCampaignSpend`, `FactFootTraffic`               | Campaign ROI, store conversion |

All facts link to shared dimensions (`DimDate`, `DimStore`, `DimProduct`, `DimCustomer`, `DimSalesRep`, `DimPromotion`, etc.) so cross‑domain KPIs (e.g., *Sales per Sq Ft*, *Campaign ROI*) can be computed in a single filter context:contentReference[oaicite:0]{index=0}.  

---

## 2 | New Objects in v2.1  

### 2.1 Snapshot Facts (blue)  
*Provide point‑in‑time metrics independent of running balances*:contentReference[oaicite:1]{index=1}  

| Table | Grain | Refresh | Key KPI Driver |
|-------|-------|---------|----------------|
| **FactInventorySnapshot** | Product × Store × Day | Nightly append | Stock on Hand, WOS, Inventory Age |
| **FactOrderStatus** | Order × Day | Daily upsert | Open‑order pipeline, Days‑in‑Status |

### 2.2 Type‑2 Dimensions (purple)  
Managed per SCD strategy v1.0:contentReference[oaicite:2]{index=2}  

- **DimProduct** (`UnitCost`)  
- **DimStore** (`SquareFootage`)  

Historic attributes allow back‑dated KPIs such as *Gross Margin %* and *Sales per Sq Ft*.  

### 2.3 Campaign & Foot‑Traffic Integration  
`DimCampaign` + `FactCampaignSpend` join with `FactFootTraffic` to calculate *Campaign ROI* and *Store Conversion Rate %*:contentReference[oaicite:3]{index=3}.  

---

## 3 | Entity‑Relationship Diagram  

![ERD_v2.1](ERD_v2.1.png)  

Legend  
- **Blue** = snapshot fact  **Purple** = Type‑2 dimension  Gray lines = FKs  

> *Diagram generated from `Retail_Data_Model_v2.1.dbml`; validated against SpecShell FK list — no orphan tables.*  

---

## 4 | Audit & ETL Metadata  

Every table carries standard columns (`LoadDate`, `SourceSystem`, `RecordHash`) enabling hash‑diff incremental loads and lineage checks:contentReference[oaicite:4]{index=4}.  

---

## 5 | Performance & Indexing  

| Object | Index / Strategy | Rationale |
|--------|------------------|-----------|
| `FactSales` | `IX_FactSales_FK (DateID, StoreID)` | Accelerates daily sales slicers & YoY comps. |
| Type‑2 dims | Clustered on surrogate key (SK) | Retains temporal order for partition elimination. |
| Snapshots | Partition by `SnapshotDateID` | Fast prune for recent‑period dashboards. |

---

## 6 | Usage Patterns & Example Queries  

| Persona | Question | Tables Touched | Sample DAX / SQL Snippet |
|---------|----------|----------------|--------------------------|
| Sales Mgr | Promo uplift last 7 days | FactOrderItemPromotion, FactOrderItems | `Promo Uplift % = DIVIDE([PromoRev]-[BaseRev],[BaseRev])` |
| Ops Lead | Top stores by Stock‑out Rate | FactInventorySnapshot, DimStore | `COUNTROWS(FILTER(Snapshot, ClosingQty=0)) / COUNTROWS(Snapshot)` |
| Exec | Sales vs COGS trend | FactSales, FactCostOfGoods | `Margin % = 1 - DIVIDE([COGS],[Revenue])` |

---

## 7 | Change‑Log  

| Version | Date | Notes |
|---------|------|-------|
| **v2.1** | 2025‑07‑23 | Added snapshot facts, campaign/foot‑traffic tables, SCD dims; updated audit metadata & ERD. |
| v1.0 | 2025‑05‑?? | Initial narrative for core sales/ops/CRM model. |

