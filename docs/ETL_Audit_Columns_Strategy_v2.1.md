# ETL & Audit Column Strategy · **v2.1**

*Aligned with Incremental Engine (T‑0032) & Data‑Spec v3.3.1*  
*2025‑07‑23*

---

## 1 | Standard Audit Columns

| Column | Data Type | Constraint | Default | Purpose |
|--------|-----------|------------|---------|---------|
| **LoadDate** | `DATETIME2(3)` | `NOT NULL` | `SYSUTCDATETIME()` | ETL ingest timestamp |
| **SourceSystem** | `NVARCHAR(50)` | `NOT NULL` | `'UNKNOWN'` | Upstream system id |
| **RecordHash** | `BINARY(32)` | `NOT NULL` | *(computed by loader)* | SHA‑256 of business cols for change detection |

> *Hash length 32 bytes ~ 64 hex chars; stored as binary for size efficiency.*

---

## 2 | Hash‑Diff Methodology

1. **`CONCAT_WS('|', colA,…,colN)`** concatenates natural key + business attributes.  
2. `HASHBYTES('SHA2_256', expr)` produces a 256‑bit checksum.  
3. Loader compares **source hash ≠ target hash** to trigger an update (dims) or upsert (facts).  
4. **Never include PII** (e.g., Name, Email) inside the hash to avoid accidental exposure via checksum attacks.

---

## 3 | Watermark & Batch Log

### 3.1 Watermark Table

```sql
CREATE TABLE etl.Watermark (
    TableName      sysname PRIMARY KEY,
    LastSeen       DATETIME2(3)  NOT NULL,
    RowCount       BIGINT        NOT NULL,
    LastLoadStatus VARCHAR(20)   NOT NULL  -- Success | Failed
);

Incremental procs update RowCount & LastSeen; the nightly monitor flags gaps.

---

3.2 Batch Log

CREATE TABLE etl.BatchLog (
    BatchID        BIGINT IDENTITY PRIMARY KEY,
    JobName        VARCHAR(100),
    StartTime      DATETIME2(3),
    EndTime        DATETIME2(3),
    Status         VARCHAR(20),   -- Success / Failed / Partial
    RowsInserted   BIGINT,
    RowsUpdated    BIGINT,
    RowsDeleted    BIGINT,
    ErrorMessage   NVARCHAR(4000)
);

---

4 | Generic Loader Templates
Two reference procedures live under /sql/templates/:

usp_Load_Dim_Template.sql – wraps sp_SCD2_Merge for Type‑2 dims.

usp_Load_Fact_Template.sql – hash‑diff & soft‑delete pattern for facts.

(See template code blocks below – customise per table.)

---

5 | Soft Deletes & SCD Integration
Facts get an IsActive BIT flag; absence in source during a load marks IsActive = 0.
Dims call sp_SCD2_Merge (see SCD_Strategy v2.1) to produce new Type‑2 rows when hash changes.

---

6 | Security & Compliance
Do not hash PII columns (Name, Email, Phone).

Use column‑level encryption for any PII stored.

Audit & BatchLog tables contain no business data – they can be granted read access to Ops.

---

7 | Change‑log

| Version  | Date       | Notes                                                                                                                 |
| -------- | ---------- | --------------------------------------------------------------------------------------------------------------------- |
| **v2.1** | 2025‑07‑23 | Added watermark & batchlog schemas, generic load templates, hash‑diff algorithm, PII guidance, audit column defaults. |
| v1.0     | 2025‑05‑?? | Initial audit column definition.                                                                                      |

---

