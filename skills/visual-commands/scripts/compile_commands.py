#!/usr/bin/env python3
"""Compile Visual Commands slash syntax into a normalized plan.
This helper does not generate images. Codex may use it for deterministic parsing/debugging.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

REGISTRY = Path(__file__).resolve().parents[1] / "references" / "commands.json"

def load_registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))

def parse(text: str):
    reg = load_registry()
    by_name = {c["name"]: c for c in reg["commands"]}
    alias = {}
    for c in reg["commands"]:
        for a in c.get("aliases", []):
            alias[a] = c["name"]

    # Capture /command and its trailing parameter text until next slash command.
    matches = list(re.finditer(r'(?<!\S)/([A-Za-z0-9][A-Za-z0-9_-]*(?::[A-Za-z0-9_-]+)?)', text))
    items = []
    for i, m in enumerate(matches):
        raw = m.group(1)
        name = alias.get(raw, raw)
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        param = text[m.end():end].strip()
        cmd = by_name.get(name)
        items.append({
            "raw": raw,
            "name": name,
            "known": bool(cmd),
            "category": cmd.get("category") if cmd else None,
            "mode": cmd.get("mode") if cmd else None,
            "parameter": param,
            "description": cmd.get("description") if cmd else None,
        })

    # Resolve common single-value categories: last explicit command wins.
    last_wins_categories = {"output", "background"}
    resolved = []
    shadowed = set()

    for idx, item in enumerate(items):
        if not item["known"]:
            continue
        if item["category"] in last_wins_categories:
            for j in range(idx):
                if items[j]["known"] and items[j]["category"] == item["category"]:
                    # background can be additive only when previous isn't a replace/isolate command; conservative last-win
                    shadowed.add(j)
        # Single camera views conflict; masters do not get shadowed by simple modifiers.
        if item["category"] == "camera" and item["mode"] != "master":
            for j in range(idx):
                if items[j]["known"] and items[j]["category"] == "camera" and items[j]["mode"] != "master":
                    shadowed.add(j)

    for idx, item in enumerate(items):
        item = dict(item)
        item["active"] = idx not in shadowed
        resolved.append(item)

    return {
        "input": text,
        "commands": resolved,
        "unknown": [i["raw"] for i in resolved if not i["known"]],
        "masters": [i["name"] for i in resolved if i["known"] and i["mode"] == "master" and i["active"]],
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("text", nargs="+", help="Visual Commands string")
    args = ap.parse_args()
    print(json.dumps(parse(" ".join(args.text)), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
