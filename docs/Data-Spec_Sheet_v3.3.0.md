Data-Spec Sheet v3.3
Explicitly aligned with SpecShell v3.3 DACPAC (2025-07-22)

1 · Dimension Tables (v3.3)
Existing Dimensions
DimDate (PK: DateID)

DimProduct (PK: ProductID, FK: SupplierID)

DimStore (PK: StoreID)

DimCustomer (PK: CustomerID, FK: AssignedRepID)

DimPromotion (PK: PromotionCode)

DimSalesRep (PK: SalesRepID, FK: StoreID)

New Dimensions (explicitly added v3.3)

| Dimension           | PK             | Audit Columns                      | Description / Example values             |
| ------------------- | -------------- | ---------------------------------- | ---------------------------------------- |
| **DimReturnReason** | ReturnReasonID | LoadDate, SourceSystem, RecordHash | Reasons like "Damaged", "Defective"      |
| **DimCampaign**     | CampaignID     | LoadDate, SourceSystem, RecordHash | Campaign details for promo effectiveness |

Static Lookups (explicitly included audit columns)
DimSupplier (PK: SupplierID)

DimPaymentType (PK: PaymentTypeID)

DimInteractionType (PK: InteractionTypeID)

DimEventType (PK: EventTypeID)

All dimensions explicitly contain:
LoadDate DATETIME2, SourceSystem NVARCHAR(50), RecordHash CHAR(64)

2 · Fact Tables (v3.3)

| Fact Table                   | Grain (Explicit)                   | Key FKs / Indexes (Explicit)                                          | Audit Columns                      |
| ---------------------------- | ---------------------------------- | --------------------------------------------------------------------- | ---------------------------------- |
| **FactOrderHeader**          | One row per order                  | DateID, CustomerID, StoreID, SalesRepID, PaymentTypeID, PromotionCode | LoadDate, SourceSystem, RecordHash |
| **FactOrderItems**           | One row per product line per order | OrderID, ProductID, DateID                                            | LoadDate, SourceSystem, RecordHash |
| **FactOrderReturns**         | One row per returned product line  | OrderID, ProductID, DateID, ReturnReasonID                            | LoadDate, SourceSystem, RecordHash |
| **FactInventoryEvents**      | One row per inventory event        | EventTypeID, ProductID, StoreID, SupplierID, DateID                   | LoadDate, SourceSystem, RecordHash |
| **FactCustomerInteractions** | One row per customer interaction   | CustomerID, SalesRepID, InteractionTypeID, DateID                     | LoadDate, SourceSystem, RecordHash |

Explicitly New Fact Tables

| New Fact Table                     | Grain (Explicit)                                 | Key FKs / Indexes (Explicit)                                 | Audit Columns                      |
| ---------------------------------- | ------------------------------------------------ | ------------------------------------------------------------ | ---------------------------------- |
| **FactSales**                      | Daily sales summary (Store × Date)               | DateID, StoreID<br>**IX\_FactSales\_FK** (`DateID, StoreID`) | LoadDate, SourceSystem, RecordHash |
| **FactInventorySnapshot**          | Inventory position (Product × Store × Date)      | SnapshotDateID, ProductID, StoreID                           | LoadDate, SourceSystem, RecordHash |
| **FactOrderStatus**                | Order status daily snapshot                      | SnapshotDateID, OrderID                                      | LoadDate, SourceSystem, RecordHash |
| **FactCostOfGoods**                | Daily COGS (Store × Product × Date)              | DateID, ProductID, StoreID                                   | LoadDate, SourceSystem, RecordHash |
| **FactCampaignSpend**              | Spend per campaign                               | CampaignID, DateID                                           | LoadDate, SourceSystem, RecordHash |
| **FactOrderItemPromotion**         | Promo usage by order item                        | OrderID, ProductID, PromotionCode                            | LoadDate, SourceSystem, RecordHash |
| **FactFootTraffic**                | Store visits per day                             | StoreID, DateID                                              | LoadDate, SourceSystem, RecordHash |
| **FactLeadLifecycle** *(Optional)* | Lead status lifecycle tracking (Customer × Date) | CustomerID, DateID                                           | LoadDate, SourceSystem, RecordHash |

3 · Audit Column Standards (Explicit v3.3)
Each table explicitly contains:

LoadDate DATETIME2 DEFAULT SYSUTCDATETIME()

SourceSystem NVARCHAR(50) DEFAULT 'UNKNOWN'

RecordHash CHAR(64) (Explicit hash of critical business attributes.)

4 · Index Definitions (Explicitly documented)
Explicit composite index (new v3.3):

CREATE INDEX IX_FactSales_FK ON dbo.FactSales (DateID, StoreID)

Surrogate PKs & FK constraints explicitly documented in full in SpecShell v3.3 DDL.

5 · PK/FK Summary Matrix (Explicit v3.3)

| Table                    | Primary Key      | Foreign Keys                                                          |
| ------------------------ | ---------------- | --------------------------------------------------------------------- |
| DimDate                  | DateID           | —                                                                     |
| DimProduct               | ProductID        | SupplierID → DimSupplier                                              |
| DimStore                 | StoreID          | —                                                                     |
| DimCustomer              | CustomerID       | AssignedRepID → DimSalesRep                                           |
| DimPromotion             | PromotionCode    | —                                                                     |
| DimSalesRep              | SalesRepID       | StoreID → DimStore                                                    |
| DimReturnReason          | ReturnReasonID   | —                                                                     |
| DimCampaign              | CampaignID       | —                                                                     |
| FactOrderHeader          | OrderID          | DateID, CustomerID, StoreID, SalesRepID, PaymentTypeID, PromotionCode |
| FactOrderItems           | OrderItemID      | OrderID → FactOrderHeader, ProductID → DimProduct, DateID → DimDate   |
| FactOrderReturns         | ReturnID         | OrderID, ProductID, DateID, ReturnReasonID                            |
| FactInventoryEvents      | EventID          | EventTypeID, ProductID, StoreID, SupplierID, DateID                   |
| FactCustomerInteractions | InteractionID    | CustomerID, SalesRepID, InteractionTypeID, DateID                     |
| FactSales                | SalesFactID      | DateID, StoreID                                                       |
| FactInventorySnapshot    | SnapshotDateID   | SnapshotDateID → DimDate, ProductID → DimProduct, StoreID → DimStore  |
| FactOrderStatus          | OrderStatusID    | SnapshotDateID → DimDate, OrderID → FactOrderHeader                   |
| FactCostOfGoods          | COGSID           | DateID, ProductID, StoreID                                            |
| FactCampaignSpend        | CampaignSpendID  | CampaignID, DateID                                                    |
| FactOrderItemPromotion   | OrderItemPromoID | OrderID, ProductID, PromotionCode                                     |
| FactFootTraffic          | FootTrafficID    | StoreID, DateID                                                       |
| FactLeadLifecycle (opt.) | LeadLifecycleID  | CustomerID, DateID                                                    |

Change-log
2025-07-22 – v3.3: Explicitly aligned with SpecShell v3.3; added 7 dims, 12 facts, standardised audit columns, added explicit IX_FactSales_FK, included explicit PK/FK summary.
