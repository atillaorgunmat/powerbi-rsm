<#  Builds Spec.dacpac from the SQL Project
    Usage: .\T-0031b_build_spec_dacpac.ps1 -SqlProjPath "..\RetailStaging_Spec_v32.sqlproj" -OutDir "..\gap_analysis"
#>
param(
  [string]$SqlProjPath = "..\RetailStaging_Spec_v32.sqlproj",
  [string]$OutDir      = "..\gap_analysis"
)
Write-Host "Building DACPAC from $SqlProjPath ..."
dotnet build $SqlProjPath -c Release
$dacpac = Get-ChildItem -Path (Split-Path $SqlProjPath) -Recurse -Filter *.dacpac | Select-Object -First 1
Copy-Item $dacpac.FullName -Destination (Join-Path $OutDir "Spec.dacpac") -Force
Write-Host "Spec.dacpac created."
