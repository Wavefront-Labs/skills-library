#!/usr/bin/env python3
"""librarian - the drill-in interface to the library.

An agent should consult a library of tens of thousands of skills while carrying almost nothing in context, the
way a person consults a librarian: state the job, get a few candidates, open one, read only what is needed.
Every operation returns a small bounded page, and an empty answer is a valid answer.

    route(task, context)    ranked candidates (id, kind, status, level, score, description); [] when nothing is close enough
    card(id)                the answer-shaped extract of one skill: goal, gotchas, verify, sources (a few hundred tokens)
    get(id)                 the full skill body
    expand(id)              neighbours: what a method uses, which methods use a skill, siblings in the same product
    browse(node)            walk the taxonomy: "" = categories, "cat" = fields, "cat.field" = products, "cat.field.product" = skills
    report(id, outcome)     feed the loop: used | not_useful | wrong | gap, appended to a local log (nothing leaves the machine)

    python tools/librarian.py route "retire a product from a shared Kubernetes cluster" --context kubernetes,argocd
    python tools/librarian.py card <id> | get <id> | expand <id> | browse [node] | report <id> <outcome> [--task ...] [--note ...]
    python tools/librarian.py --selftest

Retrieval is semantic when `WAVEFRONT_SKILLS_EMB` points at embeddings built by `tools/retrieval_eval.py embed` and
`fastembed` + `numpy` are installed; otherwise ranked keyword (BM25) with a stricter silence rule. Methods outrank
skills at equal relevance. Environment: WAVEFRONT_SKILLS_EMB, WAVEFRONT_SKILLS_MIN (clear-cosine floor, default 0.76), WAVEFRONT_SKILLS_LOW (floor when keywords agree, default 0.62),
WAVEFRONT_SKILLS_LOG (report log, default ~/.wavefront-skills/reports.jsonl).
"""
import glob, json, math, os, re, sys, time
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUS_RANK = {"verified": 3, "docs-checked": 2, "draft": 1, "unreviewed-low-risk": 1, "gated": 0, "stub": 0}
TOK = re.compile(r"[a-z0-9]+")
STOP = set("a an the and or of to in on for with is are be by from as at it this that how when what your you we i do can should my our".split())
LICENCE = ("Wavefront Skills Library - (c) 2026 Wavefront Labs and contributors. Licensed under the Apache License, "
           "Version 2.0; see LICENSE in the repository. Provided as is, without warranty.")
ID_IN_BODY = re.compile(r"`([a-z0-9][a-z0-9-]*(?:\.[a-z0-9][a-z0-9-]*){3})`")


def toks(s):
    return [t for t in TOK.findall(s.lower()) if t not in STOP and len(t) > 1]


