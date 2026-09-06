import json
import re
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
script = root / "skills" / "visual-commands" / "scripts" / "compile_commands.py"
registry = root / "skills" / "visual-commands" / "references" / "commands.json"

def run(s):
    p = subprocess.run([sys.executable, str(script), s], capture_output=True, text=True, check=True)
    return json.loads(p.stdout)

def test_known():
    r = run("/xray /cinematic /night")
    assert not r["unknown"]
    assert [x["name"] for x in r["commands"]] == ["xray", "cinematic", "night"]

def test_alias():
    r = run("/360 /blackbg")
    assert r["commands"][0]["name"] == "360view"

def test_param():
    r = run("/remove red chair /night")
    assert r["commands"][0]["parameter"] == "red chair"

def test_registry_integrity():
    assert registry.exists(), "commands.json not found"
    data = json.loads(registry.read_text(encoding="utf-8"))
    cmds = data.get("commands", [])
    assert len(cmds) == 322, f"Expected 322 commands, found {len(cmds)}"
    
    names = [c.get("name") for c in cmds]
    assert len(names) == len(set(names)), "Duplicate command names found in commands.json"
    
    aliases = {}
    for c in cmds:
        for a in c.get("aliases", []):
            assert a not in aliases, f"Duplicate alias {a}"
            aliases[a] = c.get("name")
            assert a not in set(names), f"Alias {a} collides with command name"

    # Check relative links in markdown documentation
    for md in root.rglob("*.md"):
        if ".git" in md.parts:
            continue
        content = md.read_text(encoding="utf-8")
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
        for label, target in links:
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            clean_target = target.split("#")[0]
            if clean_target:
                resolved = (md.parent / clean_target).resolve()
                assert resolved.exists(), f"Broken link in {md}: [{label}]({target}) -> {resolved}"

    # Check that all commands in README examples exist in commands.json
    readme_text = (root / "README.md").read_text(encoding="utf-8")
    readme_slash_cmds = set(re.findall(r"(?<!\S)/([A-Za-z0-9_:-]+)", readme_text))
    cmd_set = set(names) | set(aliases.keys())
    for c in readme_slash_cmds:
        assert c in cmd_set, f"README mentions unverified command: /{c}"

if __name__ == "__main__":
    test_known()
    test_alias()
    test_param()
    test_registry_integrity()
    print("All tests passed.")
