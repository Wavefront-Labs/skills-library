---
id: computing-software.software-engineering.git.clean-and-smudge-filters
name: clean-and-smudge-filters
category: computing-software
field: software-engineering
product: git
tags: [git, clean-smudge-filter, gitattributes, keyword-expansion, filter-process, notebook-output-stripping]
level: advanced
status: verified
description: "Transform files on add and checkout with clean/smudge filters: keyword expansion, stripping notebook outputs, required filters and filter processes."
sources: ["https://git-scm.com/book/en/v2/Customizing-Git-Git-Attributes", "https://git-scm.com/docs/gitattributes#_filter", "https://github.com/kynan/nbstripout"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clean and smudge filters

**Goal:** store a normalised form in the repo while the working tree holds a convenient
form, e.g. Jupyter notebooks without outputs, or a `$Date$` keyword filled at checkout.

## Model
- **clean**: runs on `git add`; working-tree content -> stdin, stored blob <- stdout.
- **smudge**: runs on checkout; blob -> stdin, working file <- stdout.
- Declared in `.gitattributes` (committed); commands defined in config (NOT committed,
  each clone must set them - a deliberate security boundary).

```gitattributes
*.ipynb filter=nbstrip
*.c     filter=dater
```
```bash
git config filter.nbstrip.clean "nbstripout"
git config filter.nbstrip.smudge cat
git config filter.nbstrip.required true    # fail add/checkout if the filter errors or is missing
```
`nbstripout --install` writes this config for you (clean = `python -m nbstripout`, smudge `cat`, required true) but puts the attribute lines in `.git/info/attributes` (local, not committed) unless you pass `--attributes .gitattributes`.

## Keyword expansion example (Pro Git)
```bash
git config filter.dater.clean  'sh /path/clean_date.sh'    # perl -pe 's/\$Date[^\$]*\$/\$Date\$/'
git config filter.dater.smudge 'sh /path/expand_date.sh'   # perl -pe 's/\$Date\$/\$Date: today\$/'
```
Keep the commands in script files: an inline `perl -pe "...$Date..."` in the config value loses the
`$Date` to shell expansion and fails. Verified: the stored blob has `$Date$`, a fresh checkout has `$Date: today$`.
Clean must exactly undo smudge, or files show as modified forever.

## Rules for well-behaved filters
- Idempotent: `clean(clean(x)) == clean(x)`; `clean(smudge(b)) == b`.
- Read all stdin, write all stdout, exit 0. `%f` passes the path as an argument.
- Fast: invoked per file on add/checkout/status. For many files use a long-running
  `filter.<name>.process` (the protocol Git LFS uses) instead of spawning per file.
- Never depend on files outside the blob content for clean output (breaks determinism).

## After adding or changing a filter
Existing files are not reprocessed until touched:
```bash
git add --renormalize .        # re-run clean on all tracked files
git commit -m "Apply nbstrip filter"
```
Other clones see phantom changes until they configure the filter; document setup in
README or a bootstrap script.

## Pitfalls
- Secrets via smudge (decrypt on checkout, e.g. git-crypt): clean must re-encrypt
  deterministically or every `git status` shows changes.
- CI without the filter configured checks out the raw (cleaned) form; usually fine.
- `git diff` compares cleaned content; use `diff.<name>.textconv` for readable diffs.

## Verify
- [ ] `git status` clean right after checkout and after `git add --renormalize .`.
- [ ] `git show HEAD:nb.ipynb | grep -c '"outputs": \[\]'` confirms stored form.
