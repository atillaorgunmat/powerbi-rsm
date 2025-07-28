# Slowly‑Changing Dimension Strategy · **v2.1**

*Aligned with Data‑Spec v3.3.1 · 2025‑07‑23*

---

## 1 | Type‑2 Dimensions in Scope

| Dimension | Business Reason for History | Surrogate Key | Type‑2 Columns |
|-----------|----------------------------|---------------|----------------|
| **DimCustomer** | Loyalty tier, lifecycle | CustomerSK | Tier, Segment, AtRiskFlag |
| **DimProduct** | Cost price, category | ProductSK | UnitCost, SubCategory |
| **DimStore** | Floor space, region | StoreSK | SquareFootage, Region |

Each row carries **EffectiveFrom, EffectiveTo, IsCurrent** flags and the audit trio *LoadDate / SourceSystem / RecordHash*.

---

## 2 | Generic Type‑2 MERGE Template

```sql
CREATE OR ALTER PROCEDURE dbo.sp_SCD2_Merge
  @DimName sysname,               -- e.g., 'DimProduct'
  @BusinessKeyCols nvarchar(max), -- e.g., 'ProductID'
  @HashCols       nvarchar(max)   -- e.g., 'ProductName,UnitCost'
AS
/* 1. Source staging view expected: stg.<DimName> */
DECLARE @sql nvarchar(max) = N'
;WITH src AS (
  SELECT *, HASHBYTES(''SHA2_256'', CONCAT_WS(''|'',' + @HashCols + ')) AS SourceHash
  FROM   stg.' + @DimName + '
),
tgt AS (
  SELECT *, HASHBYTES(''SHA2_256'', CONCAT_WS(''|'',' + @HashCols + ')) AS TargetHash
  FROM   dbo.' + @DimName + '
  WHERE  IsCurrent = 1
)
MERGE tgt
USING src
ON   ' + @BusinessKeyCols + '
WHEN MATCHED AND tgt.TargetHash <> src.SourceHash THEN
  UPDATE SET IsCurrent    = 0,
             EffectiveTo  = SYSUTCDATETIME()
WHEN NOT MATCHED THEN
  INSERT (' + @BusinessKeyCols + ',EffectiveFrom,IsCurrent,' + @HashCols + ',LoadDate,SourceSystem,RecordHash)
  VALUES (src.' + REPLACE(@BusinessKeyCols, '=', '') + ',SYSUTCDATETIME(),1,' + @HashCols + ',
          SYSUTCDATETIME(),''POS'',src.SourceHash);';
EXEC (@sql);

Call pattern:

EXEC dbo.sp_SCD2_Merge
     @DimName        = 'DimProduct',
     @BusinessKeyCols= 'ProductID',
     @HashCols       = 'ProductName,UnitCost,SubCategory';

---

3 | Querying History in Power BI

IsLatestVersion =
VAR maxEff = CALCULATE(MAX(DimProduct[EffectiveFrom]),
                       ALLEXCEPT(DimProduct,DimProduct[ProductID]))
RETURN IF(DimProduct[EffectiveFrom] = maxEff, 1, 0)

Add IsLatestVersion = 1 filter to “current view” measures; drop the filter to show historic context.

---

4 | Linkage to Incremental‑Load Engine
The MERGE template relies on RecordHash produced by the incremental‑load engine (T‑0032).
Audit columns (LoadDate, SourceSystem) are auto‑filled for lineage compliance (see ETL_Audit_Columns_Strategy v2.1).

---

5 | Change‑log

| Version  | Date       | Notes                                                                                                                      |
| -------- | ---------- | -------------------------------------------------------------------------------------------------------------------------- |
| **v2.1** | 2025‑07‑23 | Added DimProduct & DimStore to Type‑2 list; introduced generic MERGE proc with hash diff; added DAX “current row” pattern. |
| v1.0     | 2025‑05‑?? | Baseline strategy for DimCustomer only.                                                                                    |
