SELECT name, type_desc 
FROM sys.tables 
ORDER BY name;


SELECT t.name AS TableName,
       c.name AS ColumnName,
       typ.name AS DataType
FROM sys.tables t
LEFT JOIN sys.columns c ON c.object_id = t.object_id
LEFT JOIN sys.types typ ON c.user_type_id = typ.user_type_id
WHERE t.name IN ('DimCustomer','DimDate','DimProduct','DimSalesRep','DimSourceSystem','DimStore')
  AND c.name IN ('LoadDate', 'SourceSystem', 'RecordHash')
ORDER BY t.name, c.name;


CREATE TABLE dbo.DimReturnReason
(
    ReasonID        INT IDENTITY(1,1) PRIMARY KEY,
    ReasonDesc      NVARCHAR(40) NOT NULL,
    LoadDate        DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem    NVARCHAR(50) NOT NULL,
    RecordHash      CHAR(64)     NOT NULL
);

CREATE TABLE dbo.FactSales
(
    FactSalesID     BIGINT IDENTITY(1,1) PRIMARY KEY,
    DateID          INT NOT NULL,
    StoreID         INT NOT NULL,
    ProductID       INT NOT NULL,
    CustomerID      INT NULL,
    SalesRepID      INT NULL,
    Quantity        DECIMAL(18,2) NOT NULL,
    NetSalesAmount  DECIMAL(19,4) NOT NULL,
    DiscountAmount  DECIMAL(19,4) NULL,
    CostAmount      DECIMAL(19,4) NULL,
    LoadDate        DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem    NVARCHAR(50) NOT NULL,
    RecordHash      CHAR(64) NOT NULL,
    INDEX IX_FactSales_FK (DateID, StoreID, ProductID) INCLUDE (NetSalesAmount, Quantity)
);



CREATE TABLE dbo.FactInventorySnapshot
(
    SnapshotDateID INT NOT NULL,
    StoreID        INT NOT NULL,
    ProductID      INT NOT NULL,
    ClosingQty     DECIMAL(18,2) NOT NULL,
    ClosingCost    DECIMAL(19,4) NULL,
    LoadDate       DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem   NVARCHAR(50) NOT NULL,
    RecordHash     CHAR(64) NOT NULL,
    CONSTRAINT PK_FactInventorySnapshot PRIMARY KEY (SnapshotDateID, StoreID, ProductID)
);


CREATE TABLE dbo.FactOrderStatus
(
    OrderStatusID  BIGINT IDENTITY(1,1) PRIMARY KEY,
    OrderID        NVARCHAR(40) NOT NULL,
    StatusDateID   INT NOT NULL,
    StatusCode     NVARCHAR(20) NOT NULL,
    CustomerID     INT NULL,
    StoreID        INT NULL,
    LoadDate       DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem   NVARCHAR(50) NOT NULL,
    RecordHash     CHAR(64) NOT NULL
);


CREATE TABLE dbo.FactReturn
(
    FactReturnID   BIGINT IDENTITY(1,1) PRIMARY KEY,
    ReturnDateID   INT NOT NULL,
    StoreID        INT NOT NULL,
    ProductID      INT NOT NULL,
    CustomerID     INT NULL,
    ReturnReasonID INT NOT NULL,
    ReturnQty      DECIMAL(18,2) NOT NULL,
    ReturnAmount   DECIMAL(19,4) NOT NULL,
    LoadDate       DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem   NVARCHAR(50) NOT NULL,
    RecordHash     CHAR(64) NOT NULL
);


CREATE TABLE dbo.FactCostOfGoods
(
    CostDateID     INT NOT NULL,
    ProductID      INT NOT NULL,
    UnitCost       DECIMAL(19,4) NOT NULL,
    CurrencyCode   CHAR(3) NOT NULL DEFAULT 'USD',
    LoadDate       DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem   NVARCHAR(50) NOT NULL,
    RecordHash     CHAR(64) NOT NULL,
    CONSTRAINT PK_FactCostOfGoods PRIMARY KEY (CostDateID, ProductID)
);


SELECT name FROM sys.tables ORDER BY name;
-- Should now list all expected dimensions and facts (13 tables total)


CREATE TABLE dbo.DimSupplier
(
    SupplierID      INT IDENTITY(1,1) PRIMARY KEY,
    SupplierName    NVARCHAR(100) NOT NULL,
    LoadDate        DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem    NVARCHAR(50) NOT NULL,
    RecordHash      CHAR(64) NOT NULL
);


CREATE TABLE dbo.DimPaymentType
(
    PaymentTypeID   INT IDENTITY(1,1) PRIMARY KEY,
    PaymentType     NVARCHAR(50) NOT NULL,
    LoadDate        DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem    NVARCHAR(50) NOT NULL,
    RecordHash      CHAR(64) NOT NULL
);


CREATE TABLE dbo.DimInteractionType
(
    InteractionTypeID INT IDENTITY(1,1) PRIMARY KEY,
    InteractionType   NVARCHAR(50) NOT NULL,
    LoadDate          DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem      NVARCHAR(50) NOT NULL,
    RecordHash        CHAR(64) NOT NULL
);


CREATE TABLE dbo.DimEventType
(
    EventTypeID     INT IDENTITY(1,1) PRIMARY KEY,
    EventType       NVARCHAR(50) NOT NULL,
    LoadDate        DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem    NVARCHAR(50) NOT NULL,
    RecordHash      CHAR(64) NOT NULL
);


