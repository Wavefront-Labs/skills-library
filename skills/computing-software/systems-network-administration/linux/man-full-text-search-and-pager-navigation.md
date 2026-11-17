---
id: computing-software.systems-network-administration.linux.man-full-text-search-and-pager-navigation
name: man-full-text-search-and-pager-navigation
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, man-k, man-pages, manpager, man-k-full-text, less-navigation, apropos, lpic-1]
level: intro
status: docs-checked
description: "Find answers inside man pages fast: man -k vs man -K full-text search, man -f, jumping sections in less, MANPAGER/MANWIDTH, and printing pages to PDF or text."
sources:
  - https://manpages.debian.org/trixie/man-db/man.1.en.html
  - https://manpages.debian.org/trixie/man-db/mandb.8.en.html
  - https://github.com/gwsw/less
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Searching and navigating man pages

## Find the page
```bash
man -k 'partition table'        # = apropos: searches NAME lines (needs mandb index)
man -f crontab                  # = whatis: which sections have crontab → crontab(1), crontab(5)
man 5 crontab                   # pick section explicitly
man -K 'ProtectSystem'          # full-text search across ALL page sources (slow)
man -a passwd                   # show every matching page in turn
```

## Inside less (default pager)
| Key | Action |
|---|---|
| `/pattern` `n` `N` | search forward, next, previous |
| `/^ +-r` | jump to an option's definition (options are indented) |
| `/^[A-Z]` | jump between section headings (NAME, SYNOPSIS, EXAMPLES...) |
| `g` / `G` | top / bottom |
| `&pattern` | show only matching lines |
| `-N` Enter | toggle line numbers (`-N` / `--LINE-NUMBERS`) |
| `h` | less help |
Open straight at a term: `man -P 'less -p ^EXAMPLES' rsync` or `LESS='+/--delete' man rsync`.

## Environment
- `MANPAGER` takes precedence over `PAGER` for choosing the pager, e.g. `MANPAGER='less -R'`.
- `MANWIDTH=80` sets the line length for formatting; `MANOPT` is parsed before the command line; `MANPATH` is the search path.

## Output
```bash
man -Tpdf rsync > rsync.pdf            # pdf is a groff device (needs groff PDF support)
man rsync | col -b > rsync.txt         # plain text without backspace overstrikes
man -l ./mytool.1                      # view a local page file
```

## Gotchas
- Empty `man -k` results → index missing: run `mandb` (root).
- Minimal containers often strip man pages — read them on a full host or online at man7.org.

## Verify
- [ ] You can go from a keyword to the exact option paragraph in under a minute using `-k`/`-K` and `/^ +-opt`.

## Checked
2026-10-27. Checked against Debian man(1) and mandb(8) (man-db, trixie) and the less manual source (gwsw/less). Confirmed: man -k, -f, -K, -a, -l, -T, -P; MANPAGER over PAGER, MANWIDTH, MANOPT, MANPATH; mandb builds the index; less keys /, h, g, G, &pattern, -N and -p, and +cmd. Removed: the per-hit prompt keys for -K, the unverified man -wK combination, the coloured MANPAGER recipe and the man-db.timer and dpkg exclusion remarks. The less link in sources now points to the upstream manual.

Method: documentation only; no commands were run.
