#!/usr/bin/env python3
"""Live pilot: does a real Claude Code agent, with the connector skill installed, actually consult the
library, and does it do so efficiently (one search, one or two fetches, cites the id)?

Runs `claude -p` headlessly per task with tools locked to the connector script only, parses the
stream-json transcript, and reports per task: finds, gets, whether a skill id was cited, and for
negative controls whether it (correctly) left the library alone.

    python connector/eval/live_pilot.py [--model sonnet] [--tasks connector/eval/pilot_tasks.json]

Needs the connector installed (~/.claude/skills/wavefront-skills) and WAVEFRONT_SKILLS_LOCAL or a key.
Prompts say "plan only" and tools are restricted, so the agent cannot touch anything real.

Results so far (9 Nov 2026, Sonnet): with the skill loaded and no hook, 0/6 expert tasks consulted the
library (0/3 with natural phrasing too); 3/3 controls correctly left it alone. The description trigger is
advisory and the model answers from memory. Limitation: `claude -p` does not fire UserPromptSubmit hooks
(verified: only SessionStart hook events appear in the stream, with the prompt as an argument or on stdin),
so this harness cannot measure prompt_hook.py; test the hook in an interactive session. Other installed
hooks (persona or style plugins) also run in these sessions and may suppress tool use.
"""
import argparse, json, os, re, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
ID_RE = re.compile(r"\b[a-z][a-z0-9-]+\.[a-z][a-z0-9-]+\.[a-z][a-z0-9-]+\.[a-z0-9][a-z0-9-]+\b")  # category.field.product.name


def run_task(prompt, model, max_turns, cwd):
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "stream-json", "--verbose",
           "--max-turns", str(max_turns), "--permission-mode", "default",
           "--allowedTools", "Bash(python *skills.py*)"]
    t0 = time.time()
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=420, shell=(os.name == "nt"))
    finds = gets = 0; denied = 0; final = ""
    for line in p.stdout.splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "assistant":
            for blk in ev.get("message", {}).get("content", []):
                if blk.get("type") == "tool_use":
                    c = json.dumps(blk.get("input", {}))
                    if "skills.py" in c and " find" in c: finds += 1
                    elif "skills.py" in c and " get" in c: gets += 1
                    else: denied += 1  # tried something outside the allowlist
        elif ev.get("type") == "result":
            final = ev.get("result", "") or ""
    return {"finds": finds, "gets": gets, "other_tool_calls": denied, "cited": sorted(set(ID_RE.findall(final))),
            "secs": round(time.time() - t0), "exit": p.returncode, "final_head": final[:160].replace("\n", " "),
            "stderr_tail": p.stderr[-200:].replace("\n", " ") if p.returncode else ""}


def main():
    a = argparse.ArgumentParser(); a.add_argument("--model", default="sonnet"); a.add_argument("--max-turns", type=int, default=10)
    a.add_argument("--tasks", default=os.path.join(HERE, "pilot_tasks.json")); a.add_argument("--only", type=int, default=0)
    args = a.parse_args()
    tasks = json.load(open(args.tasks, encoding="utf-8"))[: args.only or None]
    cwd = tempfile.mkdtemp(prefix="wf-pilot-")  # clean dir: no project CLAUDE.md or project skills
    rows = []
    for t in tasks:
        r = run_task(t["prompt"], args.model, args.max_turns, cwd); r.update(kind=t["kind"], prompt=t["prompt"]); rows.append(r)
        # With the prompt hook installed the search happens outside the agent, so a fetch or a cited id is the signal.
        used = r["finds"] or r["gets"] or r["cited"]
        ok = (not used) if t["kind"] == "nofire" else (used and r["gets"] <= 2 and r["finds"] <= 2)
        print(f"{'PASS' if ok else 'FAIL'} [{t['kind']:6}] finds={r['finds']} gets={r['gets']} other={r['other_tool_calls']} "
              f"cited={len(r['cited'])} {r['secs']}s | {t['prompt'][:70]}", flush=True)
        if r["exit"]: print("      exit", r["exit"], r["stderr_tail"])
    fire = [r for r in rows if r["kind"] == "fire"]; nofire = [r for r in rows if r["kind"] == "nofire"]
    called = sum(1 for r in fire if r["finds"] or r["gets"])
    print(f"\ncall rate on tasks that should use it: {called}/{len(fire)}")
    print(f"efficient (<=2 finds, <=2 gets) among those: {sum(1 for r in fire if (r['finds'] or r['gets']) and r['finds'] <= 2 and r['gets'] <= 2)}/{called or 1}")
    print(f"cited a skill id: {sum(1 for r in fire if r['cited'])}/{len(fire)}")
    print(f"left alone on controls: {sum(1 for r in nofire if not (r['finds'] or r['gets']))}/{len(nofire)}")
    out = os.path.join(HERE, "last_pilot.json"); json.dump(rows, open(out, "w"), indent=1); print("details:", out)


if __name__ == "__main__":
    main()
