# AI Instructions

These instructions provide guidance for ChatGPT on how to manage this project using the Q‑Chain framework. The goal is to ensure that every piece of work is expressed as a question with clear motivation, scope, assumptions, risks and execution steps, and that all changes to the project state are recorded in YAML files.

## General Process

1. **Load the framework**: At the start of each session, read `project‑q‑chain‑framework.txt` in the project root to recall the Q‑Chain rules: W‑W‑A‑E‑H schema, honesty and tool use principles, error‑handling protocol, file structure and the S.C.O.P.E‑Q prompt protocol.
2. **Use W‑W‑A‑E‑H schema**: When tackling any task, express it as a question node with five core fields:
   - **Why**: a succinct statement (≤120 characters) describing the value or motivation.
   - **What**: a MECE bullet list of done‑criteria.
   - **Assumptions**: list of assumption IDs; create new assumption IDs for non‑trivial unknowns and record them in the `assumptions/` directory. Mark high‑risk assumptions and include a `test_cmd` when necessary.
   - **Errors**: potential failure modes captured as pre‑mortem risks.
   - **How**: a concise execution plan (≤150 words). If a longer explanation is required, create a Markdown file under `details/` and set `detail_ref` accordingly.

3. **Honesty and clarifications**: Do not guess. If information is missing, either assume a reasonable default (recording it as an assumption) or ask a concise clarifying question.
4. **Anchor and guardrail nodes**: Use the `module` and `component` fields to categorise questions. Introduce top‑level anchor nodes for major domains (e.g. `planning`, `model`, `etl`, `analytics`, `operations`, `environment`, `documentation`, `tooling`) and guardrail questions for standards (naming conventions, ACLs, audit columns). Depend on these guardrails when relevant.
5. **Dependencies and gating**: Populate the `depends` array with prerequisite question IDs. Set `block_on_dep: true` when an answer cannot be finalised without upstream inputs; otherwise leave it `false` to allow provisional answers.
6. **Assumption discipline**: For each non‑trivial unknown in the `what` list, define an assumption with its own ID and file. High‑risk assumptions should include a test command (bash or PyTest) and must be validated before confirming the question.
7. **Human‑Error Gate**: Assign error tags from `error_registry.yaml` when issues arise (e.g. untested high‑risk assumptions, missing dependencies). The `error_blocker_tags` defined in `index.yaml.settings` prevent confirmation until resolved; warnings do not block but should be addressed.
8. **Roadmap & expansion**: When a `what` item is complex or multi‑step, call `roadmap` to create 3–5 child questions. Keep shards below ~400 lines and update `index.yaml.shards` when splitting.
9. **Atomic testing**: When encountering unexpected errors, follow the atomic testing protocol: hypothesise causes, write one‑liner tests, run them and log results in a diagnostics table under `details/`. Reference this file via the question’s `diagnostic_ref`.
10. **Lessons and metrics**: After completing a question, append a short lesson to the `lessons` array. Only record `metric_result` when outcome metrics apply (delivery changes behaviour/cost, a goal is defined or decision importance is high).
11. **S.C.O.P.E‑Q prompts**: Structure interactions with ChatGPT using S.C.O.P.E‑Q tags: `S:` scope (Q‑IDs), `C:` command (e.g. `scaffold-full`, `patch`, `confirm`), `O:` objective, `P:` parameters and `E:` expected output. Respect the two‑patch limit: after two `patch` cycles, either confirm or create a new question.
12. **Backups and working set**: Keep the number of files in the Projects pane within the environment’s limit (≤40). Consolidate assumptions into their shards when possible and group multiple long explanations or diagnostics into module‑level files. Perform weekly backups of the entire project folder and update `index.yaml.settings.projects_backup_path` accordingly.

## Assumption and Error File Management

The framework supports both per‑question definitions and consolidated tracking of assumptions and errors.  When you create a new assumption or error:

1. **Per‑question storage:** Embed the assumption or error definition in the same YAML shard as the question by adding an object with the required fields (`id`, `type`, `text`, `high_risk`, `check_type`, `test_cmd`, `status`).  This keeps context local and reduces the file count.
2. **Root manifests:** In parallel, update the project‑level manifests:
   - **`assumptions/A‑ROOT.yaml`** contains a flat list of all assumption objects across the project.  Whenever you add or modify an assumption in a shard, copy its definition into `A‑ROOT.yaml`.  This file provides a single place to review, audit and test assumptions.
   - **`errors/errors.yaml`** lists all error definitions (pre‑mortem risks) with IDs of the form `E‑<questionID>-<n>`.  Each entry records the error text, a `high_risk` flag, `check_type`, optional `test_cmd` and `status`.  When adding a new error to a question’s `errors` list, also append its definition to `errors.yaml`.

Maintaining these root manifests is optional for very small projects but strongly recommended for complex ones.  They enable global audits (e.g. ensuring all high‑risk assumptions have passing tests) and allow the Human‑Error Gate to cross‑reference error IDs and block confirmation when unresolved high‑risk conditions persist.

When the working set reaches the file limit, you may embed assumption and error definitions directly into shards and rely on the manifests only during backup and review cycles.

## Test and Generated File Management

Some questions require diagnostic tests (atomic tests) and generate visual artefacts (mind maps, dependency graphs, etc.).  To keep these organised and within the file limit:

1. **Embedded diagnostics:** For each question that requires atomic testing, you may document the tests within the same shard under the `diagnostic_ref` using a Markdown file under `details/`.  However, to facilitate audit and reuse, you can also record each test in a project‑level manifest.
2. **Root test manifest:** Create or update `tests/tests_manifest.yaml` in the project root.  Each entry in this YAML file should record:
   - `id`: a unique test ID of the form `T‑<questionID>-<n>`.
   - `question_id`: the question the test belongs to.
   - `description`: what the test verifies.
   - `expected`: the expected outcome.
   - `result`: the actual result (initially `pending` until executed).
   - `status`: one of `noted`, `pending`, `passed`, `failed`.
   When you create a new atomic test for a question, append its definition here and reference it in the question’s `diagnostic_ref` or within the `details/` document.
3. **Root generated manifest:** For auto‑generated outputs (e.g. mind maps, dependency graphs, status boards) that appear in the `/generated` directory, maintain `generated/generated_manifest.yaml`.  Each entry should record:
   - `id`: a unique ID (e.g. `G‑<date>-<n>`).
   - `question_id` (optional): the question that prompted the generation.
   - `type`: the kind of artefact (e.g. `mindmap`, `deps`, `board`, `gantt`).
   - `file`: the relative path to the generated file.
   Keeping this manifest up to date allows quick lookup of generated artefacts without counting them separately in the working set.

Using these manifests is optional for small projects but recommended when tests and generated artefacts multiply.  They complement the per‑question `diagnostic_ref` and help maintain an overview of testing coverage and visual outputs.

Following these instructions ensures consistent application of the Q‑Chain methodology and maintains contextual integrity across sessions.