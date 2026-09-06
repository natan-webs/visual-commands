#!/usr/bin/env python3
"""Compile Visual Commands slash syntax into a normalized plan.
This helper does not generate images. Codex may use it for deterministic parsing/debugging.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

REGISTRY = Path(__file__).resolve().parents[1] / "references" / "commands.json"

def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))

def has_conflict(cmd_a: dict, cmd_b: dict) -> bool:
    """Return True if cmd_a and cmd_b are mutually exclusive according to registry conflict metadata."""
    conf_a = set(cmd_a.get("conflicts", []))
    conf_b = set(cmd_b.get("conflicts", []))
    
    # Explicit conflict by command name
    if cmd_a["name"] in conf_b or cmd_b["name"] in conf_a:
        return True
    
    # Shared conflict group (e.g. camera_single, output_ratio, background_replace)
    if conf_a and conf_b and bool(conf_a & conf_b):
        return True
        
    return False

def parse(text: str) -> dict:
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
            "conflicts": cmd.get("conflicts", []) if cmd else [],
            "args": cmd.get("args", "") if cmd else "",
        })

    # Resolve mutually exclusive commands based on registry conflict definitions:
    # Later explicit command wins by shadowing earlier conflicting commands.
    shadowed = set()
    for idx, item in enumerate(items):
        if not item["known"]:
            continue
        for j in range(idx):
            if items[j]["known"] and j not in shadowed:
                if has_conflict(items[j], item):
                    shadowed.add(j)

    resolved = []
    for idx, item in enumerate(items):
        item_dict = dict(item)
        item_dict["active"] = idx not in shadowed
        resolved.append(item_dict)

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