CREATE TABLE dbo.DimCampaign
(
    CampaignID      INT IDENTITY(1,1) PRIMARY KEY,
    CampaignName    NVARCHAR(60) NOT NULL,
    Channel         NVARCHAR(30) NOT NULL,
    Budget          DECIMAL(12,2) NOT NULL,
    StartDate       DATE NOT NULL,
    EndDate         DATE NOT NULL,
    LoadDate        DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem    NVARCHAR(50) NOT NULL,
    RecordHash      CHAR(64) NOT NULL
);


CREATE TABLE dbo.DimPromotion
(
    PromotionCode   NVARCHAR(15) PRIMARY KEY,
    Description     NVARCHAR(60) NOT NULL,
    DiscountType    NVARCHAR(10) NOT NULL,
    DiscountValue   DECIMAL(5,2) NOT NULL,
    StartDate       DATE NOT NULL,
    EndDate         DATE NOT NULL,
    PromoCost       DECIMAL(10,2) NOT NULL,
    CampaignID      INT NULL FOREIGN KEY REFERENCES DimCampaign(CampaignID),
    LoadDate        DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem    NVARCHAR(50) NOT NULL,
    RecordHash      CHAR(64) NOT NULL
);


CREATE TABLE dbo.FactOrderHeader
(
    OrderID         INT PRIMARY KEY,
    FreightCost     DECIMAL(8,2) NOT NULL,
    DateID          INT NOT NULL,
    ShipDateID      INT NULL,
    CustomerID      INT NOT NULL,
    StoreID         INT NOT NULL,
    SalesRepID      INT NOT NULL,
    PaymentTypeID   INT NOT NULL,
    PromotionCode   NVARCHAR(15) NULL FOREIGN KEY REFERENCES DimPromotion(PromotionCode),
    OrderTotal      DECIMAL(10,2) NOT NULL,
    LoadDate        DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem    NVARCHAR(50) NOT NULL,
    RecordHash      CHAR(64) NOT NULL
);


CREATE TABLE dbo.FactInventoryEvents
(
    EventID         INT IDENTITY(1,1) PRIMARY KEY,
    EventTypeID     INT NOT NULL FOREIGN KEY REFERENCES DimEventType(EventTypeID),
    ProductID       INT NOT NULL,
    StoreID         INT NOT NULL,
    SupplierID      INT NOT NULL FOREIGN KEY REFERENCES DimSupplier(SupplierID),
    Qty             INT NOT NULL,
    DateID          INT NOT NULL,
    RelatedEventID  INT NULL,
    LoadDate        DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem    NVARCHAR(50) NOT NULL,
    RecordHash      CHAR(64) NOT NULL
);


CREATE TABLE dbo.FactCustomerInteractions
(
    InteractionID       INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID          INT NOT NULL,
    SalesRepID          INT NOT NULL,
    InteractionTypeID   INT NOT NULL FOREIGN KEY REFERENCES DimInteractionType(InteractionTypeID),
    DateID              INT NOT NULL,
    Notes               NVARCHAR(MAX) NULL,
    LoadDate            DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem        NVARCHAR(50) NOT NULL,
    RecordHash          CHAR(64) NOT NULL
);


CREATE TABLE dbo.FactCampaignSpend
(
    CampaignSpendID INT IDENTITY(1,1) PRIMARY KEY,
    CampaignID      INT NOT NULL FOREIGN KEY REFERENCES DimCampaign(CampaignID),
    DateID          INT NOT NULL,
    SpendAmount     DECIMAL(12,2) NOT NULL,
    LoadDate        DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem    NVARCHAR(50) NOT NULL,
    RecordHash      CHAR(64) NOT NULL
);


CREATE TABLE dbo.FactOrderItemPromotion
(
    BridgeID        INT IDENTITY(1,1) PRIMARY KEY,
    OrderItemID     BIGINT NOT NULL,
    PromotionCode   NVARCHAR(15) NOT NULL FOREIGN KEY REFERENCES DimPromotion(PromotionCode),
    CampaignID      INT NOT NULL FOREIGN KEY REFERENCES DimCampaign(CampaignID),
    PromoDiscount   DECIMAL(7,2) NOT NULL,
    PromoRevenue    DECIMAL(9,2) NOT NULL,
    LoadDate        DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem    NVARCHAR(50) NOT NULL,
    RecordHash      CHAR(64) NOT NULL
);


CREATE TABLE dbo.FactFootTraffic
(
    FootTrafficID   INT IDENTITY(1,1) PRIMARY KEY,
    StoreID         INT NOT NULL,
    DateID          INT NOT NULL,
    VisitCount      INT NOT NULL,
    LoadDate        DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem    NVARCHAR(50) NOT NULL,
    RecordHash      CHAR(64) NOT NULL
);


CREATE TABLE dbo.FactLeadLifecycle
(
    LeadLifecycleID   INT IDENTITY(1,1) PRIMARY KEY,
    LeadID            INT NOT NULL,
    CustomerID        INT NOT NULL,
    StageCode         NVARCHAR(10) NOT NULL,
    StageStartDateID  INT NOT NULL,
    StageEndDateID    INT NOT NULL,
    AssignedRepID     INT NOT NULL,
    CampaignID        INT NOT NULL FOREIGN KEY REFERENCES DimCampaign(CampaignID),
    LoadDate          DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SourceSystem      NVARCHAR(50) NOT NULL,
    RecordHash        CHAR(64) NOT NULL
);


