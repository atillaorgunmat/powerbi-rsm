# Fact Log  (immutable, append-only)

| ID  | Date       | Fact                                                                                  |
|-----|------------|---------------------------------------------------------------------------------------|
| F01 | 2025-06-25 | Final presentation locked to **2025-08-30**                                           |
| F02 | 2025-06-25 | Source control is **local Git only** (no remote push)                                 |
| F03 | 2025-06-25 | Primary editor is **VS Code** with Markdown & GitLens extensions installed            |
| F04 | 2025-06-25 | Methodology in force: **RSM v1.0** (Reason-First Solo Methodology)                    |
| F05 | 2025-06-25 | Folder skeleton under `~/Projects/PowerBI-RSM` is frozen (changes require Governor)   |

---

## Context-Kit SOP  (Governor ritual)

1. Open latest **Plan.md** and locate current `phase:` line.  
2. Run `grep -l "State: In-Progress" tasks/*` to list open Tasks and copy IDs into JSON array.  
3. Copy the **most recent 3–5 Fact IDs** from the bottom of this log.  
4. Assemble packet in this exact order:  
