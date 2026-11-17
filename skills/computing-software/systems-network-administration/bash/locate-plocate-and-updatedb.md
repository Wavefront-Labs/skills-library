---
id: computing-software.systems-network-administration.bash.locate-plocate-and-updatedb
name: locate-plocate-and-updatedb
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, locate, plocate, mlocate, updatedb, updatedb-conf, prunepaths, prunefs, file-search, file-management, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Find files by name with locate/plocate: how the database is built, updatedb.conf PRUNEPATHS/PRUNEFS tuning, regex and -e existence checks, and why results are stale or missing."
sources:
  - https://plocate.sesse.net/
  - https://man7.org/linux/man-pages/man1/locate.1.html
  - https://man.archlinux.org/man/updatedb.conf.5
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# locate / plocate - name search from an index instead of walking the disk

**Goal:** answer "where is a file called X" quickly, keep the index scoped, and know when to fall back to `find`.

## 1. How it works
- `locate` searches databases of file names built earlier by `updatedb`; the lists reflect the system when the database was last updated.
- plocate replaces mlocate with a posting-list index: an inverted index over trigrams (three-byte combinations), so it narrows candidates instead of scanning every entry. Its own example shows the database at /var/lib/plocate/plocate.db against /var/lib/mlocate/mlocate.db for mlocate.
- Like mlocate and slocate, results are user-dependent: a user sees a file only if `find` would list it (all directories from the root have +rx permission).

## 2. Querying (options from the GNU findutils locate man page)
```bash
locate sshd_config                 # plain string: names containing it anywhere
locate -i 'readme'                 # ignore case
locate -b 'sshd_config'            # match the final path component only
locate -r '/etc/.*\.conf$'         # regular expression; anchor with ^ and $
locate -e '*.pem'                  # only names that currently exist
locate -c pattern                  # count instead of printing
locate -l 20 pattern               # limit matches
locate -0 '*.log' | xargs -0 ls -l # NUL separators
```
- A plain string matches names containing it. A pattern with metacharacters (`*`, `?`, `[]`) must match the whole name, so such patterns usually start and end with `*`; metacharacters do not treat `/` or `.` specially. Quote patterns so the shell does not expand them.
- `-e` checks existence at query time and can slow the query a lot with many matches; the file can still vanish before you use it.
- `-d path` (colon-separated) or `LOCATE_PATH` selects other databases; `-S` prints database statistics.
- GNU locate warns when a database is more than 8 days old; `--max-database-age` changes that.
- Use `-0` when names may contain newlines. plocate has its own man pages (plocate(1), updatedb(8)); option sets differ from the GNU page, so check `man locate` on your system.

## 3. Tuning updatedb (/etc/updatedb.conf)
Format is `VARIABLE = "VALUE"`, one per line, no escapes, unknown variables are an error.
```
PRUNE_BIND_MOUNTS = "yes"
PRUNEFS = "nfs nfs4 cifs tmpfs"
PRUNEPATHS = "/tmp /var/tmp"
PRUNENAMES = ".git node_modules"
```
- `PRUNEFS`: file-system types not scanned, matched case-insensitively; by default none are skipped. Anything mounted under a skipped file system is skipped too.
- `PRUNENAMES`: directory names without paths, no globbing; default none.
- `PRUNEPATHS`: directories, written exactly as `locate` would report them; default none. It cannot exclude non-directory files in this implementation.
- `PRUNE_BIND_MOUNTS`: `0`, `no`, `1` or `yes`; if on, bind mounts are not scanned (a bind mount of a directory on itself is not skipped); default off. Btrfs subvolume mounts can count as bind mounts.
- A pruned directory is still entered in the database, so `locate` can show `/tmp` itself but not its contents.
- A distribution may ship a populated updatedb.conf, so read yours rather than assuming defaults.

## 4. Freshness
Files created after the last `updatedb` run are not found; files deleted since stay listed unless you use `-e`. Run `updatedb` as root to refresh.

## 5. locate vs find
- Name-only lookup across the whole system: `locate`.
- Size, time, permissions, content, or files newer than the last index: `find`.

## Failure modes
- Empty or missing database: `updatedb` has not run yet (path differs between mlocate and plocate).
- Files on a network or bind mount are missing: check PRUNEFS and PRUNE_BIND_MOUNTS in your updatedb.conf.
- Users see less than root: results are filtered by directory permissions, by design.
- Huge or slow database: large churning trees (container layers, caches) are not pruned.

## Verify
- [ ] `locate -S` (GNU) shows statistics for the database; check your implementation's man page for plocate.
- [ ] A file created after `updatedb` is found only after the next run.

## Checked
Checked 2026-11-08 against the plocate home page (trigram index, user-dependent results, database paths), the GNU findutils locate(1) page (patterns, -b/-e/-r/-c/-l/-0/-d/-S, LOCATE_PATH, 8-day warning) and updatedb.conf(5) (variables, defaults, prune notes). Removed because the pages do not give them: package install commands, timer unit names, `updatedb -U -o` overrides, setgid detail, the claim that network filesystems are pruned by default (the page says nothing is pruned by default), the `\` basename-exact trick and the `plocate --statistics` flag.

Method: docs-only read of cited pages, 2026-11-08
