/* === 1 | Instance & edition check === */
SELECT  SERVERPROPERTY('MachineName')      AS [Host],
        SERVERPROPERTY('Edition')          AS [Edition],
        SERVERPROPERTY('ProductVersion')   AS [SQL_Version],
        SERVERPROPERTY('EngineEdition')    AS [EngineEdition];   -- 4 = Express

/* === 2 | Database size & autogrowth === */
USE master;
SELECT  d.name AS [DB],
        CONVERT(DECIMAL(10,2), SUM(m.size)*8/1024.0) AS [Size_GB],
        SUM(m.size) AS [Size_Pages],
        MAX(m.max_size) AS [Max_Size_Pages]
FROM    sys.databases AS d
JOIN    sys.master_files AS m ON d.database_id = m.database_id
WHERE   d.name IN ('RetailStaging')          -- Adjust explicitly if your DB has different name
GROUP BY d.name;

/* === 3 | Free drive space === */
EXEC master..xp_fixeddrives; -- Free space per drive in MB

/* === 4 | TempDB size === */
SELECT  CONVERT(DECIMAL(10,2), SUM(size)*8/1024.0) AS [TempDB_Size_GB]
FROM    sys.master_files
WHERE   database_id = 2; -- tempdb

/* === 5 | BACKUP (COPY_ONLY) explicitly === */
DECLARE @backup nvarchar(512) =
N'C:\Backups\RetailStaging_preT0031_' +
 CONVERT(char(8), GETDATE(), 112) + '.bak';

BACKUP DATABASE RetailStaging
 TO  DISK = @backup
 WITH INIT, COPY_ONLY, COMPRESSION, NAME = 'Pre‐T0031 safeguard';

PRINT 'Backup created at ' + @backup;
