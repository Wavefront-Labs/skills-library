#!/usr/bin/env python3
"""A/B test: does the library change the quality of an agent's answer to expert tasks?

Arms (same model, same prompt, same locked-down tools, clean settings):
  A  control:  no library.
  B  product:  the hook's shortlist (top 5 candidates) in the system prompt; the agent may fetch with skills.py.
  C  ceiling:  the top two skill bodies pre-injected into the system prompt; no fetching needed.
Grading: blind pairwise judge (A vs B, A vs C) on a fixed rubric, order randomised per comparison.

    python connector/eval/ab_test.py run   --tasks T.json --out DIR [--limit N] [--arms ABC] [--model sonnet]
    python connector/eval/ab_test.py judge --tasks T.json --out DIR [--judge opus]
    python connector/eval/ab_test.py report --out DIR

Resumable: existing outputs are skipped, so run it in chunks. Needs WAVEFRONT_SKILLS_LOCAL.
"""
import argparse, concurrent.futures, json, os, random, re, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS_PY = os.path.join(HERE, "..", "wavefront-skills", "scripts", "skills.py")
CLEAN_SETTINGS = {"disableAllHooks": True, "skillOverrides": {"wavefront-skills": "off"}}  # no persona hooks, no connector skill
ID_RE = re.compile(r"\b[a-z][a-z0-9-]+\.[a-z][a-z0-9-]+\.[a-z][a-z0-9-]+\.[a-z0-9][a-z0-9-]+\b")

RUBRIC = """You are grading two answers to the same expert request. Judge ONLY the answers' quality for a competent
professional who will act on them. Criteria, in order: (1) correctness, no wrong or dangerous advice;
(2) specificity: exact commands, flags, object names, versions where they matter; (3) covers the non-obvious
traps and verification steps; (4) fits the asker's actual situation. Ignore length, tone and formatting.
Reply with JSON only: {"winner": "1" | "2" | "tie", "score1": 1-5, "score2": 1-5, "reason": "<one sentence>"}."""


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", shell=(os.name == "nt"), **kw)


def lib(*args):
    return sh([sys.executable, "-X", "utf8", SKILLS_PY, *args], timeout=60).stdout


def shortlist(prompt):
    out = lib("find", re.sub(r"\s+", " ", prompt)[:300], "-k", "5")
    return [l for l in out.splitlines() if l.strip() and not l.startswith("Wavefront Skills Library -") and not l.startswith("no match")]


def claude(prompt, model, system_extra, allow_skills, cwd, settings_file, max_turns):
    # Prompt goes on stdin: the Windows command line caps at 8K chars, and arm C carries two skill bodies.
    # Injected material rides in the same user turn, above the request, as a hook's additionalContext would.
    cmd = ["claude", "-p", "--model", model, "--output-format", "stream-json", "--verbose", "--max-turns", str(max_turns),
           "--permission-mode", "default", "--settings", settings_file,
           "--allowedTools", "Bash(python *skills.py*)" if allow_skills else "NoSuchTool"]
    text = (system_extra + "\n\n---\n\n" if system_extra else "") + prompt
    t0 = time.time(); p = sh(cmd, cwd=cwd, timeout=600, input=text)
    gets, fetched, final, usage = 0, [], "", {}
    for line in p.stdout.splitlines():
        try: ev = json.loads(line)
        except ValueError: continue
        if ev.get("type") == "assistant":
            for b in ev.get("message", {}).get("content", []):
                if b.get("type") == "tool_use":
                    c = json.dumps(b.get("input", {}))
                    if "skills.py" in c and " get " in c:
                        gets += 1; fetched += ID_RE.findall(c)
        elif ev.get("type") == "result":
            final = ev.get("result", "") or ""; usage = ev.get("usage", {}) or {}
    return {"answer": final, "gets": gets, "fetched": sorted(set(fetched)), "secs": round(time.time() - t0),
            "exit": p.returncode, "err": p.stderr[-300:] if p.returncode else "", "usage": usage}


