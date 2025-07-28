# Data Design · **v1.0**

*Build‑phase umbrella document linking physical schema (Data‑Spec v3.3.1) and narrative model (Retail Data Model v2.1).*  
*Created 2025‑07‑24*

---

## 1 | Modelling Principles  *(Build DW)*

| Topic | Convention | Source |
|-------|------------|--------|
| **Surrogate keys** | INT IDENTITY, named `<Table>SK`, never reused; natural keys kept for trace. | Data‑Spec v3.3.1 🔗 |
| **Audit columns** | `LoadDate DATETIME2(3)` default `SYSUTCDATETIME()`, `SourceSystem NVARCHAR(50)` default `'UNKNOWN'`, `RecordHash BINARY(32)`; all `NOT NULL`:contentReference[oaicite:0]{index=0} | ETL Audit v2.1 |
| **Naming** | `Dim*`, `Fact*`, `stg.*` (staging), `etl.*` (metadata); PK `pk_<table>`, FK `fk_<child>_<parent>`. | internal standard |
| **Hash‑diff** | SHA2‑256 on natural key + business attrs, exclude PII; used by incremental loaders. | ETL Audit v2.1 |
| **Snapshot vs SCD vs Transaction** | Decision matrix in §3. | Snapshot v2.1:contentReference[oaicite:1]{index=1} / SCD v2.1:contentReference[oaicite:2]{index=2} |

---

## 2 | Source → Target Mapping  *(Integration Design)*

| Source System | Domain | Transport & Cadence | Landing / Staging | Core DW Table | Grain |
|---------------|--------|---------------------|-------------------|---------------|-------|
| **POS CSV**   | Sales  | SFTP nightly @ 01:00 | `stg.SalesPos`    | `FactOrderItems` | *Order line* |
| **OMS API**   | Orders | JSON every 30 min    | `stg.OrdersOms`   | `FactOrderStatus` | *Order × Day (snapshot)* |
| **WMS CSV**   | Inventory | SFTP hourly       | `stg.WmsOnHand`   | `FactInventorySnapshot` | *Product × Store × Day* |
| **Marketing API** | Campaign | JSON daily   | `stg.MktSpend`    | `FactCampaignSpend` | *Campaign × Day* |
| *(extend as sources on‑board)* | | | | | |

---

## 3 | Table‑Type Decision Matrix

| Use case | Table type | Rationale | Reference |
|----------|------------|-----------|-----------|
| Daily stock position | **Snapshot Fact** (`FactInventorySnapshot`) | Captures point‑in‑time balance without replaying transactions. | Snapshot Strategy v2.1 |
| Order pipeline ageing | Snapshot fact (`FactOrderStatus`) | Trend analysis of status duration. | id. |
| Product cost changes | **SCD Type‑2 Dim** (`DimProduct`) | Preserve historical cost for margin restatements. | SCD Strategy v2.1 |
| Pure transactional events (sales) | **Fact** (`FactOrderItems`) | High‑volume inserts, no updates. | Data‑Spec |

---

## 4 | Index & Partition Policy  *(Ops)*

- **Facts**  
  - Clustered index on surrogate PK.  
  - Monthly partition on `DateID` from 2022‑01 onward; hot partition current month.  
  - Key non‑clustered index:  
    `IX_FactSales_FK (DateID, StoreID)` for daily dashboard slicers.  
- **Dimensions**  
  - Clustered on surrogate PK; non‑clustered on natural business key.  
  - `IsCurrent = 1` filtered index for SCD Type‑2 dims to speed point‑in‑time joins.  
- **Snapshot facts**  
  - Partition switch retention: keep 3 years hot, older partitions archived to cheaper tier.

---

## 5 | Governance Hooks  *(Governance)*

| Area | Implementation |
|------|----------------|
| **Lineage** | Audit trio + BatchLog + Watermark tables (ETL_Audit v2.1) |
| **Data quality** | DQ dashboard will surface % hash mismatches, stale watermark. |
| **Security / PII** | PII not included in RecordHash; masking policy in Vision doc. |
| **CI checks** | `check_kpi_trace.py`, FK diff script (planned in CI/CD pipeline). |

---

## Change‑log

| Version | Date | Notes |
|---------|------|-------|
| **v1.0** | 2025‑07‑24 | Initial creation: modelling principles, source‑target map, decision matrix, index policy, governance links. |
