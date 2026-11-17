#!/usr/bin/env python3
"""coverage_check - does the library cover every canonical topic of a subject?

Specs live in taxonomy/coverage/<subject>.yaml: a scope (category/field/products) and a list of
canonical topics drawn from external sources (exam blueprints, official docs ToCs, SIG lists),
each with `match` keywords. A topic is covered when a skill in scope has a tag equal to a
keyword, or a keyword appears as a whole word in the skill's id/name. `min: N` on a topic requires N skills.
Depth: a topic may list `subtopics` (same id/name/match shape, taken from the source's sub-sections);
the report shows subtopics covered as a percentage. Breadth = topics covered; depth = subtopics covered.

Run: python tools/coverage_check.py             # report; exit 0 (gaps are content work, not CI failures)
     python tools/coverage_check.py --strict    # exit 1 on any uncovered topic
     python tools/coverage_check.py --markdown  # issue body for the scheduled coverage workflow
     python tools/coverage_check.py --json
     python tools/coverage_check.py --selftest
Spec shape errors (bad scope, duplicate topic ids, empty match) always exit 2.
"""
import json
import re
import sys
import yaml
from reindex import ROOT, load_skills

SPECS = ROOT / "taxonomy" / "coverage"


def validate(spec):
    errs = []
    scope = spec.get("scope") or {}
    for k in ("category", "field", "products"):
        if not scope.get(k):
            errs.append(f"scope.{k} missing")
    seen = set()
    for t in spec.get("topics") or []:
        for st in t.get("subtopics") or []:
            if not st.get("id") or not st.get("match"):
                errs.append(f"topic {t.get('id')}: subtopic without id/match")
        tid = t.get("id")
        if not tid:
            errs.append("topic without id")
        elif tid in seen:
            errs.append(f"duplicate topic id {tid!r}")
        seen.add(tid)
        if not t.get("match"):
            errs.append(f"topic {tid!r}: empty match")
    if not seen:
        errs.append("no topics")
    return errs


def load_specs(d=SPECS):
    specs = []
    for p in sorted(d.glob("*.yaml")):
        spec = yaml.safe_load(p.read_text(encoding="utf-8"))
        spec["_file"] = p.name
        errs = validate(spec)
        if errs:
            print(f"{p.name}: " + "; ".join(errs), file=sys.stderr)
            sys.exit(2)
        specs.append(spec)
    return specs


def in_scope(skill, scope):
    return (skill["category"] == scope["category"] and skill["field"] == scope["field"]
            and skill["product"] in scope["products"])


def covers(skill, keywords):
    if "_hay" not in skill:  # computed once per skill: specs x topics x subtopics call this a lot
        skill["_tags"] = {str(t).lower() for t in skill.get("tags") or []}
        # Whole-word match on id/name: "ci" must not hit "lifecycle", "env" must not hit "environment".
        skill["_hay"] = " " + re.sub(r"[^a-z0-9]+", " ", (skill["id"] + " " + skill["name"]).lower()) + " "
    tags, hay = skill["_tags"], skill["_hay"]
    return [k for k in keywords if str(k).lower() in tags
            or " " + re.sub(r"[^a-z0-9]+", " ", str(k).lower()) + " " in hay]


def check(spec, skills):
    pool = [s for s in skills if in_scope(s, spec["scope"])]
    rows = []
    for t in spec["topics"]:
        hits = [s["id"] for s in pool if covers(s, t["match"])]
        need = int(t.get("min", 1))
        subs = [{"id": st["id"], "name": st.get("name", st["id"]),
                 "covered": any(covers(s, st["match"]) for s in pool)}
                for st in t.get("subtopics") or []]
        rows.append({"id": t["id"], "name": t.get("name", t["id"]), "source": t.get("source", ""),
                     "min": need, "skills": hits, "covered": len(hits) >= need, "subtopics": subs})
    n_sub = sum(len(r["subtopics"]) for r in rows)
    n_sub_ok = sum(1 for r in rows for st in r["subtopics"] if st["covered"])
    return {"subject": spec.get("subject", spec["_file"]), "scope": spec["scope"],
            "in_scope_skills": len(pool), "topics": rows,
            "depth": {"subtopics": n_sub, "covered": n_sub_ok,
                      "pct": round(100.0 * n_sub_ok / n_sub, 1) if n_sub else None}}


