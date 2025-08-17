#!/usr/bin/env python3
# Reads docs/Q_Chain/**.yaml (shards) and generates:
#   - docs/Project/mindmaps/qchain_mindmap.md (Mermaid mindmap w/ features)
#   - docs/Project/mindmaps/qchain_dependencies.md (Mermaid depends graph)
#   - docs/Project/mindmaps/qchain.mm (FreeMind)
import sys, yaml, pathlib, xml.sax.saxutils as sax

ROOT = pathlib.Path(__file__).resolve().parents[1]
Q_DIR = ROOT / "docs" / "Q_Chain"
OUT_DIR = ROOT / "docs" / "Project" / "mindmaps"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_all_qnodes():
    nodes = []
    if not Q_DIR.exists():
        print(f"[WARN] {Q_DIR} missing", file=sys.stderr); return nodes
    # scan all .yaml under docs/Q_Chain/ (supports shards like q/*.yaml)
    for y in Q_DIR.rglob("*.yaml"):
        try:
            data = yaml.safe_load(y.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[WARN] failed to parse {y}: {e}", file=sys.stderr); continue
        if isinstance(data, list):
            # assume list of question nodes
            for n in data:
                node = {
                    "id": (n.get("id") or "").strip(),
                    "title": (n.get("title") or n.get("text") or "").strip(),
                    "module": n.get("module","misc"),
                    "component": n.get("component",""),
                    "why": (n.get("why") or "").strip(),
                    "what": n.get("what") or [],
                    "assumptions": n.get("assumptions") or [],
                    "errors": n.get("errors") or [],
                    "tests": n.get("tests") or [],
                    "owners": [o.get("handle") if isinstance(o, dict) and "handle" in o else str(o) for o in (n.get("owners") or [])],
                    "depends": n.get("depends") or [],
                    "status": n.get("status","proposed"),
                    "decision_importance": n.get("decision_importance","medium"),
                    "block_on_dep": bool(n.get("block_on_dep", False)),
                }
                if node["id"]:
                    nodes.append(node)
    # de-dupe by id (keep last seen)
    uniq = {}
    for n in nodes:
        uniq[n["id"]] = n
    return list(uniq.values())

def mermaid_mindmap(nodes):
    lines = ["```mermaid", "mindmap", "  root((Q-Chain))"]
    by_mod = {}
    for n in nodes:
        by_mod.setdefault(n["module"], []).append(n)
    for mod, qs in sorted(by_mod.items()):
        lines.append(f"  {mod}")
        for q in qs:
            lines.append(f"    {q['id']}[{(q['title'] or q['id']).replace('[','(').replace(']',')')}]")
            lines.append(f"      status: {q['status']}")
            if q.get("component"): lines.append(f"      component: {q['component']}")
            if q.get("why"): lines.append(f"      why: {q['why']}")
            if q.get("what"):
                lines.append("      what")
                for w in q["what"]:
                    lines.append(f"        - {w}")
            if q.get("assumptions"):
                lines.append("      assumptions")
                for a in q["assumptions"]:
                    lines.append(f"        - {a}")
            if q.get("errors"):
                lines.append("      errors")
                for e in q["errors"]:
                    lines.append(f"        - {e}")
            if q.get("tests"):
                lines.append("      tests")
                for t in q["tests"]:
                    lines.append(f"        - {t}")
            if q.get("owners"):
                lines.append("      owners")
                for o in q["owners"]:
                    lines.append(f"        - {o}")
            lines.append(f"      decision: {q['decision_importance']}")
            lines.append(f"      block_on_dep: {str(q['block_on_dep']).lower()}")
    lines.append("```")
    return "\n".join(lines)

def mermaid_deps(nodes):
    lines = ["```mermaid", "flowchart TD"]
    for n in nodes:
        title = (n['title'] or n['id']).replace('"','\\"')
        lines.append(f'  {n["id"]}["{n["id"]}\\n{title}"]')
    for n in nodes:
        for d in n.get("depends", []):
            lines.append(f"  {d} --> {n['id']}")
    lines.append("```")
    return "\n".join(lines)

def freemind(nodes):
    by_mod = {}
    for n in nodes:
        by_mod.setdefault(n["module"], []).append(n)
    def mm_node(text, children=None):
        attrs = f'TEXT="{sax.escape(text)}"'
        return f"<node {attrs}/>" if not children else f"<node {attrs}>" + "".join(children) + "</node>"
    modules_xml = []
    for mod, qs in sorted(by_mod.items()):
        q_nodes = []
        for q in qs:
            capsule = " | ".join([
                f"ID:{q['id']}", f"T:{q['title'] or q['id']}", f"C:{q['component']}",
                f"S:{q['status']}", f"D:{q['decision_importance']}",
                f"Depends:{','.join(q['depends']) or '—'}",
            ])
            children = [mm_node(f"- {w}") for w in q.get("what",[])]
            q_nodes.append(mm_node(capsule, children))
        modules_xml.append(mm_node(mod, q_nodes))
    return f'<?xml version="1.0" encoding="UTF-8"?><map version="1.0.1">{mm_node("Q-Chain", modules_xml)}</map>'

def main():
    nodes = load_all_qnodes()
    (OUT_DIR / "qchain_mindmap.md").write_text(mermaid_mindmap(nodes), encoding="utf-8")
    (OUT_DIR / "qchain_dependencies.md").write_text(mermaid_deps(nodes), encoding="utf-8")
    (OUT_DIR / "qchain.mm").write_text(freemind(nodes), encoding="utf-8")
    print(f"[ok] wrote: {OUT_DIR}")

if __name__ == "__main__":
    main()
