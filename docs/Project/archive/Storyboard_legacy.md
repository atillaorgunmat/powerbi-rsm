# Storyboard — Retail Multi-Source KPI Suite

Project Overview
Deliver a unified analytics solution integrating multiple data sources into a Power BI Fabric model. Enable strategic and operational insights via Sales, Operations, and Executive dashboards.

| Fact ID | Fact Description                                                                                                                                                       | Source                                   | Linked Tasks                                   |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- | ---------------------------------------------- |
| **F01** | Retail Multi-Source KPI Suite explicitly defined scope, KPI domains (Sales, Operations, CRM, Cross-Domain), and role-specific insights (Executive, Sales, Operations). | Project Charter.md                       | T-0002, T-0004, T-0005, T-0006, T-0007, T-0008 |
| **F02** | Detailed star-schema Retail Data Model explicitly defining Dimension and Fact tables, data structure, PK–FK relationships.                                             | Retail Data Model.md, Data-Spec Sheet.md | T-0001, T-0002, T-0003, T-0004, T-0008         |
| **F03** | Explicit KPI definitions, calculation methods, and source tables clearly documented and confirmed.                                                                     | KPI List v1.0.md, KPI\_Cards.md          | T-0005, T-0006, T-0007                         |
| **F04** | Explicit governance methodology (RSM v1.0) confirmed for structured solo project management.                                                                           | Plan zero.md                             | T-0003                                         |
| **F05** | Explicit decision made to consolidate all project documentation into unified Storyboard.md, explicitly replacing Plan.md and FactLog.md.                               | Explicit Governor Decision (Post T-0004) | T-0001, T-0004, T-0008                         |

P-01 · Foundation
Focus: Stand up baseline artefacts so analytical work can proceed clearly and explicitly.
Deliverables: D-1 folder skeleton, D-2 README, D-3 Storyboard v0.1, D-4 Context Kit SOP explicitly defined.
Acceptance: Governor explicitly confirms each deliverable present; explicitly verifies all tasks set to Done.

Task ID Title Depends on Linked Facts State Last Log
T-0001 Create folder skeleton — F02, F05 Done ✅ 2025-06-25 confirmed
T-0002 Draft README & Vision — F01, F02 Done ✅ 2025-06-25 committed
T-0003 Author Plan v0.1 T-0002 F02, F04 Done ✅ 2025-06-25 committed
T-0004 Seed Fact & Context SOP T-0002 F01, F02 Done ✅ 2025-06-25 migration

P-02 · Initiation & Detailed Planning
Focus: Confirm analytics scope and detailed planning blueprint explicitly aligned to project vision.
Deliverables: D-1 KPI Dictionary ("KPI List v1.0.md"), D-2 KPI Cards explicitly defined (Sales, Ops, Exec), D-3 Data-Spec Sheet (/docs/Data-Spec.md) explicitly populated.
Acceptance: Governor explicitly signs off KPI list and data specification.

Task ID Title Depends on Linked Facts State Last Log
T-0005 Gather KPI Definitions & Constraints — F01 Done ✅ 2025-06-28 KPI v1.0 commit
T-0006 Draft KPI Card Templates T-0005 F01 Done ✅ 2025-06-28 KPI Cards committed
T-0007 Validate KPI List w/ Governor T-0006 F01 Done ✅ 2025-06-28 explicitly validated
T-0008 Draft Data-Spec Sheet T-0007 F01, F02, F05 Done ✅ 2025-06-28 explicitly confirmed
T-0009 Build Data_KPI_Trace Matrix T-0008 F01, F02 Planned ⏳ Explicitly created after T-0008
T-0010 Load Sample Data & Prototype KPIs T-0008 F01, F02, F05 Planned ⏳ Explicitly created after T-0008
T-0011 Referential Integrity Tests T-0008 F01, F02 Planned ⏳ Explicitly created after T-0008