CREATE TABLE dbo.DimCustomer (
    CustomerID   INT PRIMARY KEY,
    CustomerName NVARCHAR(80) NOT NULL,
    Gender       CHAR(1) NULL CHECK (Gender IN ('M','F')),
    BirthDate    DATE NULL,
    Email        NVARCHAR(120) NULL,
    Phone        NVARCHAR(30)  NULL,
    LoyaltyTier  NVARCHAR(20) NULL,
    LoadDate     DATETIME NOT NULL DEFAULT (GETUTCDATE()),
    SourceSystem NVARCHAR(50) NOT NULL DEFAULT ('UNKNOWN')
                 CHECK (SourceSystem IN ('POS','ERP','CRM','CSV')),
    RecordHash   NVARCHAR(64) NULL CHECK (RecordHash IS NULL OR LEN(RecordHash)=64)
);
