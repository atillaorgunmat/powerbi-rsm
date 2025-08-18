#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
Q_DIR = ROOT / "docs" / "Q_Chain" / "q"
SRC = Q_DIR / "Q-ROOT.yaml"

def load_all(doc_text):
    docs = list(yaml.safe_load_all(doc_text))
    items = []
    for d in docs:
        if not d:
            continue
        if isinstance(d, dict) and isinstance(d.get("questions"), list):
            items.extend([x for x in d["questions"] if isinstance(x, dict)])
        elif isinstance(d, list):
            items.extend([x for x in d if isinstance(x, dict)])
        elif isinstance(d, dict) and d.get("id"):
            items.append(d)
    return items

def write_shard(mod, items):
    shard = Q_DIR / f"{mod}.yaml"
    existing = []
    if shard.exists():
        try:
            d = yaml.safe_load(shard.read_text(encoding="utf-8")) or {}
            if isinstance(d, dict) and isinstance(d.get("questions"), list):
                existing = [x for x in d["questions"] if isinstance(x, dict)]
        except Exception:
            pass
    by_id = {}
    for x in existing + items:
        idx = (x.get("id") or "").strip()
        if idx:
            by_id[idx] = x
    out = {"questions": [by_id[k] for k in sorted(by_id.keys())]}
    shard.write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"[ok] wrote shard {shard} (questions={len(out['questions'])})")

def main():
    if not SRC.exists():
        print(f"[warn] {SRC} not found; nothing to split")
        return
    Q_DIR.mkdir(parents=True, exist_ok=True)
    nodes = load_all(SRC.read_text(encoding="utf-8"))
    buckets = {}
    for q in nodes:
        mid = (q.get("module") or "misc")
        buckets.setdefault(mid, []).append(q)
    for mod, items in sorted(buckets.items()):
        write_shard(mod, items)
    # archive original
    arch = Q_DIR / "archive"
    arch.mkdir(exist_ok=True, parents=True)
    SRC.rename(arch / "Q-ROOT.legacy.yaml")
    print(f"[ok] archived original to {arch/'Q-ROOT.legacy.yaml'}")

if __name__ == "__main__":
    main()
