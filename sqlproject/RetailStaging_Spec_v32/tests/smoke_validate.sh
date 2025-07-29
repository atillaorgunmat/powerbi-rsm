#!/usr/bin/env bash
: "${SQL_CONN:?❌ Set SQL_CONN variable first (export SQL_CONN=...)}"

set -euo pipefail


# --- connection parsing ---
SERVER=$(echo "$SQL_CONN" | sed -n 's/.*Server=\([^;,]*\).*/\1/p')
PORT=$(echo "$SQL_CONN"   | sed -n 's/.*Server=[^,]*,\([0-9]*\).*/\1/p')
PORT=${PORT:-1433}   # default if comma-port not present
# --------------------------

echo "👋 Smoke-test: ping SQL Server..."
nc -vz "$SERVER" "$PORT"

echo "🛠 Extracting live database schema → tmp.dacpac"
sqlpackage /a:Extract /tf:tmp.dacpac /SourceConnectionString:"$SQL_CONN"

echo "🔍 Comparing extracted schema to Spec.dacpac v3.3"
mkdir -p tmp
sqlpackage /a:DeployReport \
           /sf:tmp.dacpac \
           /tf:Spec.dacpac \
           /op:tmp/deploy_report.xml \
           /TargetDatabaseName:SchemaDiffTemp 

if ! grep -q "<Operation " tmp/deploy_report.xml; then
  echo "✅ Schema matches exactly."
else
  echo "❌ Schema differences detected!"
  exit 1
fi

