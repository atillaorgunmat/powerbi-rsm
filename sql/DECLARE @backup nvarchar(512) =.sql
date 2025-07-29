DECLARE @backup nvarchar(512) =
  N'C:\Backups\RetailStaging_preT0031_' +
  CONVERT(char(8), GETDATE(), 112) + '.bak';

BACKUP DATABASE RetailStaging
 TO DISK = @backup
 WITH INIT, COPY_ONLY, 
      NAME = 'Pre-T0031 safeguard';

PRINT 'Backup created at ' + @backup;

