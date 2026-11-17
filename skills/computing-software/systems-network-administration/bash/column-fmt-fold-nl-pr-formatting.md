---
id: computing-software.systems-network-administration.bash.column-fmt-fold-nl-pr-formatting
name: column-fmt-fold-nl-pr-formatting
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, column-t, fmt-fold, nl-command, pr-command, text-formatting, expand-unexpand, lpic-1]
level: intro
status: verified
description: "Format text output for humans: column -t tables, fmt/fold wrapping, nl line numbering, pr paging/columns, expand/unexpand tabs (LPIC-1 103.2 text filters)."
sources:
  - https://www.gnu.org/software/coreutils/manual/html_node/Formatting-file-contents.html
  - https://man7.org/linux/man-pages/man1/column.1.html
  - https://www.gnu.org/software/coreutils/manual/html_node/nl-invocation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# column, fmt, fold, nl, pr

## Tables with column
```bash
mount | column -t
column -t -s: /etc/passwd | less -S                  # -s input separator
printf 'NAME SIZE\nroot 20G\nvar 100G\n' | column -t -R 2   # right-align column 2 (util-linux)
lsblk -o NAME,SIZE,MOUNTPOINT | column -t -N A,B,C -J     # -J JSON output (tested on util-linux 2.35.2; the release that added -J/-N/-R is unconfirmed, it is not in the 2.33 release notes)
```
## Wrapping
```bash
fmt -w 72 notes.txt          # reflow paragraphs (joins and wraps)
fold -w 80 -s long.log       # hard-wrap at width, -s breaks at spaces; doesn't join lines
```
## Numbering
```bash
nl -ba script.sh              # number all lines (default skips blank: -bt)
nl -nrz -w3 -s'  ' file       # zero-padded 3-wide, custom separator
cat -n file                    # simpler alternative
```
## Paging/print layout
```bash
pr -3 -t -w 120 list.txt      # 3 columns, no header, width 120
pr -h "Inventory" -l 60 file  # header, 60 lines per page
pr -m -t a.txt b.txt          # merge files side by side
```
## Tabs
`expand -t 4 file` tabs→spaces; `unexpand -a -t 4` spaces→tabs (Makefiles need real tabs).

## Gotchas
- `column -t` splits on any whitespace by default — fields with spaces break alignment; use `-s` with a real delimiter.
- `-N/-R/-J` are util-linux options; other `column` implementations may not have them (check `column --version`).
- Multibyte/UTF-8 widths can misalign in `fold`/`pr` (byte-based in some versions).

## Verify
- [ ] Output aligns in an 80-column terminal; scripts that parse output don't rely on column-padded spacing.
