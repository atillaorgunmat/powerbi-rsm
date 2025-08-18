#!/usr/bin/env python3
from pathlib import Path
import yaml
import xml.sax.saxutils as sax

# ---------- config ----------
ROOT = Path(__file__).resolve().parents[1]          # repo root
Q_DIR = ROOT / "docs" / "Q_Chain"
OUT_DIR = ROOT / "docs" / "Project" / "mindmaps"
Q_GLOB = ("q/**/*.yaml", "q/*.yaml", "*.yaml")

# ---------- helpers ----------
def _normalize_node(d: dict) -> dict:
    if not isinstance(d, dict):
        raise ValueError("node is not a dict")
    nid = (d.get("id") or "").strip()
    if not nid:
        raise ValueError("node missing id")
    return {
        "id": nid,
        "title": d.get("title") or "",
        "text": d.get("text") or "",
        "module": d.get("module") or "misc",
        "component": d.get("component") or "",
        "status": d.get("status") or "",
        "decision_importance": d.get("decision_importance") or "",
        "block_on_dep": bool(d.get("block_on_dep", False)),
        "depends": [x for x in (d.get("depends") or []) if x],
        "what": [x for x in (d.get("what") or []) if x],
    }

def _skip(path: Path) -> bool:
    parts = set(path.parts)
    if 'archive' in parts: return True
    if path.name.endswith('.legacy.yaml'): return True
    return False

def load_all_qnodes():
    """Load Q-nodes from shard files (supports: list-root, {questions: [...]}, or single object)."""
    nodes = []
    for pat in Q_GLOB:
        for p in sorted(Q_DIR.glob(pat)):
            if _skip(p) or not p.is_file():
                continue
            try:
                docs = list(yaml.safe_load_all(p.read_text(encoding="utf-8")))
            except Exception:
                continue
            for doc in docs:
                if not doc:
                    continue
                # shard style: { questions: [...] }
                if isinstance(doc, dict) and isinstance(doc.get("questions"), list):
                    for q in doc["questions"]:
                        try:
                            nodes.append(_normalize_node(q))
                        except Exception:
                            pass
                # list-root: [ {...}, {...} ]
                elif isinstance(doc, list):
                    for q in doc:
                        try:
                            nodes.append(_normalize_node(q))
                        except Exception:
                            pass
                # single object
                elif isinstance(doc, dict):
                    try:
                        nodes.append(_normalize_node(doc))
                    except Exception:
                        pass
    # de-dup by id
    uniq = {}
    for n in nodes:
        uniq[n["id"]] = n
    return list(uniq.values())

def _label(n: dict) -> str:
    return (n.get("title") or n.get("text") or n["id"])

def _esc_mm(s: str) -> str:
    # Mermaid mindmap is sensitive to [] and {}
    return (s or "").replace("[","(").replace("]",")").replace("{","(").replace("}",")")

# ---------- outputs ----------
def mermaid_mindmap(nodes):
    by_mod = {}
    for n in nodes:
        by_mod.setdefault(n["module"], []).append(n)
    lines = ["```mermaid", "mindmap", "  root((Q-Chain))"]
    for mod, qs in sorted(by_mod.items()):
        lines.append(f"    {_esc_mm(mod)}")
        for q in sorted(qs, key=lambda x: x["id"]):
            title = _esc_mm(_label(q))
            lines.append(f"      {q['id']}[{q['id']} — {title}]")
            if q.get("status"):
                lines.append(f"        status: {_esc_mm(q['status'])}")
    lines.append("```")
    return "\n".join(lines)

def mermaid_deps(nodes):
    lines = ["```mermaid", "flowchart TB"]
    # nodes with <br/> for GitHub Mermaid line-break
    for n in nodes:
        title = _label(n).replace('"','\\"')
        lines.append(f'  {n["id"]}["{n["id"]}<br/>{title}"]')
    # cluster by module
    by_mod = {}
    for n in nodes:
        key = (n.get("module") or "misc")
        by_mod.setdefault(key, []).append(n["id"])
    for mod, ids in sorted(by_mod.items()):
        safe = (mod or "misc").replace('"','\\"')
        lines.append(f'  subgraph "{safe}"')
        for qid in sorted(ids):
            lines.append(f"    {qid}")
        lines.append("  end")
    # edges
    for n in nodes:
        for d in (n.get("depends") or []):
            lines.append(f"  {d} --> {n['id']}")
    lines.append("```")
    return "\n".join(lines)

def freemind(nodes):
    by_mod = {}
    for n in nodes:
        by_mod.setdefault(n["module"], []).append(n)
    def node(text, children=None):
        attrs = f'TEXT="{sax.escape(text)}"'
        return f"<node {attrs}/>" if not children else f"<node {attrs}>" + "".join(children) + "</node>"
    modules_xml = []
    for mod, qs in sorted(by_mod.items()):
        q_nodes = []
        for q in sorted(qs, key=lambda x: x["id"]):
            capsule = " | ".join([
                f"ID:{q['id']}",
                f"T:{_label(q)}",
                f"C:{q.get('component','')}",
                f"S:{q.get('status','')}",
                f"D:{q.get('decision_importance','')}",
                f"Depends:{','.join(q.get('depends',[])) or '—'}",
            ])
            children = [node(f"- {w}") for w in (q.get("what") or [])]
            q_nodes.append(node(capsule, children))
        modules_xml.append(node(mod, q_nodes))
    return f'<?xml version="1.0" encoding="UTF-8"?><map version="1.0.1">{node("Q-Chain", modules_xml)}</map>'

def main():
    nodes = load_all_qnodes()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "qchain_mindmap.md").write_text(mermaid_mindmap(nodes), encoding="utf-8")
    (OUT_DIR / "qchain_dependencies.md").write_text(mermaid_deps(nodes), encoding="utf-8")
    (OUT_DIR / "qchain.mm").write_text(freemind(nodes), encoding="utf-8")
    print(f"[ok] wrote mindmaps to {OUT_DIR} (nodes={len(nodes)})")

if __name__ == "__main__":
    main()
