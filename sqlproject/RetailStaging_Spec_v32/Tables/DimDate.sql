CREATE TABLE dbo.DimDate (
    DateID       INT        PRIMARY KEY,          -- YYYYMMDD
    FullDate     DATE       NOT NULL,
    Year         SMALLINT   NOT NULL,
    Quarter      TINYINT    NOT NULL,
    MonthNo      TINYINT    NOT NULL,
    MonthName    NVARCHAR(9) NOT NULL,
    DayOfWeek    NVARCHAR(9) NOT NULL,
    -- Audit
    LoadDate     DATETIME   NOT NULL DEFAULT (GETUTCDATE()),
    SourceSystem NVARCHAR(50) NOT NULL DEFAULT ('UNKNOWN')
                 CHECK (SourceSystem IN ('POS','ERP','CRM','CSV')),
    RecordHash   NVARCHAR(64) NULL
);
-- Write your own SQL object definition here, and it'll be included in your package.
