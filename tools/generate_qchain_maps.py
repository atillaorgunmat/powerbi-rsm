from pathlib import Path
import yaml
import xml.sax.saxutils as sax

# ---------- config ----------
ROOT = Path(__file__).resolve().parents[1]           # repo root
Q_ROOT = ROOT / "docs" / "Q_Chain"
OUT_DIR = ROOT / "docs" / "Project" / "mindmaps"
Q_GLOBS = ("q/**/*.yaml", "q/*.yaml", "*.yaml")

# ---------- helpers ----------
def _first(lst):
    return lst[0] if lst else None

def _derive_module(tags, explicit):
    # tag-first: take first tag of form mod:NAME
    if isinstance(tags, list):
        for t in tags:
            if isinstance(t, str) and t.startswith("mod:"):
                return t.split(":", 1)[1].strip() or "misc"
    if explicit:
        return explicit
    return "misc"

def _norm_list(x):
    if not x:
        return []
    if isinstance(x, list):
        return [v for v in x if v]
    return [x]

def _norm_id(x):
    return (x or "").strip()

def _label(n):
    return (n.get("title") or n.get("text") or n["id"])

def _esc_mm_text(s: str) -> str:
    # Mermaid mindmap is sensitive to [] and {} tokens
    return (s or "").replace("[","(").replace("]",")").replace("{","(").replace("}",")")

def _node_base(d: dict, ntype: str) -> dict:
    nid = _norm_id(d.get("id"))
    if not nid:
        raise ValueError("node missing id")
    tags = d.get("tags") or []
    mod = _derive_module(tags, d.get("module"))
    out = {
        "id": nid,
        "type": ntype,                     # 'q', 'a', 'e'
        "title": d.get("title") or "",
        "text":  d.get("text")  or "",
        "tags":  tags if isinstance(tags, list) else [],
        "module": mod,
        "component": d.get("component") or "",
        "status": d.get("status") or "",
        "decision_importance": d.get("decision_importance") or "",
        "depends": _norm_list(d.get("depends")),
        "what": _norm_list(d.get("what")),
    }
    # parent support (turn parent into a dependency as well)
    parent = _norm_id(d.get("parent"))
    if parent:
        out["parent"] = parent
        if parent not in out["depends"]:
            out["depends"].append(parent)
    return out

# ---------- loaders ----------
def load_questions():
    nodes = []
    for pat in Q_GLOBS:
        for p in sorted((Q_ROOT / "").glob(pat)):
            if not p.is_file():
                continue
            try:
                docs = list(yaml.safe_load_all(p.read_text(encoding="utf-8")))
            except Exception:
                continue
            for doc in docs:
                if not doc:
                    continue
                if isinstance(doc, dict) and isinstance(doc.get("questions"), list):
                    for q in doc["questions"]:
                        try:
                            nodes.append(_node_base(q, "q"))
                        except Exception:
                            pass
                elif isinstance(doc, list):
                    for q in doc:
                        try:
                            nodes.append(_node_base(q, "q"))
                        except Exception:
                            pass
                elif isinstance(doc, dict) and _norm_id(doc.get("id")):
                    try:
                        nodes.append(_node_base(doc, "q"))
                    except Exception:
                        pass
    # de-dup by id (last wins)
    uniq = {}
    for n in nodes:
        uniq[n["id"]] = n
    return list(uniq.values())

def _load_listish(file_path, root_key):
    p = file_path
    if not p.exists():
        return []
    out = []
    try:
        docs = list(yaml.safe_load_all(p.read_text(encoding="utf-8")))
    except Exception:
        return out
    for doc in docs:
        if not doc:
            continue
        if isinstance(doc, dict) and isinstance(doc.get(root_key), list):
            out.extend([d for d in doc[root_key] if isinstance(d, dict)])
        elif isinstance(doc, list):
            out.extend([d for d in doc if isinstance(d, dict)])
        elif isinstance(doc, dict) and _norm_id(doc.get("id")):
            out.append(doc)
    return out

def load_assumptions():
    raw = _load_listish(Q_ROOT / "assumptions" / "manifest.yaml", "assumptions")
    nodes = []
    for a in raw:
        try:
            n = _node_base(a, "a")
            if "module" not in a and "tags" not in a:
                # default module for assumptions (if completely untagged)
                n["module"] = "assumptions"
            nodes.append(n)
        except Exception:
            pass
    return nodes

