#!/usr/bin/env python3
"""Claude Code hook: consult the Wavefront Skills Library before the agent researches or reasons it out.

Two events, one script (the event name comes in on stdin):
  UserPromptSubmit          every real prompt: inject the best-matching methods/skills as context
  PreToolUse WebSearch|WebFetch  the moment research is about to happen: inject what the library already knows

Why: in a live pilot (9 Nov 2026) agents with the connector skill loaded answered expert tasks from memory and
never consulted the library; a description-triggered skill is advice, a hook is a guarantee. And a keyword
shortlist fired noise on 6 of 7 real prompts, so this version is semantic with a silence threshold: nothing is
injected unless the top match is clearly relevant.

Install (user settings, ~/.claude/settings.json), using the python that has fastembed + numpy:
  "UserPromptSubmit": [{"hooks": [{"type": "command", "timeout": 25,
      "command": "<python> -X utf8 \\"<path to this file>\\""}]}],
  "PreToolUse": [{"matcher": "WebSearch|WebFetch", "hooks": [{"type": "command", "timeout": 25,
      "command": "<python> -X utf8 \\"<path to this file>\\""}]}]

Environment:
  WAVEFRONT_SKILLS_LOCAL  library checkout (skills.index.jsonl must be current)
  WAVEFRONT_SKILLS_EMB    folder with ids.json + shard_*.npy from tools/retrieval_eval.py embed; unset = keyword fallback
  WAVEFRONT_SKILLS_MIN    cosine threshold for the top match (default 0.76); below it the hook says nothing

Falls back to the keyword search in skills.py when fastembed or embeddings are missing or out of date, with a
stricter rule (two distinct content words must match). Never blocks: any failure exits 0 with no output.
"""
import glob, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL = os.environ.get("WAVEFRONT_SKILLS_LOCAL", "")
EMB = os.environ.get("WAVEFRONT_SKILLS_EMB", "")
# Calibrated on bge-small: real tasks scored 0.765-0.789 for their top match and conversational prompts
# 0.635-0.75, so the margin is narrow; raise it if the hook is noisy, lower it if it stays silent on real tasks.
MIN = float(os.environ.get("WAVEFRONT_SKILLS_MIN", "0.76"))
MIN_WORDS = 6
SKIP = re.compile(r"^\s*(/|!|y(es)?\b|no?\b|ok(ay)?\b|thanks|continue|go ahead|do it|proceed)", re.I)
FACT = re.compile(r"^\s*(what is|what's|whats|who is|when (is|was|did)|how many|how much|define|translate)\b", re.I)
GET = f'python "{os.path.join(HERE, "skills.py")}" card <id>   # then: get <id>, and report <id> used|not_useful|wrong'


def query_text(data):
    ev = data.get("hook_event_name", "")
    if ev == "PreToolUse":
        ti = data.get("tool_input") or {}
        q = ti.get("query") or " ".join(x for x in (ti.get("prompt"), ti.get("url")) if x) or ""
        return ev, q.strip()
    p = (data.get("prompt") or "").strip()
    if len(p.split()) < MIN_WORDS or SKIP.match(p) or FACT.match(p):
        return ev, ""
    return ev or "UserPromptSubmit", p


def candidates(q):
    """Ask the librarian (semantic when embeddings are configured, keyword otherwise; it decides when to stay silent)."""
    if not LOCAL:
        return []
    sys.path.insert(0, os.path.join(LOCAL, "tools"))
    import librarian
    lib = librarian.Library(LOCAL)
    return [f"{r['id']}  [{r['kind']}, {r['status']}, {r['score']:.2f}] - {r['description']}" for r in lib.route(q, k=5)]


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    ev, q = query_text(data)
    if not q:
        return
    try:
        lines = candidates(q)
    except Exception:
        return
    if not lines:
        return
    lead = ("Before researching this, the Wavefront Skills Library already covers it. Use the fitting one "
            "instead of searching the web:" if ev == "PreToolUse" else
            "Wavefront Skills Library candidates for this task (ranked, cosine). Check the card of the fitting one before planning (card, then get if worth it):")
    ctx = (lead + "\n  " + GET + "\nPrefer method over skill, verified over draft; fetch at most two; cite the id you used. "
           "If none fits, ignore this and say 'No library coverage for: <summary>' in your reply.\n" + "\n".join(lines))
    print(json.dumps({"hookSpecificOutput": {"hookEventName": ev, "additionalContext": ctx}}))


if __name__ == "__main__":
    main()
