import json, subprocess, sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
script = root / "skills" / "visual-commands" / "scripts" / "compile_commands.py"

def run(s):
    p = subprocess.run([sys.executable, str(script), s], capture_output=True, text=True, check=True)
    return json.loads(p.stdout)

def test_known():
    r = run("/xray /cinematic /night")
    assert not r["unknown"]
    assert [x["name"] for x in r["commands"]] == ["xray","cinematic","night"]

def test_alias():
    r = run("/360 /blackbg")
    assert r["commands"][0]["name"] == "360view"

def test_param():
    r = run("/remove red chair /night")
    assert r["commands"][0]["parameter"] == "red chair"

if __name__ == "__main__":
    test_known(); test_alias(); test_param()
    print("All tests passed.")
