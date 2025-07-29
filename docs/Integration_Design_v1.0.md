# Integration Design · **v1.0**

*End‑to‑end pipeline architecture, source inventory, data‑flow and governance checkpoints.*  
*Created 2025‑07‑24*

---

## 1 | Source Inventory  *(Build DW)*

| Source | Domain | Data Owner | Format | Transport | Cadence | Landing Path | SLA (Lag) |
|--------|--------|------------|--------|-----------|---------|--------------|-----------|
| **POS** | Sales Tx | Retail Ops | CSV | SFTP | Nightly 01:00 | `/landing/pos/YYYYMMDD/` | ≤ 2 h |
| **OMS** | Orders | e‑Com IT | JSON API | HTTPS | 30 min | `/landing/oms/` | ≤ 30 min |
| **WMS** | Inventory | Supply Chain | CSV | SFTP | Hourly | `/landing/wms/` | ≤ 1 h |
| **Marketing Cloud** | Campaign Spend | Mktg | JSON | REST pull | Daily 05:00 | `/landing/mkt/` | ≤ 3 h |
| *(extend as new feeds onboard)* | | | | | | | |

---

## 2 | Landing & Staging Conventions  *(Build DW)*

- **Folder pattern** `/landing/<source>/<YYYYMMDD>/file_*.csv`  
  - Retain raw files **30 days**, then archive to Azure Blob *cool* tier.  
- **External tables** `ext.<source>_<entity>` (PolyBase / OPENROWSET).  
- **Staging views** `stg.<Entity>` flatten external data and standardise column names.  
- **File validation:** schema hash, record count, mandatory column check before staging load.

---

## 3 | Data‑Flow Diagram  *(Monitor / Ops)*

![integration_flow_v1](integration_flow_v1.png)  

> *Swim‑lanes: Source → Landing → Staging → Incremental Load (Procs) → DW Star → Power BI.*  
> Create in draw.io → export PNG (≈ 1000 px wide) and save alongside this doc.

---

## 4 | Data‑Quality Checkpoints  *(Monitor)*

| Checkpoint | Table / Process | Threshold | Alert Channel |
|------------|-----------------|-----------|---------------|
| **Watermark Lag** | `etl.Watermark` | `NOW() – LastSeen > 2h` | PBI DQ dashboard & Teams |
| **Hash Mismatch %** | Dim loaders | > 0.5 % changed rows | Ops email |
| **Schema Drift** | External table vs expected | Any diff | CI pipeline fail |
| **Batch Failure Count** | `etl.BatchLog.Status = 'Failed'` | ≥ 1 | PagerDuty |

---

## 5 | SLAs & Recovery  *(Ops)*

| Pipeline | SLA Lag | RPO | RTO | Retry Policy |
|----------|---------|-----|-----|--------------|
| POS Sales | 2 h | 30 min | 2 h | 3× exponential back‑off |
| OMS Orders | 30 min | 15 min | 1 h | API re‑pull + dead‑letter |
| WMS Snapshot | 1 h | 30 min | 2 h | Re‑ingest latest file |
| Marketing Spend | 3 h | 1 h | 4 h | Daily re‑try |

---

## 6 | Security & PII Handling  *(Governance)*

- **Transport security** – GPG‑encrypted SFTP or HTTPS/TLS 1.2+.  
- **Landing zone encryption** – Azure Storage Server‑Side Encryption (SSE).  
- **Hash‑diff policy** – PII columns (Name, Email, Phone) are **excluded** from `RecordHash`.  
- **Key rotation** – Quarterly; managed via Azure Key Vault.

---

## 7 | Cross‑References

| Design Artefact | Link |
|-----------------|------|
| Data Design v1.0 | schema / modelling principles |
| ETL & Audit Strategy v2.1 | watermark & batch logging implementation |
| SCD Strategy v2.1 | `sp_SCD2_Merge` loader |
| Snapshot Strategy v2.1 | snapshot driver SP |

---

## Change‑log

| Version | Date | Notes |
|---------|------|-------|
| **v1.0** | 2025‑07‑24 | Initial creation: source inventory, landing rules, flow diagram placeholder, DQ checkpoints, SLAs, security policy. |
