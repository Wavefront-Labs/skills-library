#!/usr/bin/env python3
"""Wavefront Skills Library client used by the connector skill.

    python skills.py find "<one-sentence task summary>" [-k 5] [--context kubernetes,argocd]
    python skills.py card <id> | get <id> | expand <id> | browse [node]
    python skills.py report <id> used|not_useful|wrong|gap [--task "..."] [--note "..."]

Environment (one of):
    WAVEFRONT_SKILLS_LOCAL  path to a library checkout: searched directly through its tools/serve.py
    WAVEFRONT_SKILLS_URL    base URL of a hosted instance implementing connector/CONTRACT.md

Output is plain text meant for an agent: find prints at most 10 lines, get prints one skill, and every
response starts with the licence notice. Standard library only, so it runs wherever Python 3.9+ does.
"""
import argparse, json, os, re, subprocess, sys, urllib.error, urllib.parse, urllib.request

LOCAL = os.environ.get("WAVEFRONT_SKILLS_LOCAL", "")
URL = os.environ.get("WAVEFRONT_SKILLS_URL", "")
MAX_K = 10


def api(path, params=None):
    url = URL.rstrip("/") + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "wavefront-skills-connector/0.2.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        msg = {404: "no such skill", 429: "rate limited, wait a minute"}
        sys.exit(f"library: {msg.get(e.code, f'HTTP {e.code}')}")
    except (urllib.error.URLError, TimeoutError) as e:
        sys.exit(f"library unreachable ({e}); continue without it")


def librarian():
    sys.path.insert(0, os.path.join(LOCAL, "tools"))
    import librarian as lib
    return lib.Library(LOCAL)


def local(cmd, *args):
    out = subprocess.run([sys.executable, "-X", "utf8", os.path.join(LOCAL, "tools", "serve.py"), cmd, *args],
                         capture_output=True, text=True, encoding="utf-8")
    return out.stdout if out.returncode == 0 else sys.exit(out.stderr.strip() or "local library call failed")


def need_source():
    if not LOCAL and not URL:
        sys.exit("No library configured. Set WAVEFRONT_SKILLS_LOCAL to a checkout of the Wavefront Skills Library "
                 "(https://github.com/Wavefront-Labs/skills-library) or WAVEFRONT_SKILLS_URL to a hosted instance. "
                 "Continuing without the library is fine.")


def find(q, k, context=""):
    need_source()
    k = max(1, min(k, MAX_K))
    if LOCAL:
        rows = librarian().route(q, context, k)
        if not rows:
            print("no matching skills or methods")
        for r in rows:
            print(f"{r['id']}  [{r['kind']}, {r['status']}, {r['level']}, score {r['score']:.2f}]\n    {r['description']}")
        return
    d = api("/find", {"q": q, "k": k})
    if d.get("deprecated"):
        print("CONNECTOR OUT OF DATE: update the wavefront-skills skill, then retry.")
    if d.get("notice"):
        print(d["notice"], "\n")
    rows = d.get("results", [])
    if not rows:
        print("no matching skills or methods")
        return
    for r in rows:
        print(f"{r['id']}  [{r.get('kind', 'skill')}, {r.get('status', '?')}, {r.get('level', '?')}, score {r.get('score', 0):.2f}]\n    {r.get('description', '')}")


def get(skill_id):
    need_source()
    if not re.fullmatch(r"[a-z0-9][a-z0-9\-.]{2,200}", skill_id):
        sys.exit("not a skill id")
    if LOCAL:
        print(local("get", skill_id))
        return
    d = api(f"/skills/{urllib.parse.quote(skill_id)}")
    if d.get("deprecated"):
        print("CONNECTOR OUT OF DATE: update the wavefront-skills skill, then retry.")
    print(d.get("notice", ""), "\n")
    print(d.get("body", ""))


def local_only(fn):
    need_source()
    if not LOCAL:
        sys.exit("this command needs WAVEFRONT_SKILLS_LOCAL (a hosted instance only implements find and get)")
    out = fn(librarian())
    if out is None:
        sys.exit("no such skill")
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("find"); f.add_argument("query"); f.add_argument("-k", type=int, default=5); f.add_argument("--context", default="")
    for n in ("get", "card", "expand"):
        sub.add_parser(n).add_argument("id")
    b = sub.add_parser("browse"); b.add_argument("node", nargs="?", default="")
    r = sub.add_parser("report"); r.add_argument("id"); r.add_argument("outcome"); r.add_argument("--task", default=""); r.add_argument("--note", default="")
    a = p.parse_args()
    if a.cmd == "find":
        find(a.query, a.k, a.context)
    elif a.cmd == "get":
        get(a.id)
    elif a.cmd == "card":
        local_only(lambda l: l.card(a.id))
    elif a.cmd == "expand":
        local_only(lambda l: l.expand(a.id))
    elif a.cmd == "browse":
        local_only(lambda l: l.browse(a.node))
    else:
        local_only(lambda l: l.report(a.id, a.outcome, a.task, a.note))
