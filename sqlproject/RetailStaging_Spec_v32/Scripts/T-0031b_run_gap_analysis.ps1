<#  Generates DeployReport.xml and Markdown summary.
    Requires: Spec.dacpac already built.
    Usage: .\T-0031b_run_gap_analysis.ps1 -DbServer "20.117.181.28" -DbName "RetailStaging" -OutDir "..\gap_analysis"
#>
param(
  [string]$DbServer = "20.117.181.28",
  [string]$DbName   = "RetailStaging",
  [string]$OutDir   = "..\gap_analysis"
)
$sqlpackage = "~/sqlpackage/sqlpackage"
$spec       = Join-Path $OutDir "Spec.dacpac"
$report     = Join-Path $OutDir "DeployReport.xml"

& $sqlpackage /a:DeployReport `
    /sf:$spec `
    /tcs:"Server=$DbServer,1433;Database=$DbName;User ID=sa;Password=fatgyx-zinhy9-poCcip;Encrypt=False;TrustServerCertificate=True" `
    /op:$report
Write-Host "DeployReport created at $report"

# --- Convert XML to Markdown table ---
[xml]$xml = Get-Content $report
$md = @("# Schema Gap Report", "", "| Object | Issue |", "|--------|-------|")
foreach ($item in $xml.DeploymentReport.Operations.Operation) {
    $md += "| $($item.Name) | $($item.Message -replace '\|', '/') |"
}
$md += "" ; $md | Out-File (Join-Path $OutDir "schema_gap_report.md") -Encoding utf8
Write-Host "Markdown report generated."
