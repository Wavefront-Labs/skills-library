---
id: computing-software.software-engineering.git.export-and-linguist-attributes
name: export-and-linguist-attributes
category: computing-software
field: software-engineering
product: git
tags: [git, export-ignore, linguist-attributes, gitattributes, export-subst, linguist-generated, git-archive]
level: practitioner
status: verified
description: "Control release tarballs and host behaviour with .gitattributes: export-ignore and export-subst for git archive, and linguist-generated/vendored/language overrides for GitHub."
sources: ["https://git-scm.com/book/en/v2/Customizing-Git-Git-Attributes", "https://git-scm.com/docs/gitattributes#_creating_an_archive", "https://github.com/github-linguist/linguist/blob/main/docs/overrides.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Export and linguist attributes

**Goal:** release archives contain only what users need, and the host's language
stats, diffs and PR views ignore generated or vendored code.

## git archive attributes
```gitattributes
/.github         export-ignore
/tests           export-ignore
.gitattributes   export-ignore
.gitignore       export-ignore
/VERSION         export-subst
```
`export-subst` expands `$Format:...$` placeholders (same as `git log --pretty`) at archive time:
```
VERSION file content:  $Format:%H %cd$
```
```bash
git archive --format=tar.gz --prefix=app-1.4.0/ -o app-1.4.0.tar.gz v1.4.0
tar tzf app-1.4.0.tar.gz | head     # confirm tests/ absent
```
Attributes are read from the tree being archived (the tag), so the `.gitattributes` must be
committed before tagging (checked: with `export-subst` and `tests export-ignore`, the archive had `$Format:%h$` expanded and no `tests/`). Other archive producers (package registries, module zips) may apply their own rules; check their docs.

## Linguist overrides (GitHub language bar and diffs)
```gitattributes
docs/**                 linguist-documentation
vendor/**               linguist-vendored
src/gen/**              linguist-generated=true     # collapsed in PR diffs, excluded from stats
*.pb.go                 linguist-generated
*.sql                   linguist-detectable=true
*.inc                   linguist-language=PHP
third_party/**          -linguist-vendored          # count it after all
```
`linguist-generated` files are excluded from stats and hidden in diffs per the Linguist overrides doc (https://github.com/github-linguist/linguist/blob/main/docs/overrides.md), a big review
win for lockfiles and codegen; reviewers can still expand them.

## Related attributes in the same file
- `binary` (= `-diff -merge -text`) for assets.
- `merge=ours` with `git config merge.ours.driver true` to keep your version of a file on merge.
- `diff=<driver>` for textconv.

## Gotchas
- Patterns follow gitignore rules but a leading `/` anchors to the directory of the
  `.gitattributes`; `dir/` (trailing slash) does not match in attributes - use `dir/**`.
- Check what applies: `git check-attr -a -- path/to/file`.
- Linguist changes appear on GitHub only after a push to the default branch.

## Verify
- [ ] `git archive HEAD | tar t` lists no CI, test or dev-only files.
- [ ] `git check-attr linguist-generated -- src/gen/x.go` prints `set`/`true`.
