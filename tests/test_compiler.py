import json
import re
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
script = root / "skills" / "visual-commands" / "scripts" / "compile_commands.py"
registry = root / "skills" / "visual-commands" / "references" / "commands.json"

VALID_CATEGORIES = {
    "action",
    "background",
    "camera",
    "composition",
    "environment",
    "fidelity",
    "layout",
    "lighting",
    "look",
    "material",
    "optics",
    "output",
    "transform",
}

VALID_MODES = {"modifier", "master"}

def run(s: str) -> dict:
    p = subprocess.run([sys.executable, str(script), s], capture_output=True, text=True, check=True)
    return json.loads(p.stdout)

def test_known():
    r = run("/xray /cinematic /night")
    assert not r["unknown"]
    assert [x["name"] for x in r["commands"]] == ["xray", "cinematic", "night"]
    assert all(x["active"] for x in r["commands"])

def test_alias():
    r = run("/360 /blackbg")
    assert r["commands"][0]["raw"] == "360"
    assert r["commands"][0]["name"] == "360view"
    assert r["commands"][0]["active"]
    assert r["commands"][1]["name"] == "blackbg"
    assert r["commands"][1]["active"]
    assert r["masters"] == ["360view"]

def test_param():
    r = run("/remove red chair /night")
    assert r["commands"][0]["name"] == "remove"
    assert r["commands"][0]["parameter"] == "red chair"
    assert r["commands"][0]["active"]
    assert r["commands"][1]["name"] == "night"
    assert r["commands"][1]["parameter"] == ""
    assert r["commands"][1]["active"]

def test_environment_conflict():
    r = run("/day /night")
    assert [x["name"] for x in r["commands"]] == ["day", "night"]
    assert not r["commands"][0]["active"], "/day should be inactive"
    assert r["commands"][1]["active"], "/night should be active"

def test_background_conflict():
    r = run("/blackbg /whitebg")
    assert [x["name"] for x in r["commands"]] == ["blackbg", "whitebg"]
    assert not r["commands"][0]["active"], "/blackbg should be inactive"
    assert r["commands"][1]["active"], "/whitebg should be active"

def test_camera_conflict():
    r = run("/frontview /rearview")
    assert [x["name"] for x in r["commands"]] == ["frontview", "rearview"]
    assert not r["commands"][0]["active"], "/frontview should be inactive"
    assert r["commands"][1]["active"], "/rearview should be active"

def test_output_ratio_conflict():
    r = run("/9:16 /16:9")
    assert [x["name"] for x in r["commands"]] == ["9:16", "16:9"]
    assert not r["commands"][0]["active"], "/9:16 should be inactive"
    assert r["commands"][1]["active"], "/16:9 should be active"

def test_additive_environment():
    r = run("/night /rain /fog")
    assert [x["name"] for x in r["commands"]] == ["night", "rain", "fog"]
    assert all(x["active"] for x in r["commands"]), "Additive environment commands should all remain active"

def test_master_and_modifiers():
    r = run("/360view /productshot /blackbg")
    assert [x["name"] for x in r["commands"]] == ["360view", "productshot", "blackbg"]
    assert all(x["active"] for x in r["commands"])
    assert r["masters"] == ["360view"]

def test_registry_integrity():
    assert registry.exists(), "commands.json not found"
    data = json.loads(registry.read_text(encoding="utf-8"))
    cmds = data.get("commands", [])
    assert len(cmds) == 322, f"Expected 322 commands, found {len(cmds)}"
    
    names = [c.get("name") for c in cmds]
    assert len(names) == len(set(names)), "Duplicate command names found in commands.json"
    
    aliases = {}
    for c in cmds:
        name = c.get("name")
        assert name and isinstance(name, str), f"Invalid command name: {name}"
        assert c.get("category") in VALID_CATEGORIES, f"Invalid category in command {name}: {c.get('category')}"
        assert c.get("mode") in VALID_MODES, f"Invalid mode in command {name}: {c.get('mode')}"
        
        conflicts = c.get("conflicts")
        assert isinstance(conflicts, list), f"Conflicts in command {name} must be a list"
        for conf in conflicts:
            assert isinstance(conf, str) and conf.strip(), f"Invalid conflict entry in command {name}: {conf}"
            
        args = c.get("args")
        assert isinstance(args, str), f"Args in command {name} must be a string"

        for a in c.get("aliases", []):
            assert a not in aliases, f"Duplicate alias {a}"
            aliases[a] = name
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
    test_environment_conflict()
    test_background_conflict()
    test_camera_conflict()
    test_output_ratio_conflict()
    test_additive_environment()
    test_master_and_modifiers()
    test_registry_integrity()
    print("All tests passed.")
