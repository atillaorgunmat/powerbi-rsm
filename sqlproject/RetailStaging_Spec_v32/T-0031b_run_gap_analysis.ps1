<#
.SYNOPSIS
    Schema gap analysis — compares Spec DACPAC to target DB and writes schema_gap_report.md

.PARAMETER Spec
    Path to Spec.dacpac extracted from SpecShell

.PARAMETER TargetConnection
    Full connection string for the target database to compare (RetailStaging)

.EXAMPLE
    ./T-0031b_run_gap_analysis.ps1 `
        -Spec "./Spec.dacpac" `
        -TargetConnection "Data Source=20.117.181.28,1433;Initial Catalog=RetailStaging;User Id=sa;Password=*****;Encrypt=False;TrustServerCertificate=True"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Spec,
    [Parameter(Mandatory = $true)]
    [string]$TargetConnection
)

# ----- Paths -----
$root      = Split-Path -Parent $Spec
$gapXml    = Join-Path $root "gap.xml"
$mdReport  = Join-Path $root "schema_gap_report.md"

# ----- Run SqlPackage DeployReport -----
Write-Host "Running SqlPackage DeployReport…" -ForegroundColor Cyan
& sqlpackage /a:DeployReport `
             /SourceFile:$Spec `
             /TargetConnectionString:$TargetConnection `
             /op:$gapXml /Quiet

if ($LASTEXITCODE -ne 0) {
    Write-Error "SqlPackage failed (exit $LASTEXITCODE)"; exit $LASTEXITCODE
}

# ----- Parse gap.xml -----
[xml]$xml = Get-Content $gapXml
$ops = $xml.DeploymentReport.Operations.Operation |
       Where-Object { $_.Type -ne 'NotSupported' }

if (!$ops) {
    "NO_GAPS" | Set-Content $mdReport
    Write-Host "NO_GAPS — schema aligned." -ForegroundColor Green
    exit 0
}

# ----- Build Markdown report -----
$lines = @(
    "# Schema Gap Report",
    "",
    "| Object | Issue |",
    "|--------|-------|"
)
foreach ($o in $ops) {
    $lines += "| $($o.Name) | $($o.Type) |"
}
$lines | Set-Content $mdReport
Write-Host "Gaps found — see schema_gap_report.md" -ForegroundColor Yellow
exit 1

