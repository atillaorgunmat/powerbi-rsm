CREATE TABLE dbo.DimStore (
    DimStoreSK  INT IDENTITY(1,1) PRIMARY KEY,
    StoreID     INT          NOT NULL,
    StoreName   NVARCHAR(80) NOT NULL,
    Region      NVARCHAR(40) NULL,
    StoreType   NVARCHAR(25) NULL,
    Status      NVARCHAR(15) NULL,
    ValidFrom   DATE         NOT NULL,
    ValidTo     DATE         NOT NULL DEFAULT ('9999-12-31'),
    IsCurrent   BIT          NOT NULL DEFAULT (1),
    UNIQUE (StoreID, ValidFrom),
    LoadDate    DATETIME     NOT NULL DEFAULT (GETUTCDATE()),
    SourceSystem NVARCHAR(50) NOT NULL DEFAULT ('UNKNOWN')
                 CHECK (SourceSystem IN ('POS','ERP','CRM','CSV')),
    RecordHash  NVARCHAR(64) NULL CHECK (RecordHash IS NULL OR LEN(RecordHash)=64)
);
