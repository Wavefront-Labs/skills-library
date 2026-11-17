---
id: computing-software.systems-network-administration.bash.batch-renaming-files
name: batch-renaming-files
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, batch-rename, rename-command, perl-rename, mmv, mv, file-management, parameter-expansion]
level: practitioner
status: gated
description: "Rename many files safely: perl rename vs util-linux rename differences, pure-bash loops with parameter expansion, mmv, dry runs and collision protection."
sources:
  - https://man7.org/linux/man-pages/man1/rename.1.html
  - https://metacpan.org/dist/File-Rename/view/source/rename
  - https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch renaming

## Know your `rename`
| Variant | Check | Syntax |
|---|---|---|
| Perl rename (Debian/Ubuntu `rename`, Arch `perl-rename`) | `rename --version` mentions File::Rename | `rename 's/\.jpeg$/.jpg/' *.jpeg` |
| util-linux rename (RHEL/Fedora/Arch `rename`) | `rename --version` → util-linux | `rename .jpeg .jpg *.jpeg` (plain string, first occurrence) |

```bash
rename -n 's/ /_/g' *               # perl: -n dry run — ALWAYS first
rename -n 'y/A-Z/a-z/' *            # lowercase
rename -n 's/^(\d+)-/sprintf("%03d-",$1)/e' *.mp3   # zero-pad numbers
rename -nv ' ' '_' *                # util-linux: -n -v (2.33+)
```

## Pure bash (portable, no tool differences)
```bash
for f in *.JPG; do
  new="${f%.JPG}.jpg"
  [[ -e $new ]] && { echo "skip: $new exists" >&2; continue; }
  mv -n -- "$f" "$new"
done
# recursive with find:
find . -type f -name '*.log.1' -exec bash -c 'for f; do mv -n -- "$f" "${f%.1}.old"; done' _ {} +
```
## mmv (pattern based)
`mmv '*.jpeg' '#1.jpg'`; `mmv -n` dry run; detects collisions before acting.

## Gotchas
- `mv` overwrites silently — use `-n` (no-clobber) or `-i`; check for duplicates produced by lowercasing.
- `--` before filenames to survive names starting with `-`.
- Filenames with newlines break `ls | while read` loops — use globs or `find -print0`.
- Renaming under version control: `git mv` to keep history obvious.

## Verify
- [ ] Dry run output reviewed; `ls | wc -l` same before and after (no files lost to collisions).

## Checked

- Date: 2026-11-02.
- Source pages listed in `sources` were fetched where possible; rename man page fetched; mmv, perl-rename and the shell loops not covered. Treat the specific names, flags and figures as unconfirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
