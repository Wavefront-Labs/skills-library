#!/usr/bin/env python3
"""serve - the reference for what any server in front of this library returns.
Contract: EVERY response starts with the licence notice, before any skill data.
Search returns ids + descriptions only; full text comes back one skill per call.
Run: python tools/serve.py search <words...> | python tools/serve.py get <id> | python tools/serve.py --selftest
"""
import json, re, sys
from reindex import MANIFEST, ROOT

LICENCE_NOTICES = {
    "Apache-2.0": (
        "Wavefront Skills Library - (c) 2026 Wavefront Labs and contributors. Licensed under the Apache License, "
        "Version 2.0; see LICENSE in the repository. Provided as is, without warranty."
    ),
}


def _skills():
    return [json.loads(l) for l in MANIFEST.read_text(encoding="utf-8").splitlines() if l.strip()]


_TOK = re.compile(r"[a-z0-9]+")
_STOP = set("a an the and or of to in on for with is are be by from as at it this that how when what your you we i do can should my our".split())


def _toks(s):
    return [t for t in _TOK.findall(s.lower()) if t not in _STOP and len(t) > 1]


def search(words, limit=10):
    """Ranked keyword search (BM25) over name, description, tags, product and field.

    Replaced the old all-words-must-appear filter on 9 Nov 2026: on 24 blind phrasings of one
    method that filter returned it 0 times; this ranks it in the top 3 for 7 and the top 10 for 9.
    Semantic search (tools/retrieval_eval.py) does better again and is what the hosted API uses;
    this is the dependency-free floor. Methods outrank skills at equal score.
    """
    import math
    from collections import Counter
    q = _toks(" ".join(words))
    rows = _skills()
    docs = [Counter(_toks(" ".join([s["id"].split(".")[-1].replace("-", " ")] * 3 + [s["desc"]] + s["tags"]
                                   + [s.get("product", "").replace("-", " ")] * 2 + [s.get("field", "").replace("-", " ")])))
            for s in rows]
    n = len(docs)
    df = Counter(t for tf in docs for t in tf)
    avg = sum(sum(tf.values()) for tf in docs) / max(n, 1)
    scored = []
    for s, tf in zip(rows, docs):
        ln = sum(tf.values())
        sc = sum(math.log(1 + (n - df[t] + .5) / (df[t] + .5)) * tf[t] * 2.2 / (tf[t] + 1.2 * (.25 + .75 * ln / avg))
                 for t in q if t in tf)
        if sc:
            scored.append((sc * (1.15 if s.get("product") == "methods" else 1.0), s))
    scored.sort(key=lambda x: -x[0])
    lines = [f"{s['id']}  [{'method' if s.get('product') == 'methods' else 'skill'}, {s.get('status', '?')}] - {s['desc']}"
             for _, s in scored[:max(1, min(limit, 10))]]
    return LICENCE_NOTICES["Apache-2.0"] + "\n\n" + ("\n".join(lines) or "no matches")


def get(skill_id):
    s = next((s for s in _skills() if s["id"] == skill_id or skill_id in s.get("aliases", [])), None)  # old ids keep working after a move
    if not s:
        return LICENCE_NOTICES["Apache-2.0"] + "\n\nno such skill"
    body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", (ROOT / s["path"]).read_text(encoding="utf-8"), count=1, flags=re.S)
    return LICENCE_NOTICES[s["licence"]] + "\n\n" + body.lstrip()


def selftest():
    first = _skills()[0]
    for out in (search(["blender"]), search(["zzz-no-such-thing"]), get(first["id"]), get("no.such.id")):
        assert out.startswith(LICENCE_NOTICES["Apache-2.0"]), out[:80]
    assert "---" not in get(first["id"]).splitlines()[2], "frontmatter leaked"
    print("serve selftest OK")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # skills contain non-ASCII; Windows consoles default to cp1252
    a = sys.argv[1:]
    if a == ["--selftest"]:
        selftest()
    elif a[:1] == ["search"]:
        print(search(a[1:]))
    elif a[:1] == ["get"] and len(a) == 2:
        print(get(a[1]))
    else:
        print(__doc__); sys.exit(2)
