# Landing-Zone Conventions

| Item             | Rule                                          | Rationale                                   |
|------------------|-----------------------------------------------|---------------------------------------------|
| **Root**         | C:\landing\                                 | Mirrors Integration Design v1.0.            |
| **Source folders** | pos, oms, wms, mkt                  | POS sales, OMS orders, WMS inventory, marketing spend. |
| **Date sub-folder** | YYYYMMDD (UTC)                           | Batch isolation; watermark alignment.       |
| **File naming**  | <source>_<YYYYMMDD>_<HHMM>.(csv\|json)      | Unique, sortable.                           |
| **Retention**    | Keep 30 days → archive to \\archive\landing\| Storage hygiene.                            |
| **Security**     | ACL: read/write = svc_etl; deny others.     | Prevents accidental tampering.              |
| **Validation**   | Schema-linted vs Data-Spec v3.3.1.md.       | Early fail if columns drift.                |
| **Next hop**     | External tables read from dated folder.       | Keeps staging logic simple.                 |

> **Updated:** 2025-07-25 – initial creation per S-001b.
