#!/usr/bin/env python3
"""lint - validate every skill file against SCHEMA.md.
Run: python tools/lint.py [--changed-since origin/main]   (exit 1 on any error)
  --changed-since REF: also check no published id vanished and changed skills bumped `version`.
"""
import sys, re, subprocess
from datetime import date
from pathlib import Path
from reindex import parse_frontmatter, SKILLS, ROOT
from serve import LICENCE_NOTICES

LICENCES = set(LICENCE_NOTICES)

LEVELS = {"intro", "practitioner", "advanced", "sme"}
STATUS = {"stub", "draft", "unreviewed-low-risk", "gated", "docs-checked", "verified"}
KEBAB = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
REQUIRED = ("id", "name", "category", "field", "product", "tags", "level", "status", "description",
            "licence", "version", "updated")
ID_RE = re.compile(r'^[a-z0-9-]+(\.[a-z0-9-]+){3}$')
# a drive-letter path like D:/x or C:\x is a machine path; URLs (https://) and placeholders (<DRIVE>:/) don't match
# a writer correcting itself mid-sentence ("`Ctrl L`? no — use ...", "`--flag`? No, ...") left in the published text
SELF_CORRECTION = re.compile(r"[`)\]]\?\s*(?:no|not)\b\s*(?:[—–-]|\)|,|\.)", re.I)
ABS_PATH = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/](?=[A-Za-z0-9_.~-])|/(?:Users|home)/[A-Za-z]")


def canonical_categories():
    """The backticked names under '## Canonical categories' in SKILLS.md."""
    text = (ROOT / "SKILLS.md").read_text(encoding="utf-8")
    m = re.search(r'^## Canonical categories.*?$(.*?)(?=^## |\Z)', text, re.S | re.M)
    return set(re.findall(r'`([a-z0-9-]+)`', m.group(1))) if m else set()


def published_checks(ref, live_ids, alias_of, versions):
    """Against git ref (e.g. origin/main): ids never disappear (a moved skill keeps its old id in
    `aliases`), and a changed skill bumps `version`."""
    def git(*a):
        return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True).stdout
    errs = []
    for path in git("ls-tree", "-r", "--name-only", ref, "skills").splitlines():
        if not path.endswith(".md") or path.endswith("/INDEX.md"):
            continue
        old = parse_frontmatter(git("show", f"{ref}:{path}")) or {}
        oid = old.get("id") or ".".join(Path(path).with_suffix("").parts[1:])
        if oid not in live_ids and oid not in alias_of:
            errs.append(f"{path}: published id '{oid}' is gone; add it to the moved skill's `aliases`")
            continue
        if oid in live_ids and (ROOT / path).exists() and (ROOT / path).read_text(encoding="utf-8") != git("show", f"{ref}:{path}"):
            if int(versions.get(oid) or 0) <= int(old.get("version") or 0):
                errs.append(f"{path}: changed since {ref} but version not bumped (was {old.get('version') or 'unset'})")
    return errs


def main():
    errors = []
    seen_ids, alias_of, versions = {}, {}, {}
    cats = canonical_categories()
    if not cats:
        errors.append("SKILLS.md: no '## Canonical categories' list found")
    for p in sorted(SKILLS.rglob("*.md")):
        if p.name.upper() == "INDEX.MD":
            continue
        rel = p.relative_to(SKILLS).as_posix()
        parts = rel.split('/')
        def err(msg): errors.append(f"{rel}: {msg}")
        if len(parts) != 4:
            err(f"path must be <category>/<field>/<product>/<name>.md (got {len(parts)} levels)")
            continue
        cat, field, prod, _ = parts
        for seg in (cat, field, prod, p.stem):
            if not KEBAB.match(seg):
                err(f"segment '{seg}' not lowercase-kebab-case")
        if cats and cat not in cats:
            err(f"category '{cat}' is not in the canonical list in SKILLS.md")
        text = p.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if not fm:
            err("missing/invalid frontmatter"); continue
        for n, line in enumerate(text.splitlines(), 1):
            if ABS_PATH.search(line):
                err(f"line {n}: machine-specific path '{ABS_PATH.search(line).group(0)}...' (use a placeholder like <TOOLS_DIR>)")
            if SELF_CORRECTION.search(line):
                err(f"line {n}: unfinished self-correction '{SELF_CORRECTION.search(line).group(0)}' (state the right answer only)")
        for req in REQUIRED:
            if not fm.get(req):
                err(f"missing required field '{req}'")
        for key, want in (('category', cat), ('field', field), ('product', prod), ('name', p.stem)):
            if fm.get(key) and fm[key] != want:
                err(f"{key} '{fm[key]}' != path '{want}'")
        sid = f"{cat}.{field}.{prod}.{p.stem}"
        if fm.get('id') and fm['id'] != sid:
            err(f"id '{fm['id']}' != '{sid}'")
        if fm.get('level') and fm['level'] not in LEVELS: err(f"bad level '{fm['level']}'")
        if fm.get('status') and fm['status'] not in STATUS: err(f"bad status '{fm['status']}'")
        if fm.get('licence') and fm['licence'] not in LICENCES:
            err(f"licence '{fm['licence']}' has no notice in tools/serve.py LICENCE_NOTICES")
        tags = fm.get('tags')
        if tags and not isinstance(tags, list): err("tags must be a list")
        elif tags and any(t != t.lower() or not t.strip() for t in tags): err("tags must be non-empty and lowercase")
        desc = fm.get('description', '')
        if len(desc) > 200: err("description > 200 chars")
        if '\n' in desc: err("description must be one line")
        if desc.upper().startswith('TODO'): err("description is still the TODO placeholder")
        if fm.get('version') and not fm['version'].isdigit(): err(f"version '{fm['version']}' must be a whole number")
        if fm.get('updated'):
            try: date.fromisoformat(fm['updated'])
            except ValueError: err(f"updated '{fm['updated']}' must be a YYYY-MM-DD date")
        aliases = fm.get('aliases', [])
        if not isinstance(aliases, list) or any(not ID_RE.match(a) for a in aliases):
            err("aliases must be a list of old ids like category.field.product.name")
        else:
            for a in aliases:
                if a in alias_of: err(f"alias '{a}' also claimed by {alias_of[a]}")
                alias_of[a] = rel
        if sid in seen_ids:
            err(f"duplicate id '{sid}' (also {seen_ids[sid]})")
        seen_ids[sid] = rel
        versions[sid] = fm.get('version', '')
    for a, rel in alias_of.items():
        if a in seen_ids: errors.append(f"{rel}: alias '{a}' is a live id ({seen_ids[a]})")
    if "--changed-since" in sys.argv:
        errors += published_checks(sys.argv[sys.argv.index("--changed-since") + 1], seen_ids, alias_of, versions)
    if errors:
        print(f"LINT FAILED ({len(errors)} errors):")
        for e in errors:
            print("  ", e)
        sys.exit(1)
    print(f"lint OK ({len(seen_ids)} skills)")


if __name__ == "__main__":
    main()
