#!/usr/bin/env python3
"""Back-test skill/method retrieval: can a vague, real-world query find the right skills?

Why this exists: the library is only worth anything if a consumer's agent can find the right skill
from how a person actually phrases a job. Keyword matching alone fails that (it needs the skill's own
words in the query), so we measure keyword, semantic and hybrid search against labelled queries.

    pip install fastembed numpy          # not needed by the rest of the repo
    python tools/reindex.py              # skills.index.jsonl must be current
    python tools/retrieval_eval.py embed --out D:/scratch/emb        # first run ~25 min on CPU; later runs embed only new or edited skills
    python tools/retrieval_eval.py eval eval/queries/retire-product-blind.json --emb D:/scratch/emb

Skip the 25-minute embed: download the published `skills-emb.npz` (release asset), then
    python tools/retrieval_eval.py unpack skills-emb.npz --out D:/scratch/emb
    python tools/retrieval_eval.py embed --out D:/scratch/emb        # embeds only what your checkout added or edited
Maintainers publish with: python tools/retrieval_eval.py pack --emb <dir> --out skills-emb.npz

Query files are JSON lists of {"kind": "method|skill|control", "q": "...", "expect": ["<skill id>", ...]}.
  method / skill : pass if ANY expected id is in the top-k
  control        : off-topic query; pass if NONE of the expected ids appears (false-positive check)
Write queries BLIND (someone who has not read the skill's description), or the test measures
your own vocabulary rather than a user's.

What a skill/method is findable by: name, description (<= 200 chars), tags, product, field. Put the
words a person would use (retire, sunset, wind down, decommission...) in the description and tags.
"""
import argparse, collections, glob, json, math, os, re, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.environ.get("SKILLS_INDEX", os.path.join(ROOT, "skills.index.jsonl"))
MODEL = "BAAI/bge-small-en-v1.5"
TOK = re.compile(r"[a-z0-9]+")
STOP = set("a an the and or of to in on for with is are be by from as at it this that how when what your you we i do can should my our".split())


def toks(s):
    return [t for t in TOK.findall(s.lower()) if t not in STOP and len(t) > 1]


def load():
    return [json.loads(l) for l in open(INDEX, encoding="utf-8")]


def emb_text(d):  # what is embedded; keep in step with whatever the index exposes
    return f"{d['name'].replace('-', ' ')}. {d.get('desc', '')} {' '.join(d.get('tags', []))}"


def text_hash(d):
    import hashlib
    return hashlib.md5(emb_text(d).encode("utf-8")).hexdigest()[:12]


def cmd_embed(a):
    """Incremental: only skills that are new or whose name/description/tags changed are embedded; the rest reuse
    their stored vectors. A fresh folder embeds everything (about 25 min for 50K skills on CPU, resumable by --seconds)."""
    import numpy as np
    from fastembed import TextEmbedding
    rows = load(); os.makedirs(a.out, exist_ok=True)
    ids_f, hash_f = os.path.join(a.out, "ids.json"), os.path.join(a.out, "hashes.json")
    old = {}
    if os.path.exists(ids_f) and glob.glob(os.path.join(a.out, "shard_*.npy")):
        old_ids = json.load(open(ids_f))
        E = np.concatenate([np.load(f) for f in sorted(glob.glob(os.path.join(a.out, "shard_*.npy")))])
        old_hash = json.load(open(hash_f)) if os.path.exists(hash_f) else [None] * len(old_ids)
        old = {i: (E[n], old_hash[n]) for n, i in enumerate(old_ids) if n < len(E)}
    hashes = [text_hash(d) for d in rows]
    todo = [n for n, d in enumerate(rows) if d["id"] not in old or (old[d["id"]][1] not in (None, hashes[n]))]
    print(f"{len(rows)} skills: {len(rows) - len(todo)} reused, {len(todo)} to embed")
    vecs = {}
    if todo:
        model = TextEmbedding(MODEL, threads=a.threads); t0 = time.time()
        for s in range(0, len(todo), 2000):
            if time.time() - t0 > a.seconds:
                print("time budget reached; rerun to continue (finished vectors are kept in memory only, so rerun with a larger --seconds)")
                return
            chunk = todo[s:s + 2000]
            v = np.array(list(model.embed([emb_text(rows[n]) for n in chunk], batch_size=64)), dtype=np.float32)
            for n, x in zip(chunk, v):
                vecs[n] = x
            print(f"embedded {min(s + 2000, len(todo))}/{len(todo)} at {time.time() - t0:.0f}s", flush=True)
    full = np.stack([vecs[n] if n in vecs else old[rows[n]["id"]][0] for n in range(len(rows))]).astype(np.float32)
    for f in glob.glob(os.path.join(a.out, "shard_*.npy")):
        os.remove(f)
    for s in range(0, len(full), 4000):
        np.save(os.path.join(a.out, f"shard_{s // 4000:03d}.npy"), full[s:s + 4000])
    json.dump([d["id"] for d in rows], open(ids_f, "w")); json.dump(hashes, open(hash_f, "w"))
    print("embeddings up to date")


