# Q‑013 Atomic Tests

| Test | Expected | Result | Key Output |
|---|---|---|---|
| T1 env‑mount | `/mnt/data` lists project files | ? | list of files |
| T2 read‑check | open 256 chars succeeds | ? | sample content |
| T3 name‑audit | no spaces/non‑ASCII | ? | offending names |
| T4 drive‑list | files visible by folder ID | ? | file count |
| T5 import‑copy | files copied to `/mnt/data/drive-import/` | ? | destination paths |