def report(res):
    gaps = [r for r in res["topics"] if not r["covered"]]
    n = len(res["topics"])
    d = res["depth"]
    depth = f"; depth {d['covered']}/{d['subtopics']} subtopics ({d['pct']}%)" if d["subtopics"] else "; depth: no subtopics yet"
    print(f"== {res['subject']}: {n - len(gaps)}/{n} canonical topics covered "
          f"({res['in_scope_skills']} skills in scope){depth}")
    for r in res["topics"]:
        mark = "ok " if r["covered"] else "GAP"
        print(f"  [{mark}] {r['id']:<34} {len(r['skills']):>3} skill(s)  {r['source']}")
        for st in r["subtopics"]:
            if not st["covered"]:
                print(f"        [sub-GAP] {r['id']}/{st['id']}  {st['name']}")
    return gaps


def markdown(results):
    out = []
    for res in results:
        gaps = [r for r in res["topics"] if not r["covered"]]
        n = len(res["topics"])
        d = res["depth"]
        depth = f", depth {d['covered']}/{d['subtopics']} subtopics ({d['pct']}%)" if d["subtopics"] else ""
        out.append(f"### {res['subject']}: {n - len(gaps)}/{n} canonical topics covered "
                   f"({res['in_scope_skills']} skills in scope{depth})")
        sub_gaps = [(r, st) for r in res["topics"] for st in r["subtopics"] if not st["covered"]]
        if sub_gaps:
            out.append(f"{len(sub_gaps)} subtopic gap(s): " + ", ".join(f"`{r['id']}/{st['id']}`" for r, st in sub_gaps[:40])
                       + (" ..." if len(sub_gaps) > 40 else ""))
        if gaps:
            out.append("| missing topic | source | needs |\n|---|---|---|")
            out += [f"| `{r['id']}` - {r['name']} | {r['source']} | {r['min']} skill(s) |" for r in gaps]
        else:
            out.append("No gaps.")
        out.append("")
    return "\n".join(out)


def selftest():
    skills = [
        {"id": "c.f.p.foo-bar", "name": "foo-bar", "category": "c", "field": "f", "product": "p", "tags": ["alpha"]},
        {"id": "c.f.q.other", "name": "other", "category": "c", "field": "f", "product": "q", "tags": ["beta"]},
    ]
    spec = {"_file": "t", "subject": "t", "scope": {"category": "c", "field": "f", "products": ["p"]},
            "topics": [{"id": "a", "match": ["alpha"]},            # tag hit
                       {"id": "b", "match": ["bar"]},              # id/name whole-word hit
                       {"id": "e", "match": ["ba"]},               # substring only: must NOT hit
                       {"id": "c", "match": ["beta"]},             # only an out-of-scope skill matches
                       {"id": "d", "match": ["alpha"], "min": 2,   # min not met
                        "subtopics": [{"id": "s1", "match": ["alpha"]}, {"id": "s2", "match": ["gamma"]}]}]}
    assert validate(spec) == []
    got = {r["id"]: r["covered"] for r in check(spec, skills)["topics"]}
    assert got == {"a": True, "b": True, "c": False, "d": False, "e": False}, got
    assert check(spec, skills)["depth"] == {"subtopics": 2, "covered": 1, "pct": 50.0}
    assert validate({"scope": {}, "topics": [{"id": "x"}, {"id": "x", "match": []}]})
    print("coverage_check selftest OK")


def main(argv):
    if "--selftest" in argv:
        return selftest()
    skills = load_skills()
    results = [check(s, skills) for s in load_specs()]
    if "--json" in argv:
        print(json.dumps(results, indent=1))
    elif "--markdown" in argv:
        print(markdown(results))
    else:
        total_gaps = sum(len(report(r)) for r in results)
        if total_gaps and "--strict" in argv:
            sys.exit(f"{total_gaps} uncovered canonical topic(s)")


if __name__ == "__main__":
    main(sys.argv[1:])
