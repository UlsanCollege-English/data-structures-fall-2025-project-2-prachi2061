# tests/test_cli_protocol.py
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'src' / 'app.py'
RES = ROOT / 'tests' / 'resources' / 'small_words.csv'

PYTHON = sys.executable

def run_cli(commands):
    p = subprocess.Popen(
        [PYTHON, str(APP)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = p.communicate(commands)
    if err:
        print("STDERR:", err)
    return out.strip().splitlines(), err.strip()

def test_cli_load_contains_complete_and_quit():
    assert RES.exists(), f"Resource file not found: {RES}"

    cmds = f"""
load {RES}
contains hello
complete he 3
quit
"""
    out, err = run_cli(cmds)
    assert len(out) >= 2, f"Expected at least 2 lines of output, got {len(out)}. STDERR: {err}"
    assert out[0] in ("YES", "NO"), f"Unexpected contains result: {out[0]}"
    assert out[1] == 'hello,help,hell', f"Unexpected complete result: {out[1]}"

def test_cli_remove_and_stats():
    assert RES.exists(), f"Resource file not found: {RES}"

    cmds = f"""
load {RES}
remove zebra
stats
quit
"""
    out, err = run_cli(cmds)
    assert len(out) >= 2, f"Expected at least 2 lines of output, got {len(out)}. STDERR: {err}"
    assert out[0] in ("OK", "MISS"), f"Unexpected remove result: {out[0]}"
    assert out[1].startswith('words=') and 'height=' in out[1] and 'nodes=' in out[1], f"Unexpected stats format: {out[1]}"