def cmd_pack(a):
    """One compact file (float16, ~40 MB for 50K skills) for a release asset, so nobody has to embed the library themselves."""
    import numpy as np
    ids = json.load(open(os.path.join(a.emb, "ids.json"))); hashes = json.load(open(os.path.join(a.emb, "hashes.json")))
    E = np.concatenate([np.load(f) for f in sorted(glob.glob(os.path.join(a.emb, "shard_*.npy")))]).astype(np.float32)
    E /= np.linalg.norm(E, axis=1, keepdims=True)
    np.savez_compressed(a.out, E=E.astype(np.float16), ids=json.dumps(ids), hashes=json.dumps(hashes), model=MODEL)
    print(f"packed {len(ids)} vectors -> {a.out} ({os.path.getsize(a.out if a.out.endswith('.npz') else a.out + '.npz') // 2**20} MB)")


def cmd_unpack(a):
    """Unpack a published file into an embeddings folder; then run `embed --out` on it to top up whatever your checkout has added or edited."""
    import numpy as np
    z = np.load(a.file); os.makedirs(a.out, exist_ok=True)
    if str(z["model"]) != MODEL: sys.exit(f"index was built with {z['model']}, this tool uses {MODEL}")
    for f in glob.glob(os.path.join(a.out, "shard_*.npy")): os.remove(f)
    E = z["E"].astype(np.float32)
    for s in range(0, len(E), 4000): np.save(os.path.join(a.out, f"shard_{s // 4000:03d}.npy"), E[s:s + 4000])
    open(os.path.join(a.out, "ids.json"), "w").write(str(z["ids"])); open(os.path.join(a.out, "hashes.json"), "w").write(str(z["hashes"]))
    print(f"unpacked {len(E)} vectors into {a.out}; now run: python tools/retrieval_eval.py embed --out {a.out}")


def cmd_eval(a):
    import numpy as np
    from fastembed import TextEmbedding
    rows = load()
    ids = json.load(open(os.path.join(a.emb, "ids.json")))
    if ids != [d["id"] for d in rows]:
        sys.exit("embeddings are out of date with skills.index.jsonl: rerun `embed` (delete the old shards first)")
    E = np.concatenate([np.load(f) for f in sorted(glob.glob(os.path.join(a.emb, "shard_*.npy")))])
    E /= np.linalg.norm(E, axis=1, keepdims=True)
    docs = [collections.Counter(toks(" ".join([d["name"].replace("-", " ")] * 3 + [d.get("desc", "")] + d.get("tags", []) +
                                              [d.get("product", "").replace("-", " ")] * 2 + [d.get("field", "").replace("-", " ")]))) for d in rows]
    N = len(docs); df = collections.Counter(t for tf in docs for t in tf); avg = sum(sum(tf.values()) for tf in docs) / N
    model = TextEmbedding(MODEL, threads=a.threads)

    def keyword(q):
        sc = np.zeros(N); qt = toks(q)
        for i, tf in enumerate(docs):
            ln = sum(tf.values())
            for t in qt:
                if t in tf:
                    sc[i] += math.log(1 + (N - df[t] + .5) / (df[t] + .5)) * tf[t] * 2.2 / (tf[t] + 1.2 * (.25 + .75 * ln / avg))
        return sc

    def semantic(q):
        v = np.array(list(model.query_embed([q])), dtype=np.float32)[0]; v /= np.linalg.norm(v)
        return E @ v

    top = lambda sc, k=60: list(np.argsort(-sc)[:k])

    def hybrid(b, s):
        r = collections.defaultdict(float)
        for L in (b, s):
            for rank, i in enumerate(L): r[i] += 1 / (60 + rank)
        return [i for i, _ in sorted(r.items(), key=lambda x: -x[1])]

    queries = json.load(open(a.queries, encoding="utf-8"))
    tally = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0, 0]))  # kind -> mode -> [@3, @10, n]
    misses = []
    for q in queries:
        exp = set(q["expect"]); b, s = top(keyword(q["q"])), top(semantic(q["q"]))
        for mode, L in (("keyword", b), ("semantic", s), ("hybrid", hybrid(b, s))):
            got = [ids[i] for i in L]; h3 = any(i in exp for i in got[:3]); h10 = any(i in exp for i in got[:10])
            if q["kind"] == "control": h3, h10 = not h3, not h10
            t = tally[q["kind"]][mode]; t[0] += h3; t[1] += h10; t[2] += 1
            if mode == "semantic" and not h3: misses.append((q["kind"], q["q"], "in top 10" if h10 else "not in top 10"))
    print(f"{len(queries)} queries, {N} skills indexed\n")
    for kind, modes in tally.items():
        label = "no false positive in top 3" if kind == "control" else "found in top 3 / top 10"
        print(f"[{kind}] ({label})")
        for m, (h3, h10, n) in modes.items():
            print(f"   {m:9} {h3:3}/{n} ({100 * h3 // n:3}%)   {h10:3}/{n} ({100 * h10 // n:3}%)")
    if misses:
        print("\nsemantic misses outside top 3:")
        for kind, q, where in misses: print(f"   [{kind}] {q}  ({where})")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("embed"); e.add_argument("--out", required=True); e.add_argument("--seconds", type=float, default=520); e.add_argument("--threads", type=int, default=4)
    v = sub.add_parser("eval"); v.add_argument("queries"); v.add_argument("--emb", required=True); v.add_argument("--threads", type=int, default=4)
    k = sub.add_parser("pack"); k.add_argument("--emb", required=True); k.add_argument("--out", required=True)
    u = sub.add_parser("unpack"); u.add_argument("file"); u.add_argument("--out", required=True)
    a = p.parse_args()
    {"embed": cmd_embed, "eval": cmd_eval, "pack": cmd_pack, "unpack": cmd_unpack}[a.cmd](a)