class Library:
    def __init__(self, root=ROOT, emb_dir=None):
        self.root = root
        self.emb_dir = emb_dir if emb_dir is not None else os.environ.get("WAVEFRONT_SKILLS_EMB", "")
        self.min_cos = float(os.environ.get("WAVEFRONT_SKILLS_MIN", "0.76"))
        self.alpha = float(os.environ.get("WAVEFRONT_SKILLS_ALPHA", "0.25"))  # weight of keyword evidence next to cosine
        self.low_cos = float(os.environ.get("WAVEFRONT_SKILLS_LOW", "0.62"))  # floor when the keyword search agrees
        path = os.path.join(root, "skills.index.jsonl")
        if not os.path.exists(path):
            raise SystemExit("skills.index.jsonl missing: run `python tools/reindex.py` in the library checkout")
        self.rows = [json.loads(l) for l in open(path, encoding="utf-8")]
        self.by_id = {r["id"]: i for i, r in enumerate(self.rows)}
        for r in self.rows:
            for a in r.get("aliases", []):
                self.by_id.setdefault(a, self.by_id[r["id"]])
        self._bm = self._emb = self._uses = self._tax = None

    # ---------------------------------------------------------------- retrieval
    def _bm25(self):
        if self._bm is None:
            docs = [Counter(toks(" ".join([r["name"].replace("-", " ")] * 3 + [r.get("desc", "")] + r.get("tags", [])
                                          + [r.get("product", "").replace("-", " ")] * 2 + [r.get("field", "").replace("-", " ")])))
                    for r in self.rows]
            df = Counter(t for tf in docs for t in tf)
            self._bm = (docs, df, sum(sum(tf.values()) for tf in docs) / max(len(docs), 1))
        return self._bm

    def _semantic(self):
        if self._emb is None:
            self._emb = False
            try:
                import numpy as np
                from fastembed import TextEmbedding
                ids = json.load(open(os.path.join(self.emb_dir, "ids.json")))
                if ids == [r["id"] for r in self.rows]:
                    E = np.concatenate([np.load(f) for f in sorted(glob.glob(os.path.join(self.emb_dir, "shard_*.npy")))])
                    E /= np.linalg.norm(E, axis=1, keepdims=True)
                    self._emb = (np, E, TextEmbedding("BAAI/bge-small-en-v1.5", threads=4))
            except Exception:
                self._emb = False  # semantic mode is optional; fall back to keyword
        return self._emb

    def _speak(self, q, sc, top, kw):
        """Silence rule. Speak when the top cosine is clearly high, or moderately high AND the keyword search
        independently agrees (the top skill shares a content word with the question, and the two retrievers overlap
        in their top results). One cosine floor alone either missed 7 of 12 short real questions or let chit-chat
        through; this rule answered 18/19 real questions against 1/14 noise prompts on the labelled set it was chosen
        on, so treat the numbers as indicative, not validated."""
        c = float(sc[top[0]])
        if c >= self.min_cos:
            return True
        if c < self.low_cos or not kw:
            return False
        docs = self._bm25()[0]
        words = {w for w in toks(q) if len(w) > 3}
        overlap = len(words & set(docs[int(top[0])]))
        agree = len({int(i) for i in top[:5]} & set(sorted(kw, key=lambda i: -kw[i])[:10]))
        return overlap >= 1 and agree >= 1

    def _bm25_scores(self, query):
        docs, df, avg = self._bm25(); qt = toks(query); n = len(docs); out = {}
        for i, tf in enumerate(docs):
            ln = sum(tf.values()); s = 0.0
            for t in qt:
                if t in tf:
                    s += math.log(1 + (n - df[t] + .5) / (df[t] + .5)) * tf[t] * 2.2 / (tf[t] + 1.2 * (.25 + .75 * ln / avg))
            if s:
                out[i] = s
        return out

    def route(self, task, context=None, k=5, min_status="draft", include_gated=False):
        ctx = [c.strip().lower() for c in (context.split(",") if isinstance(context, str) else (context or [])) if c.strip()]
        q = (task or "").strip()[:600]
        if not q:
            return []
        floor = STATUS_RANK.get(min_status, 1)
        sem = self._semantic() if self.emb_dir else False
        scored = []
        if sem:
            np, E, model = sem
            v = np.array(list(model.query_embed([q + (" " + " ".join(ctx) if ctx else "")])), dtype=np.float32)[0]
            v /= np.linalg.norm(v)
            sc = E @ v
            top = np.argsort(-sc)[: max(k * 8, 40)]
            kw = self._bm25_scores(q + " " + " ".join(ctx))
            kmax = max(kw.values()) if kw else 1.0
            if not self._speak(q, sc, top, kw):
                return []                                  # silence is decided before fusion, from both retrievers
            floor = self.low_cos - 0.04
            pool = {int(i) for i in top if sc[i] >= floor} | {i for i, s in kw.items() if s >= 0.6 * kmax and sc[i] >= floor}
            scored = [(float(sc[i]) + self.alpha * kw.get(i, 0.0) / kmax, i) for i in pool]
        else:
            docs, df, avg = self._bm25()
            qt = toks(q + " " + " ".join(ctx)); n = len(docs)
            cand = []
            for i, tf in enumerate(docs):
                ln = sum(tf.values()); s = 0.0
                for t in qt:
                    if t in tf:
                        s += math.log(1 + (n - df[t] + .5) / (df[t] + .5)) * tf[t] * 2.2 / (tf[t] + 1.2 * (.25 + .75 * ln / avg))
                if s:
                    cand.append((s, i))
            cand.sort(reverse=True)
            cand = cand[: max(k * 4, 20)]
            words = {w for w in toks(q) if len(w) > 3}
            if not cand or len(words & set(docs[cand[0][1]])) < 2:
                return []                                  # silence rule for keyword mode: two distinct content words must match
            top_s = cand[0][0]
            scored = [(s / top_s, i) for s, i in cand]    # normalised; keyword scores are not comparable across queries
        out = []
        for s, i in scored:
            r = self.rows[i]
            st = r.get("status", "draft")
            if STATUS_RANK.get(st, 1) < floor or (st == "gated" and not include_gated):
                continue
            kind = "method" if r.get("product") == "methods" else "skill"
            boost = 1.08 if kind == "method" else 1.0
            if ctx and any(c in (r.get("tags", []) + [r.get("product", ""), r.get("field", "")]) for c in ctx):
                boost *= 1.05
            out.append({"id": r["id"], "kind": kind, "status": st, "level": r.get("level", "?"), "score": round(s * boost, 3),
                        "description": r.get("desc", "")})
        out.sort(key=lambda x: (-x["score"], -STATUS_RANK.get(x["status"], 1)))
        return out[: max(1, min(k, 10))]

    # ---------------------------------------------------------------- one skill
    def _row(self, sid):
        i = self.by_id.get(sid)
        return None if i is None else self.rows[i]

    def _read(self, row):
        text = open(os.path.join(self.root, row["path"]), encoding="utf-8", errors="replace").read()
        m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n(.*)", text, re.S)
        return (m.group(1), m.group(2).lstrip()) if m else ("", text)

    def get(self, sid):
        r = self._row(sid)
        if not r:
            return None
        return {"notice": LICENCE, "id": r["id"], "kind": "method" if r.get("product") == "methods" else "skill",
                "status": r.get("status"), "version": r.get("version"), "updated": r.get("updated"), "body": self._read(r)[1]}

    def card(self, sid):
        r = self._row(sid)
        if not r:
            return None
        front, body = self._read(r)
        goal = re.search(r"^\*\*Goal:\*\*\s*(.+?)(?:\n\s*\n|\Z)", body, re.M | re.S)
        sections = {}
        for m in re.finditer(r"^#{2,3}\s+(.+?)\s*$\n(.*?)(?=^#{2,3}\s|\Z)", body, re.M | re.S):
            sections[re.sub(r"\s*\(.*", "", m.group(1)).strip().lower()] = m.group(2)

        def bullets(*names, n=3):
            for nm in names:
                if nm in sections:
                    bl = [re.sub(r"\s+", " ", b).strip() for b in re.findall(r"^\s*(?:[-*]|\d+\.)\s+(?:\[.\]\s*)?(.+?)(?=^\s*(?:[-*]|\d+\.)\s|\Z)", sections[nm], re.M | re.S)]
                    if bl:
                        return [b[:220] for b in bl[:n]]
            return []
        for m in re.finditer(r"^(rules|gotchas|pitfalls|traps|limits):\s*\n((?:\s*[-*]\s.*\n?)+)", body, re.M | re.I):
            sections.setdefault(m.group(1).lower(), m.group(2))     # plain "Rules:" label lines, common in short skills
        src = re.search(r"^sources:\s*(\[.*?\])\s*$", front, re.M | re.S)
        card = {"id": r["id"], "kind": "method" if r.get("product") == "methods" else "skill", "status": r.get("status"),
                "level": r.get("level"), "version": r.get("version"), "updated": r.get("updated"), "description": r.get("desc", ""),
                "goal": re.sub(r"\s+", " ", goal.group(1)).strip()[:300] if goal else None,
                "gotchas": bullets("gotchas", "gotcha", "pitfalls", "traps", "failure modes this method exists to prevent", "rules", "limits"),
                "verify": bullets("verify", "self-check", "acceptance criteria", n=2)}
        if src:
            try:
                card["sources"] = json.loads(src.group(1).replace("'", '"'))[:3]
            except ValueError:
                pass
        else:
            blk = re.search(r"^sources:\s*\n((?:\s+-\s+.*\n?)+)", front, re.M)
            if blk:
                card["sources"] = [x.strip().strip("\"'") for x in re.findall(r"^\s+-\s+(.+)$", blk.group(1), re.M)][:3]
        card = {k: v for k, v in card.items() if v not in (None, [], "")}
        card["tokens_est"] = len(json.dumps(card)) // 4
        card["body_tokens_est"] = len(body) // 4
        return card

    # ---------------------------------------------------------------- neighbours
    def _links(self):
        if self._uses is None:                              # only methods carry component lists; scanning them is cheap
            self._uses = {}
            for r in self.rows:
                if r.get("product") == "methods":
                    ids = []
                    for m in ID_IN_BODY.finditer(self._read(r)[1]):
                        if m.group(1) in self.by_id and m.group(1) != r["id"] and m.group(1) not in ids:
                            ids.append(m.group(1))
                    self._uses[r["id"]] = ids
        return self._uses

    def expand(self, sid, limit=8):
        r = self._row(sid)
        if not r:
            return None
        links = self._links()
        brief = lambda i: {"id": i, "status": self.rows[self.by_id[i]].get("status"), "description": self.rows[self.by_id[i]].get("desc", "")}
        out = {"id": r["id"]}
        if r["id"] in links:
            out["uses"] = [brief(i) for i in links[r["id"]][: limit * 3]]
        used_by = [m for m, ids in links.items() if r["id"] in ids]
        if used_by:
            out["used_by_methods"] = [brief(i) for i in used_by[:limit]]
        sib = [x for x in self.rows if x["product"] == r["product"] and x["field"] == r["field"] and x["category"] == r["category"] and x["id"] != r["id"]]
        out["siblings"] = [{"id": x["id"], "status": x.get("status"), "description": x.get("desc", "")} for x in sib[:limit]]
        out["siblings_total"] = len(sib)
        return out

    # ---------------------------------------------------------------- taxonomy
    def _taxonomy(self):
        if self._tax is None:
            import yaml
            self._tax = {"cat": {}, "field": {}, "prod": {}}
            try:
                d = yaml.safe_load(open(os.path.join(self.root, "taxonomy", "categories.yaml"), encoding="utf-8"))["categories"]
                for c, v in d.items():
                    self._tax["cat"][c] = (v.get("covers") or "")
                for f in glob.glob(os.path.join(self.root, "taxonomy", "fields", "*.yaml")):
                    y = yaml.safe_load(open(f, encoding="utf-8")) or {}
                    for fld in y.get("fields", []) if isinstance(y, dict) else []:
                        self._tax["field"][f"{y.get('category')}.{fld.get('id')}"] = fld.get("scope") or ""
                for f in glob.glob(os.path.join(self.root, "taxonomy", "products", "*", "*.yaml")):
                    y = yaml.safe_load(open(f, encoding="utf-8")) or {}
                    for p in y.get("products", []) if isinstance(y, dict) else []:
                        self._tax["prod"][f"{y.get('category')}.{y.get('field')}.{p.get('id')}"] = p.get("scope") or ""
            except Exception:
                pass
        return self._tax

    def browse(self, node="", limit=20, offset=0):
        tax = self._taxonomy(); parts = [p for p in (node or "").split(".") if p]
        short = lambda s, n=170: re.sub(r"\s+", " ", s or "")[:n]
        if len(parts) == 0:
            cnt = Counter(r["category"] for r in self.rows)
            kids = [{"node": c, "count": n, "summary": short(tax["cat"].get(c))} for c, n in sorted(cnt.items(), key=lambda x: -x[1])]
        elif len(parts) == 1:
            cnt = Counter(r["field"] for r in self.rows if r["category"] == parts[0])
            kids = [{"node": f"{parts[0]}.{f}", "count": n, "summary": short(tax["field"].get(f"{parts[0]}.{f}"))} for f, n in sorted(cnt.items(), key=lambda x: -x[1])]
        elif len(parts) == 2:
            cnt = Counter(r["product"] for r in self.rows if r["category"] == parts[0] and r["field"] == parts[1])
            kids = [{"node": f"{node}.{p}", "count": n, "summary": short(tax["prod"].get(f"{node}.{p}"))} for p, n in sorted(cnt.items(), key=lambda x: -x[1])]
        else:
            rows = [r for r in self.rows if r["category"] == parts[0] and r["field"] == parts[1] and r["product"] == parts[2]]
            kids = [{"id": r["id"], "status": r.get("status"), "description": r.get("desc", "")} for r in rows]
        total = len(kids)
        return {"node": node or "", "total": total, "offset": offset, "children": kids[offset: offset + max(1, min(limit, 50))]}

    # ---------------------------------------------------------------- the loop
    def report(self, sid, outcome, task="", note=""):
        if outcome not in ("used", "not_useful", "wrong", "gap"):
            raise ValueError("outcome must be used | not_useful | wrong | gap")
        log = os.environ.get("WAVEFRONT_SKILLS_LOG") or os.path.join(os.path.expanduser("~"), ".wavefront-skills", "reports.jsonl")
        os.makedirs(os.path.dirname(log), exist_ok=True)
        rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "id": sid, "outcome": outcome,
               "task": (task or "")[:300], "note": (note or "")[:500]}
        with open(log, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        return {"logged": True, "log": log}


def _selftest():
    import tempfile
    os.environ["WAVEFRONT_SKILLS_LOG"] = os.path.join(tempfile.mkdtemp(), "r.jsonl")
    lib = Library()
    assert lib.route("hi", None) == [] and lib.route("", None) == [], "chit-chat must be silent"
    r = lib.route("move a Sealed Secret to a different name and namespace without breaking decryption")
    assert r and "sealed-secrets" in r[0]["id"], r[:1]
    c = lib.card(r[0]["id"]); g = lib.get(r[0]["id"])
    assert c["tokens_est"] < c["body_tokens_est"] and g["notice"].startswith("Wavefront"), "card must be smaller than the body"
    b = lib.browse(""); assert len(b["children"]) >= 20 and b["children"][0]["count"] > 100
    assert lib.browse("computing-software")["total"] > 10 and lib.browse("computing-software.devops-ci-cd.sealed-secrets")["total"] >= 3
    m = "computing-software.cloud-infrastructure-engineering.methods.retire-a-product-from-a-shared-cluster"
    if lib._row(m):
        e = lib.expand(m); assert len(e.get("uses", [])) >= 15, e.keys()
        used = lib.expand(e["uses"][0]["id"]); assert m in [x["id"] for x in used.get("used_by_methods", [])]
    assert lib.report(r[0]["id"], "used", task="selftest")["logged"]
    print(f"librarian selftest OK ({len(lib.rows)} skills, {'semantic' if lib._semantic() else 'keyword'} mode, card {c['tokens_est']} vs body {c['body_tokens_est']} tokens)")


def main(argv):
    if argv[:1] == ["--selftest"]:
        return _selftest()
    sys.stdout.reconfigure(encoding="utf-8")
    import argparse
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    r = s.add_parser("route"); r.add_argument("task"); r.add_argument("--context", default=""); r.add_argument("-k", type=int, default=5)
    for n in ("card", "get", "expand"):
        s.add_parser(n).add_argument("id")
    b = s.add_parser("browse"); b.add_argument("node", nargs="?", default=""); b.add_argument("--offset", type=int, default=0)
    t = s.add_parser("report"); t.add_argument("id"); t.add_argument("outcome"); t.add_argument("--task", default=""); t.add_argument("--note", default="")
    a = p.parse_args(argv); lib = Library()
    out = {"route": lambda: {"notice": LICENCE, "results": lib.route(a.task, a.context, a.k)},
           "card": lambda: lib.card(a.id), "get": lambda: lib.get(a.id), "expand": lambda: lib.expand(a.id),
           "browse": lambda: lib.browse(a.node, offset=a.offset), "report": lambda: lib.report(a.id, a.outcome, a.task, a.note)}[a.cmd]()
    if out is None:
        sys.exit("no such skill")
    if a.cmd == "get":
        print(out["notice"], "\n"); print(out["body"])
    else:
        print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1:])