def load_errors():
    raw = _load_listish(Q_ROOT / "errors" / "errors.yaml", "errors")
    nodes = []
    for e in raw:
        try:
            n = _node_base(e, "e")
            if "module" not in e and "tags" not in e:
                n["module"] = "errors"
            nodes.append(n)
        except Exception:
            pass
    return nodes

# ---------- outputs ----------
def mermaid_mindmap(all_nodes):
    # Only Q-nodes in the mindmap (keeps it readable)
    q_nodes = [n for n in all_nodes if n["type"] == "q"]
    by_mod = {}
    for n in q_nodes:
        by_mod.setdefault(n["module"], []).append(n)
    lines = ["```mermaid", "mindmap", "  root((Q-Chain))"]
    for mod, qs in sorted(by_mod.items()):
        lines.append(f"    {_esc_mm_text(mod)}")
        for q in sorted(qs, key=lambda x: x["id"]):
            title = _esc_mm_text(_label(q))
            lines.append(f"      {q['id']}[{q['id']} — {title}]")
            if q.get("status"):
                lines.append(f"        status: {_esc_mm_text(q['status'])}")
    lines.append("```")
    return "\n".join(lines)

def mermaid_deps(all_nodes):
    lines = ["```mermaid", "flowchart TB"]
    # Nodes (use <br/> line break for GitHub Mermaid)
    for n in all_nodes:
        title = _label(n).replace('"','\\"')
        lines.append(f'  {n["id"]}["{n["id"]}<br/>{title}"]')
    # Clusters by module
    by_mod = {}
    for n in all_nodes:
        key = (n.get("module") or "misc")
        by_mod.setdefault(key, []).append(n["id"])
    for mod, ids in sorted(by_mod.items()):
        safe = (mod or "misc").replace('"','\\"')
        lines.append(f'  subgraph "{safe}"')
        for nid in sorted(ids):
            lines.append(f"    {nid}")
        lines.append("  end")
    # Edges (depends)
    index = {n["id"]: n for n in all_nodes}
    for n in all_nodes:
        for d in (n.get("depends") or []):
            if d in index:
                lines.append(f"  {d} --> {n['id']}")
    # Styling for assumptions and errors
    a_ids = [n["id"] for n in all_nodes if n["type"] == "a"]
    e_ids = [n["id"] for n in all_nodes if n["type"] == "e"]
    if a_ids:
        lines.append("  classDef assumption stroke-dasharray:3 3,stroke-width:2;")
        lines.append(f"  class {' '.join(a_ids)} assumption;")
    if e_ids:
        lines.append("  classDef error stroke:#b00,stroke-width:2,fill:#fee;")
        lines.append(f"  class {' '.join(e_ids)} error;")
    lines.append("```")
    return "\n".join(lines)

def freemind(all_nodes):
    # Only Q nodes, grouped by module
    q_nodes = [n for n in all_nodes if n["type"] == "q"]
    by_mod = {}
    for n in q_nodes:
        by_mod.setdefault(n["module"], []).append(n)
    def node(text, children=None):
        attrs = f'TEXT="{sax.escape(text)}"'
        return f"<node {attrs}/>" if not children else f"<node {attrs}>" + "".join(children) + "</node>"
    modules_xml = []
    for mod, qs in sorted(by_mod.items()):
        q_nodes_xml = []
        for q in sorted(qs, key=lambda x: x["id"]):
            capsule = " | ".join([
                f"ID:{q['id']}",
                f"T:{_label(q)}",
                f"Tags:{','.join(q.get('tags',[])) or '—'}",
                f"Depends:{','.join(q.get('depends',[])) or '—'}",
            ])
            children = [node(f"- {w}") for w in (q.get("what") or [])]
            q_nodes_xml.append(node(capsule, children))
        modules_xml.append(node(mod, q_nodes_xml))
    return f'<?xml version="1.0" encoding="UTF-8"?><map version="1.0.1">{node("Q-Chain", modules_xml)}</map>'

def main():
    q = load_questions()
    a = load_assumptions()
    e = load_errors()
    nodes = q + a + e
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "qchain_mindmap.md").write_text(mermaid_mindmap(nodes), encoding="utf-8")
    (OUT_DIR / "qchain_dependencies.md").write_text(mermaid_deps(nodes), encoding="utf-8")
    (OUT_DIR / "qchain.mm").write_text(freemind(nodes), encoding="utf-8")
    print(f"[ok] wrote mindmaps to {OUT_DIR} (nodes={len(nodes)})")

if __name__ == "__main__":
    main()
