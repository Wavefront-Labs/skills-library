#!/usr/bin/env python3
"""attest - create and check skill review attestations (see REVIEWING.md).

  python tools/attest.py template <skill-id> [--github NAME]   skeleton JSON on stdout, skill hash filled in
  python tools/attest.py seal <file>                           write attestation_sha256 into the file
  python tools/attest.py check <file> [--refetch]              exit 1 on any failure
  python tools/attest.py selftest

`check` always: validates shape, skill hash vs the current file, each claim appears verbatim in the skill,
each confirmed/contradicted claim cites a listed source with a quote, and the seal matches.
`--refetch` also downloads every source and requires each evidence_quote to appear in the page text.
The network is used only with --refetch."""
import hashlib, html, json, re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHA = re.compile(r"^[0-9a-f]{64}$")
VERDICTS = {"confirmed", "contradicted", "unverifiable", "gated"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def skill_bytes(p):
    return p.read_bytes().replace(b"\r\n", b"\n")


def canon(d):
    body = {k: v for k, v in d.items() if k != "attestation_sha256"}
    return json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def norm(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip().lower()


def find_skill(sid):
    cat, field, prod, name = sid.split(".", 3)
    p = ROOT / "skills" / cat / field / prod / f"{name}.md"
    if not p.exists():
        sys.exit(f"no such skill file: {p}")
    return p


def template(sid, gh):
    p = find_skill(sid)
    t = p.read_text(encoding="utf-8")
    m = re.search(r"^version:\s*(\S+)", t, re.M)
    line = re.search(r"^sources:.*$", t, re.M)
    urls = re.findall(r"https://[^\s\"',\]]+", line.group(0)) if line else []
    return {
        "schema": "wavefront-attestation/1", "protocol": "docs-check/1",
        "skill": {"id": sid, "version": m.group(1) if m else "1", "sha256": sha(skill_bytes(p))},
        "reviewer": {"github": gh, "kind": "agent", "agent": "", "model": ""},
        "reviewed_at": "",
        "sources": [{"url": u, "fetched_at": "", "http_status": 200, "content_sha256": ""} for u in urls],
        "claims": [{"claim": "", "verdict": "confirmed", "source_url": "", "evidence_quote": ""}],
        "coverage": "", "verdict": "pass", "attestation_sha256": "",
    }


def fetch(url):
    r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "wavefront-attest/1"}), timeout=30)
    return r.status, r.read()


def check(d, refetch=False):
    e = []
    for k in ("schema", "protocol", "skill", "reviewer", "reviewed_at", "sources", "claims", "verdict", "attestation_sha256"):
        if k not in d:
            e.append(f"missing {k}")
    if e:
        return e
    if d["schema"] != "wavefront-attestation/1":
        e.append("unknown schema")
    if d["verdict"] not in ("pass", "needs-changes", "fail"):
        e.append("bad verdict")
    for k in ("github", "kind"):
        if not d["reviewer"].get(k):
            e.append(f"reviewer.{k} empty")
    s = d["skill"]
    try:
        sp = find_skill(s["id"])
    except SystemExit as x:
        return e + [str(x)]
    text = skill_bytes(sp).decode("utf-8")
    if sha(skill_bytes(sp)) != s.get("sha256"):
        e.append("skill sha256 does not match the current file (skill changed since review, or wrong hash)")
    urls = {x["url"] for x in d["sources"]}
    for x in d["sources"]:
        if not x["url"].startswith("https://"):
            e.append(f"source not https: {x['url']}")
        if not SHA.match(x.get("content_sha256", "")):
            e.append(f"bad content_sha256 for {x['url']}")
    if not d["claims"]:
        e.append("no claims")
    for i, c in enumerate(d["claims"]):
        if c.get("verdict") not in VERDICTS:
            e.append(f"claim {i}: bad verdict")
            continue
        if not c.get("claim") or c["claim"] not in text:
            e.append(f"claim {i}: text not found verbatim in the skill")
        if c["verdict"] in ("confirmed", "contradicted"):
            if c.get("source_url") not in urls:
                e.append(f"claim {i}: source_url not in sources")
            if not c.get("evidence_quote"):
                e.append(f"claim {i}: evidence_quote required")
    if sha(canon(d)) != d["attestation_sha256"]:
        e.append("attestation_sha256 mismatch (edited after sealing, or not sealed)")
    if refetch and not e:
        pages = {}
        for u in urls:
            try:
                pages[u] = fetch(u)
            except Exception as ex:
                e.append(f"refetch failed {u}: {ex}")
        for x in d["sources"]:
            if x["url"] in pages and pages[x["url"]][0] != x["http_status"]:
                e.append(f"{x['url']}: status {pages[x['url']][0]} != {x['http_status']}")
        for i, c in enumerate(d["claims"]):
            if c["verdict"] in ("confirmed", "contradicted") and c["source_url"] in pages:
                page = norm(pages[c["source_url"]][1].decode("utf-8", "replace"))
                if norm(c["evidence_quote"]) not in page:
                    e.append(f"claim {i}: evidence_quote NOT in re-fetched page (fabricated, or page changed)")
    return e


def selftest():
    first = json.loads(next(open(ROOT / "skills.index.jsonl", encoding="utf-8")))
    sid = first["id"]
    d = template(sid, "tester")
    body = find_skill(sid).read_text(encoding="utf-8")
    line = next(x for x in body.splitlines()[12:] if len(x) > 30)[:80]
    url = "https://example.com/x"
    d["reviewed_at"] = "2026-01-01T00:00:00Z"
    d["sources"] = [{"url": url, "fetched_at": "2026-01-01T00:00:00Z", "http_status": 200, "content_sha256": "0" * 64}]
    d["claims"] = [{"claim": line, "verdict": "confirmed", "source_url": url, "evidence_quote": "q"}]
    assert any("mismatch" in x for x in check(d))
    d["attestation_sha256"] = sha(canon(d))
    assert check(d) == [], check(d)
    d["claims"][0]["claim"] = "not in skill"
    d["attestation_sha256"] = sha(canon(d))
    assert any("verbatim" in x for x in check(d))
    d["claims"][0]["claim"] = line
    d["skill"]["sha256"] = "1" * 64
    d["attestation_sha256"] = sha(canon(d))
    assert any("skill sha256" in x for x in check(d))
    print("selftest ok")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "selftest":
        selftest()
    elif a[0] == "template":
        print(json.dumps(template(a[1], a[a.index("--github") + 1] if "--github" in a else ""), indent=2))
    elif a[0] == "seal":
        f = Path(a[1])
        d = json.loads(f.read_text(encoding="utf-8"))
        d["attestation_sha256"] = sha(canon(d))
        f.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    elif a[0] == "check":
        er = check(json.loads(Path(a[1]).read_text(encoding="utf-8")), "--refetch" in a)
        print("\n".join(er) or "ok")
        sys.exit(1 if er else 0)
    else:
        sys.exit(__doc__)
