#!/usr/bin/env python3
from pathlib import Path
import yaml
import xml.sax.saxutils as sax

# ---------- config ----------
ROOT = Path(__file__).resolve().parents[1]          # repo root
Q_DIR = ROOT / "docs" / "Q_Chain"
OUT_DIR = ROOT / "docs" / "Project" / "mindmaps"
Q_GLOB = ["q/*.yaml", "*.yaml", "assumptions/*.yaml", "errors/*.yaml"]

# ---------- helpers ----------
def _normalize_node(d: dict) -> dict:
    """Return a node dict with safe defaults."""
    nid = (d.get("id") or "").strip()
    if not nid:
        raise ValueError("node missing id")
    return {
        "id": nid,
        "title": d.get("title") or "",
        "module": d.get("module") or "misc",
        "component": d.get("component") or "",
        "status": d.get("status") or "",
        "decision_importance": d.get("decision_importance") or "",
        "depends": d.get("depends") or [],
        "what": d.get("what") or [],
    }

def load_all_qnodes():
    """Load questions from shard-style YAMLs or single-node YAMLs."""
    nodes = []
    for pat in Q_GLOB:
        for p in sorted(Q_DIR.glob(pat)):
            if not p.is_file():
                continue
            try:
                docs = list(yaml.safe_load_all(p.read_text(encoding="utf-8")))
            except Exception:
                # tolerate non-YAML or partially written files
                continue
            for doc in docs:
                if not doc:
                    continue
                # shard: {questions: [...]}
                if isinstance(doc, dict) and isinstance(doc.get("questions"), list):
                    for q in doc["questions"]:
                        if isinstance(q, dict) and (q.get("id") or "").strip():
                            nodes.append(_normalize_node(q))
                # single-node file
                elif isinstance(doc, dict) and (doc.get("id") or "").strip():
                    nodes.append(_normalize_node(doc))
    # de-dup by id (last one wins)
    uniq = {}
    for n in nodes:
        uniq[n["id"]] = n
    return list(uniq.values())

# ---------- outputs ----------
def mermaid_mindmap(nodes):
    # single root → avoid "There can be only one root" error
    by_mod = {}
    for n in nodes:
        by_mod.setdefault(n["module"], []).append(n)
    def esc(s: str) -> str:
        # Mermaid mindmap is picky about brackets
        return (s or "").replace("[","(").replace("]",")").replace("{","(").replace("}",")")
    lines = ["```mermaid", "mindmap", "  root((Q-Chain))"]
    for mod, qs in sorted(by_mod.items()):
        lines.append(f"    {esc(mod)}")
        for q in sorted(qs, key=lambda x: x['id']):
            title = esc(q.get("title") or q["id"])
            lines.append(f"      {q['id']}[{q['id']} — {title}]")
            if q.get("status"):
                lines.append(f"        status: {esc(q['status'])}")
    lines.append("```")
    return "\n".join(lines)

def mermaid_deps(nodes):
    # vertical layout; cluster nodes into module subgraphs
    lines = ["```mermaid", "flowchart TB"]
    for n in nodes:
        title = (n.get("title") or n["id"]).replace('"','\\"')
        lines.append(f'  {n["id"]}["{n["id"]}\\n{title}"]')
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
                f"ID:{q['id']}", f"T:{q.get('title') or q['id']}",
                f"C:{q.get('component','')}", f"S:{q.get('status','')}",
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
