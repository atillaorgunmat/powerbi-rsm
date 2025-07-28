# Snapshot Fact Strategy · **v2.1**

*Aligned with Data‑Spec v3.3.1 · 2025‑07‑23*

---

## 1 | Why Snapshot Facts?

Operational tables hold only the current state; analytics often require **point‑in‑time** views (inventory balance, order pipeline).  
Snapshot facts store these states as **daily (D1) partitions**, enabling trend KPIs without expensive reconstruction.

---

## 2 | Snapshot Fact Catalogue (2025‑07‑23)

| Fact Table | Grain | Driver Calendar | Refresh Window | Primary KPIs |
|------------|-------|-----------------|----------------|--------------|
| **FactInventorySnapshot** | *Product × Store × Day* | `DimDate.IsBusinessDay = 1` | *Insert‑only* | Stock on Hand, WOS, Stock‑out Rate |
| **FactOrderStatus** | *Order × Day* | `DimDate` (all) | *Upsert* (`OrderID`) | Avg Days in Status, Stuck Orders |
| *(Future)* FactEmployeeHeadcount | *Employee × Month* | Fiscal calendar | Insert‑only | HR trend KPIs |

---

## 3 | Driver SP Pattern

```sql
CREATE OR ALTER PROCEDURE dbo.sp_Load_SnapshotFact
  @SnapshotDate date
AS
BEGIN
   SET XACT_ABORT, NOCOUNT ON;

   -- 1. Inventory Snapshot (insert‑only)
   INSERT INTO dbo.FactInventorySnapshot (...)
   SELECT  @SnapshotDate  AS SnapshotDateID,
           p.ProductID,
           s.StoreID,
           onhand.QtyOnHand,
           SYSUTCDATETIME() AS LoadDate,
           'POS'            AS SourceSystem,
           HASHBYTES('SHA2_256', CONCAT_WS('|',p.ProductID,s.StoreID,@SnapshotDate,onhand.QtyOnHand)) AS RecordHash
   FROM   src.OnHand onhand
   JOIN   dbo.DimProduct p ON p.Sku = onhand.Sku
   JOIN   dbo.DimStore   s ON s.StoreCode = onhand.Store;

   -- 2. Order Status (upsert)
   MERGE dbo.FactOrderStatus tgt
   USING (
        SELECT o.OrderID,
               @SnapshotDate AS SnapshotDateID,
               DATEDIFF(day,o.CreatedDate,@SnapshotDate) AS DaysInStatus
        FROM   src.Orders o
   ) AS src
   ON  tgt.OrderID = src.OrderID AND tgt.SnapshotDateID = src.SnapshotDateID
   WHEN MATCHED THEN UPDATE SET DaysInStatus = src.DaysInStatus,
                                 RecordHash    = HASHBYTES('SHA2_256',CONCAT_WS('|',src.*)),
                                 LoadDate      = SYSUTCDATETIME()
   WHEN NOT MATCHED THEN
        INSERT (SnapshotDateID,OrderID,DaysInStatus,LoadDate,SourceSystem,RecordHash)
        VALUES (src.SnapshotDateID,src.OrderID,src.DaysInStatus,SYSUTCDATETIME(),'OMS',
                HASHBYTES('SHA2_256',CONCAT_WS('|',src.*)));
END
GO

Note: Both snapshot facts carry the standard audit columns LoadDate, SourceSystem, RecordHash.

---

4 | Incremental Refresh & Retention (Power BI)

{
  "policy": {
    "mode": "incremental",
    "filter": "SnapshotDateID",
    "rangeStart": "NOW() - 3 YEARS",
    "rangeEnd": "NOW() + 1 DAY",
    "detectDataChanges": true
  }
}

Partitioned tables refresh the current month daily; historical partitions are frozen.

---

5 | Change‑log

| Version  | Date       | Notes                                                                                                |
| -------- | ---------- | ---------------------------------------------------------------------------------------------------- |
| **v2.1** | 2025‑07‑23 | Added FactOrderStatus, driver SP template, audit/hash columns, and PBI incremental‑refresh guidance. |
| v1.0     | 2025‑05‑?? | Initial snapshot concept for inventory only.                                                         |

---
