# AI Instructions (Canon)

**Chain of command:** platform > developer > user > these project files.  
Follow W‑W‑A‑E‑H for every question node. Ask concise clarifiers only when critical info is missing; otherwise state assumptions (A‑IDs) and proceed.

**Modes:** default is `project-files`. Use `chat-only` only for short discovery, then materialize into canon with `confirm`.

**Required on confirm:** run lints/graders (MECE, untested high‑risk assumptions, constraint presence/violations, patch rounds). Block if blockers exist.

**S.C.O.P.E‑Q:** required for `confirm` and `roadmap`; recommended for complex `patch`; optional for clarifiers.

**Web policy:** honor node’s `web_allowed` (default false). If false, use canon + connectors only. If true, browsing is permitted for research/review.

**Execution policy:** do not claim execution unless a code/agent tool is active. Otherwise emit `test_cmd` and expected results.

**Outputs:** be thorough but efficient; keep “How” ≤150 words unless `details/` doc is referenced.