def run(a):
    tasks = json.load(open(a.tasks, encoding="utf-8"))[: a.limit or None]
    os.makedirs(a.out, exist_ok=True)
    cwd = tempfile.mkdtemp(prefix="wf-ab-")
    settings_file = os.path.join(a.out, "clean-settings.json"); json.dump(CLEAN_SETTINGS, open(settings_file, "w"))
    get_cmd = f'python "{os.path.abspath(SKILLS_PY)}" get <id>'

    def arm(task, which):
        path = os.path.join(a.out, f"{task['id']}.{which}.json")
        if os.path.exists(path): return which, "skip"
        extra, allow = "", False
        if which == "B":
            cands = shortlist(task["prompt"])
            if not cands: return which, "no-cands"
            extra = ("Wavefront Skills Library candidates for this task (ranked). If one fits, fetch it before answering:\n  " + get_cmd +
                     "\nPrefer method over skill, verified over draft; fetch at most two; cite the id you used. If none fits, ignore this.\n" + "\n".join(cands))
            allow = True
        elif which == "C":
            cands = shortlist(task["prompt"])
            ids = [l.split()[0] for l in cands[:2]]
            bodies = [lib("get", i) for i in ids]
            extra = "Reference material from the Wavefront Skills Library for this task. Use it where it fits and cite the id.\n\n" + \
                    "\n\n".join(f"### {i}\n{re.sub(r'^Wavefront Skills Library -.*?\n\n', '', b, count=1, flags=re.S)}" for i, b in zip(ids, bodies))
        r = claude(task["prompt"], a.model, extra, allow, cwd, settings_file, a.max_turns)
        r.update(id=task["id"], arm=which, prompt=task["prompt"], injected=extra[:4000])
        json.dump(r, open(path, "w", encoding="utf-8"), indent=1)
        return which, f"{r['secs']}s gets={r['gets']}" + (" EXIT" + str(r["exit"]) if r["exit"] else "")

    for t in tasks:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(a.arms)) as ex:
            res = list(ex.map(lambda w: arm(t, w), a.arms))
        print(t["id"], " ".join(f"{w}:{s}" for w, s in res), flush=True)


def judge(a):
    tasks = {t["id"]: t for t in json.load(open(a.tasks, encoding="utf-8"))[: a.limit or None]}
    vf = os.path.join(a.out, "verdicts.json")
    verdicts = json.load(open(vf)) if os.path.exists(vf) else {}
    rng = random.Random(42)
    settings_file = os.path.join(a.out, "clean-settings.json")
    for tid, t in tasks.items():
        def load(w):
            p = os.path.join(a.out, f"{tid}.{w}.json")
            return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None
        A = load("A")
        if not A or not A["answer"]: continue
        for w in "BC":
            key = f"{tid}:A-{w}"
            if key in verdicts: continue
            X = load(w)
            if not X or not X["answer"]: continue
            first_is_A = rng.random() < 0.5
            one, two = (A, X) if first_is_A else (X, A)
            prompt = (f"{RUBRIC}\n\n## REQUEST\n{t['prompt']}\n\n## ANSWER 1\n{one['answer']}\n\n## ANSWER 2\n{two['answer']}")
            p = sh(["claude", "-p", "--model", a.judge, "--output-format", "json", "--max-turns", "1",
                    "--permission-mode", "default", "--settings", settings_file, "--allowedTools", "NoSuchTool"], timeout=600, input=prompt)
            try:
                txt = json.loads(p.stdout).get("result", "")
                v = json.loads(re.search(r"\{.*\}", txt, re.S).group(0))
            except Exception as e:
                print(key, "judge parse failed:", str(e)[:80]); continue
            win = v.get("winner")
            mapped = "tie" if win == "tie" else ("A" if (win == "1") == first_is_A else w)
            sA, sX = (v.get("score1"), v.get("score2")) if first_is_A else (v.get("score2"), v.get("score1"))
            verdicts[key] = {"winner": mapped, "scoreA": sA, f"score{w}": sX, "reason": v.get("reason", ""), "gets": X.get("gets", 0)}
            json.dump(verdicts, open(vf, "w"), indent=1)
            print(key, mapped, sA, sX, "|", v.get("reason", "")[:90], flush=True)


def report(a):
    verdicts = json.load(open(os.path.join(a.out, "verdicts.json")))
    for w in "BC":
        rows = [v for k, v in verdicts.items() if k.endswith(f"A-{w}")]
        if not rows: continue
        n = len(rows); wins = sum(r["winner"] == w for r in rows); loss = sum(r["winner"] == "A" for r in rows); tie = n - wins - loss
        mA = sum(r["scoreA"] or 0 for r in rows) / n; mX = sum(r[f"score{w}"] or 0 for r in rows) / n
        extra = f"  fetched in {sum(1 for r in rows if r['gets'])}/{n} runs" if w == "B" else ""
        print(f"A vs {w}: n={n}  {w} wins {wins}  A wins {loss}  ties {tie}  mean score A {mA:.2f} vs {w} {mX:.2f}{extra}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("run", "judge", "report"):
        s = sub.add_parser(name); s.add_argument("--out", required=True)
        if name != "report": s.add_argument("--tasks", required=True)
    sub.choices["run"].add_argument("--limit", type=int, default=0); sub.choices["run"].add_argument("--arms", default="ABC")
    sub.choices["run"].add_argument("--model", default="sonnet"); sub.choices["run"].add_argument("--max-turns", type=int, default=8)
    sub.choices["judge"].add_argument("--judge", default="opus"); sub.choices["judge"].add_argument("--limit", type=int, default=0)
    a = p.parse_args(); {"run": run, "judge": judge, "report": report}[a.cmd](a)
