# Plan.md v0.1 

## Phases

### P‑01 · Foundation
| Goal | Key Outputs | Exit Check |
|------|-------------|------------|
| Lay structural bedrock for all later work. | • One‑time folder & repo setup<br>• Charter v1.1 (finalised)<br>• Initial Risk Log (open) | Repo tree passes inspection; Charter signed by Governor; Risk Log exists in `/docs/`. |

---

### P‑02 · Initiation & Detailed Planning
| Focus | Deliverables | Acceptance |
|-------|-------------|------------|
| Confirm analytics scope & blueprint. | • KPI cards for Sales, Ops, Exec in `/docs/kpi_cards/`<br>• Data‑spec sheet listing every table/field + sample rows | All stakeholders (Gov + any SMEs) sign KPI list & data spec. |

---

### P‑03 · Data Source Provisioning & Environment Setup
| Focus | Deliverables | Acceptance |
|-------|-------------|------------|
| Make raw data reachable & stand up infra. | • Sample CSV/JSON committed to `/data/sources/`<br>• SQL DDL script (`/scripts/`)<br>• On‑prem gateway online & tested | Power BI Fabric can preview each source without error. |

---

### P‑04 · Data Ingestion & Star‑Schema Modelling
| Focus | Deliverables | Acceptance |
|-------|-------------|------------|
| Build robust staging + dimensional model. | • PBIX / Fabric dataset v0.2<br>• ERD diagram `/docs/ERD.png` | Dim→Fact joins validated; Date slicer filters all facts. |

---

### P‑05 · Measure Engineering & Validation
| Focus | Deliverables | Acceptance |
|-------|-------------|------------|
| Implement & QA all DAX KPIs. | • PBIX v0.3 with measures<br>• QA sheet `/docs/measure_tests.xlsx` | 100 % test cases pass; no visual > 2 s in Perf Analyzer. |

---

### P‑06 · Sales Dashboard
| Focus | Deliverables | Acceptance |
|-------|-------------|------------|
| Build revenue‑centric UX. | • PBIX v0.4<br>• Screenshot + micro‑UX notes `/docs/` | Scenario “find under‑target region” in ≤ 3 clicks. |

---

### P‑07 · Operations Dashboard
| Focus | Deliverables | Acceptance |
|-------|-------------|------------|
| Surface supply‑chain & stock health. | • PBIX v0.5<br>• Feedback log from Ops persona | Scenario “supplier causing most stock‑outs last month” answerable on page. |

---

### P‑08 · Executive Dashboard & Polish
| Focus | Deliverables | Acceptance |
|-------|-------------|------------|
| Craft high‑level narrative & presentation polish. | • PBIX v0.6<br>• Theme JSON & final assets | 30‑second health‑scan demo ≥ 4 / 5 clarity score. |

---

### P‑09 · Testing, Deployment & Handoff
| Focus | Deliverables | Acceptance |
|-------|-------------|------------|
| Ship & transfer ownership. | • Fabric workspace link<br>• Docs bundle (zipped) in `/docs/`<br>• Loom walkthrough links in README | Two refresh cycles succeed; all RLS tests pass; hand‑off pack complete. |

---

## Top‑Level Work Breakdown ( MECE )

1. **Structural Setup & Governance (P‑01)**  
2. **Scope Finalisation – KPIs & Data Spec (P‑02)**  
3. **Source Acquisition & Environment Provisioning (P‑03)**  
4. **Data Staging & Dimensional Modelling (P‑04)**  
5. **Measure Development & Validation (P‑05)**  
6. **Sales Analytics UX (P‑06)**  
7. **Operational Analytics UX (P‑07)**  
8. **Executive Analytics UX & Polish (P‑08)**  
9. **Deployment, Testing & Knowledge Transfer (P‑09)**  

These nine items collectively cover the end‑to‑end BI solution with no overlap. Any sub‑work will inherit the Phase ID as its parent.

---

## Rolling Governance

- **Weekly Checkpoint:** 15‑min summary issue titled `WK‑NN Status`, linked from `Tasks.md`.  
- **Risk Log:** update whenever a risk is opened/closed or re‑scored.  
- **Backlog Grooming:** every Friday; Executor may split/merge tasks ≤ 15 % scope without re‑charter.

*End Plan.md v0.1*
