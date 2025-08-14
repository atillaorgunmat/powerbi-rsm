# Storyboard

<!------------ 2025-07-17 Road-map extension START ------------>
## 2025-07-17 – Added task batch T-0031b → T-0040

| Task ID | Phase | Title | State | Impact / Rationale |
|---------|-------|-------|-------|--------------------|
| T-0031b | P-03 Design | Schema Gap Analysis | Done | Produce authoritative diff between Data-Spec and live DB to eliminate hidden drift. |
| T-0031c | P-03 Design | Schema Alignment Migration | Done | Reconcile all gaps via idempotent script; regenerates canonical DACPAC. |
| T-0032 | P-04 Build DW | Incremental-Load Engine | Planned | Hash-diff + water-mark logic enables daily delta processing. |
| T-0033 | P-04 Build DW | Snapshot Fact POC | Planned | Materialise daily inventory snapshot fact for historical KPIs. |
| T-0034 | P-04 Build DW | SCD Type-2 Automation | Planned | Generic MERGE template maintains dimensional history. |
| T-0035 | P-05 Monitor | Data-Quality Dashboard | Planned | Surfaces audit metrics + alerts for late or failed loads. |
| T-0036 | P-06 Analytics & Viz | Semantic Model & KPI DAX | Planned | Power BI dataset with 15 priority KPIs validated against trace matrix. |
| T-0037 | P-07 Ops | CI/CD Pipeline | Planned | GitHub Actions workflow publishes DACPAC & PBIX on push to main. |
| T-0038 | P-04 Build DW | Performance Benchmark | Planned | Establish baseline query runtimes & index plan for 12-month volume. |
| T-0039 | P-08 Governance | Automated Documentation | Planned | Nightly schema & lineage export to HTML doc site. |
| T-0040 | P-09 Close-out | Knowledge-Transfer Pack | Planned | Runbook v1.0 + Storyboard updates for hand-off. |
| T‑0031b‑R | P‑03 Design | Robust Gap Analysis (FULL SpecShell) | Done | Populate SpecShell with all tables, regenerate Spec.dacpac, rerun diff; must reach zero gaps. |
| T-0031c | P-03  | SpecShell Finalisation & Zero-Gap Verification | Done | Ensure authoritative DACPAC has zero discrepancies explicitly documented.                                          |
| T-0032  | P-04  | Incremental-Load Engine v1.1                   | Planned | Broadened to explicitly include all dims/facts from the updated Data-Spec v3.2 for comprehensive delta-loading.    |
| T-0041  | P-05  | Multi-Fact ETL & KPI Extension                 | Planned | Add explicit ETL & DAX logic for newly introduced fact tables (Returns, Cost, Campaign) to close KPI coverage gap. |
## 2025‑07‑22 – Documentation & Test Roadmap Approved
| T‑0042 | P‑02 Planning | Data‑Spec Sheet v3.3 | Planned | Sync doc with SpecShell after T‑0031c; adds 7 dims & 12 facts. |
| T‑0043 | P‑04 Build DW | Retail Data Model v2.1 | Planned | New ER diagram and narrative incl. FK lines for all tables. |
| T‑0044 | P‑05 Measure | KPI Extensions v3.0 | Planned | Adds return‑rate, COGS %, campaign ROI KPIs. |
| T‑0045 | P‑05 Measure | Trace Matrix v3.1 | Planned | Maps new KPIs to new facts, zero unmapped rows. |
| T‑0046 | P‑04 Build DW | Strategy Docs v2.1 | Planned | Snapshot & SCD docs updated for new tables. |
| T‑0047 | P‑04 Build DW | ETL & Audit Strategy v2.1 | Planned | Documents hash‑diff + watermark logic of T‑0032 engine. |
| T‑0048 | P‑01 Foundation | Plan zero & Storyboard Refresh | Planned | Governance docs catch up with roadmap changes. |
| T‑0049 | P‑02 Planning | Charter Scope Addendum v1.1 | Planned | Charter updated to include CI/CD & extended KPI ambitions. |
| T‑0050 | P‑04 Build DW | Seed Data & Test Harness v1.0 | Planned | Provides automated incremental‑load regression tests. |
| T‑0051 | P‑05 Measure | KPI Sanity / Regression Suite | Planned | Baseline KPI regression tests before DAX build. |




### Key Decisions Log
*2025-07-17 – Approved nine-task roadmap (T-0031b → T-0040) to guarantee schema-spec parity before industrialising pipelines and reporting stack.*
*2025‑07‑22 – Integrated seed‑data test harness & KPI regression suite (T‑0050, T‑0051) into roadmap to de‑risk pipelines before DAX build.*

<!------------ 2025-07-17 Road-map extension END ------------>

| Task ID | Lessons Learned |
| T-0031b | Implicit wildcards compile everything. Always pair a global “remove” with explicit folder-based Build Include rules to prevent disabled or ad-hoc scripts from entering the model. RetailStaging_Spec_v32

Platform-specific flags matter. SqlPackage uses /op: on macOS/Linux; /dr: is Windows-only.

File-type whitelists affect visibility. Rename .sqlproj → .txt (or another text extension) when you need ChatGPT preview.

Empty gap reports can be a false pass. Verify that the Spec DACPAC truly contains all objects in the Data-Spec Sheet—otherwise both sides may be “missing” the same tables.

Separate build artefacts from migration history. Keep object DDL under /schema/… and legacy upgrades under /migrations/… to avoid accidental compilation. |

| T-0031c | SqlPackage CLI Explicit Rules:

Do not combine /SourceDatabaseName and /SourceConnectionString.

/Action:Script explicitly requires /TargetDatabaseName even for DACPAC targets.

Cross-platform compatibility explicitly requires careful use of /op: (macOS/Linux) vs /dr: (Windows-only).

Keep $LOG under repo root; build Blank.dacpac once and reuse; /a:Script needs real TargetFile.”

Azure Data Studio (ADS) Explicit Limitations:

"Generate Scripts" explicitly not supported within ADS (≥ v1.47), making SqlPackage CLI necessary.

Schema compare explicitly fails with zero-byte DACPAC ("Central Directory corrupt").

Explicit Project Hygiene:

.sqlproj explicitly must exclude ad-hoc or migration log scripts using <Build Remove> and <None Include> directives.

Verify DACPAC generation context explicitly to avoid discrepancies between ADS and SSDT.

Gap Analysis Explicit Validation:

Initial empty gap reports explicitly can be false-positive; always validate against Data-Spec Sheet v3.2. |

