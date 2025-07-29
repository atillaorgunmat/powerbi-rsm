<!------------ 2025‑07‑17 Road‑map extension START ------------>
## 2025‑07‑17 → 2025‑07‑22 – Road‑map & Execution Log

| Task ID | Phase | Title | State | Depends On | Impact / Rationale & Key Lesson |
|---------|-------|-------|-------|-----------|---------------------------------|
| T‑0031b | P‑03 Design | Schema Gap Analysis | ✅ Done | – | **LL:** Verify both sides of a diff contain *all* objects – empty reports can be false passes. |
| T‑0031c | P‑03 Design | Schema Alignment Migration | ✅ Done | T‑0031b | **LL:** `sqlpackage /Action:Script` needs `/TargetDatabaseName` plus a target endpoint; ADS cannot “Generate Scripts”. |
| T‑0032 | P‑04 Build DW | Incremental‑Load Engine | Planned | T‑0042 | – |
| T‑0033 | P‑04 Build DW | Snapshot Fact POC | Planned | T‑0032 | – |
| T‑0034 | P‑04 Build DW | SCD Type‑2 Automation | Planned | T‑0032 | – |
| T‑0035 | P‑05 Monitor | Data‑Quality Dashboard | Planned | T‑0032 | – |
| T‑0036 | P‑06 Analytics & Viz | Semantic Model & KPI DAX | Planned | T‑0033, T‑0034 | – |
| T‑0037 | P‑07 Ops | CI/CD Pipeline | Planned | T‑0032 | – |
| T‑0038 | P‑04 Build DW | Performance Benchmark | Planned | T‑0033 | – |
| T‑0039 | P‑08 Governance | Automated Documentation | Planned | T‑0032 | – |
| T‑0040 | P‑09 Close‑out | Knowledge‑Transfer Pack | Planned | T‑0036 – T‑0039 | – |
| T‑0042 | P‑02 Planning | Data‑Spec Sheet v3.3.1 | ✅ Done | T‑0031c | Spec aligned, SnapshotDateID FK added; lesson: keep Blank.dacpac & $LOG under repo root. |
| T‑0043 | P‑04 Build DW | Retail Data Model v2.1 | ✅ Done | T‑0042 | ERD & narrative delivered; Spec‑first, script‑verify method adopted. |
| T‑0044 | P‑05 Measure | KPI Extensions v3.0 | ✅ Done | T‑0043 | KPI List (IDs 001‑032) & KPI Cards v3.0 finalised; lesson: lock KPI_ID sequence to prevent collisions. |
| T‑0045 | P‑05 Measure | Data_KPI_Trace_Matrix v3.0 | ✅ Done | Depends On: T‑0044 | Matrix manually verified (32 KPIs); manual confirm accepted. |
| T‑0046 | P‑04 Build DW | Strategy Docs v2.1 | ✅ Done | Depends On: T‑0043 | Snapshot & SCD strategies refreshed. |
| T‑0047 | P‑04 Build DW | ETL & Audit Strategy v2.1 | ✅ Done | Depends On: T‑0032 | Strategy finalised (watermark & templates). |
| T‑0048 | P‑02 Planning | Data Design v1.0 | ✅ Done | Depends On: T‑0042 | Umbrella schema/model guide created; links conventions, source map, and governance rules. |
| T‑0049 | P‑02 Planning | Integration Design v1.0 | ✅ Done | Depends On: T‑0047 | Source inventory, landing conventions, data‑flow diagram, DQ checkpoints, and SLAs documented. |
| T‑0050 | P‑04 Build DW | Seed Data & Test Harness v1.0 | Planned | T‑0032 | – |
| T‑0051 | P‑05 Measure | KPI Sanity / Regression Suite | Planned | T‑0044, T‑0050 | – |

| **S-001** | P-04 Build DW | Landing Folder Tree & Sample Files | **In-Progress** | Integration Design v1.0 | **S-001a ✅** folder tree • **S-001b ✅** README • **S-001c ✅** 4 sample files • **S-001d 🟡** schema_lint pending (spec file on VM) |


### Key Decisions Log
*2025‑07‑22 – Confirmed Data‑Spec Sheet v3.3 aligned with SpecShell v3.3; adopted permanent `$LOG` directory and **Blank.dacpac** rule for all `/a:Script` actions; documented that `/TargetFile` path must exist before execution.*
*2025‑07‑23 – Identified missing SnapshotDateID → DimDate FK; updated Data‑Spec v3.3.1 and ERD accordingly.*
*2025‑07‑23 – KPI List & Cards v3.0 ratified (IDs 001‑032); ensured every new KPI maps to a fact table.  
2025‑07‑23 – Adopted Spec‑first ER‑diagram method with FK diff check in CI; updated Data‑Spec to v3.3.1.*
2025‑07‑23 – Manual verification accepted for KPI Trace Matrix; automation deferred until CI task.
2025‑07‑23 – Snapshot & SCD strategies updated (v2.1) to cover new facts/dims, hash‑diff method, and Power BI incremental refresh.
2025‑07‑23 – ETL strategy to include explicit Watermark & BatchLog tables and generic load templates.
2025‑07‑23 – Finalised ETL strategy v2.1: standardised watermark table, batch logging, and dim/fact loader templates; reinforced PII‑safe hashing.
2025‑07‑24 – Agreed to create Data_Design.md as umbrella schema & modelling guide; no separate Roadmap file required.
2025‑07‑24 – Data_Design v1.0 established as central modelling guide; re‑uses Plan zero phase headings.
2025‑07‑24 – Integration_Design v1.0 approved to consolidate pipeline architecture; Roadmap file remains in Storyboard.
2025‑07‑24 – Integration_Design v1.0 finalised as central pipeline architecture doc; aligns with Data_Design v1.0 and ETL strategy v2.1.
2025‑07‑24 – Mini‑roadmap S‑001…S‑007 approved to guarantee data & metadata prerequisites before starting Incremental‑Load Engine (T‑0032).
*2025‑07‑25 – Established canonical landing-zone folder pattern (/landing/<source>/<YYYYMMDD>/) with README; enables repeatable hash‑diff and watermark logic for T‑0032.*
*2025‑07‑25 – Landing zone README created; folder pattern and 30‑day retention rule documented.*
*2025-07-25 – Enforced **ASCII-only filenames** and “run `pwd` first” rule to eliminate hidden Unicode dash errors in CLI; adopted atomic `scp` commands from project root (`~/Projects/PowerBI-RSM`).*  
*2025-07-25 – Landing zone folder pattern `/landing/<source>/<YYYYMMDD>/` + README + 30-day retention established for incremental load engine.*  





<!------------ 2025‑07‑17 Road‑map extension END ------------>
