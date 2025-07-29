CREATE TABLE dbo.DimSalesRep (
    SalesRepID   INT PRIMARY KEY,
    SalesRepName NVARCHAR(80) NOT NULL,
    Region       NVARCHAR(40) NULL,
    HireDate     DATE NULL,
    TermDate     DATE NULL,
    Status       NVARCHAR(15) NULL,
    LoadDate     DATETIME NOT NULL DEFAULT (GETUTCDATE()),
    SourceSystem NVARCHAR(50) NOT NULL DEFAULT ('UNKNOWN')
                 CHECK (SourceSystem IN ('POS','ERP','CRM','CSV')),
    RecordHash   NVARCHAR(64) NULL CHECK (RecordHash IS NULL OR LEN(RecordHash)=64)
);
