---
id: computing-software.systems-network-administration.bash.tar-archives-compression-and-incremental
name: tar-archives-compression-and-incremental
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, tar, archives, tar-compression, tar-incremental, gzip, zstd, xz, listed-incremental, snar, strip-components, exclude, preserve-permissions, xattrs, acls, file-management, lfcs, lpic-1, sysadmin, tar-backup]
level: practitioner
status: gated
description: "Create, list and extract tar archives correctly: compression choice (gzip/zstd/xz), excludes, --strip-components, preserving owners/ACLs/xattrs, verifying, and --listed-incremental backups."
sources:
  - https://www.gnu.org/software/tar/manual/tar.html
  - https://man7.org/linux/man-pages/man1/tar.1.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# tar — archives that restore exactly what you packed

**Goal:** pack a tree so that a later extract reproduces permissions, ownership, links and
attributes; choose the compressor on purpose; and run level-0/level-1 incremental sets.

## 1. Create, list, extract
```bash
tar -cvpzf site-2026-10-16.tgz -C /srv site            # -C: cd first, archive relative paths
tar -tzf site-2026-10-16.tgz | head                     # list (t) — always check before extracting
tar -xzf site-2026-10-16.tgz -C /restore                # extract into a directory
tar -xzf a.tgz --strip-components=1 -C /opt/app         # drop the leading directory
tar -xzf a.tgz site/config                              # extract a subset: a member name (directory recurses)
tar -xzf a.tgz --wildcards 'site/config/*'              # glob members need --wildcards (else "Not found in archive", exit 2)
# -C applies to the member names AFTER it, so put -C before them: tar -xzf a.tgz -C /restore site/config
tar -czf - dir | ssh host 'tar -xzf - -C /dest'         # stream over ssh
```
- Modern GNU tar auto-detects compression on extract (`-xf` works for .gz/.xz/.zst).
- `-p` (`--preserve-permissions`) is the default for the superuser (`tar --help`); other users get the umask applied unless `-p`. `--no-same-owner` extracts files as yourself (the default for ordinary users).
- Archive **relative** paths (`-C /srv site`, not `/srv/site`): GNU tar strips leading `/`
  with a warning, and absolute archives tempt an accidental overwrite of the live tree.

## 2. Compression choice
| flag | tool | notes |
|---|---|---|
| `-z` | gzip | universal; ~1 core; `-I 'pigz -p8'` to parallelise (pigz was not run here (gated: unconfirmed, source is paywalled or blocked)) |
| `--zstd` | zstd | fast, good ratio; `-I 'zstd -T0 -19'` for max (zstd was not run here (gated: unconfirmed, source is paywalled or blocked)) |
| `-J` | xz | best ratio, slow; `-I 'xz -T0'` for threads (the `-I` form tested with xz) |
| `-j` | bzip2 | legacy; avoid for new work |
Extension convention: `.tar.gz/.tgz`, `.tar.zst`, `.tar.xz`. Compressed tars cannot be
appended to (`-r` needs an uncompressed archive).

## 3. Excludes and includes
```bash
tar -czf app.tgz --exclude='*.log' --exclude='./cache' --exclude-vcs -C /srv/app .
tar -czf app.tgz --exclude-from=exclude.txt -C /srv/app .
tar -czf app.tgz --exclude-caches-all --exclude-tag-all=.nobackup -C /srv app
```
Exclude patterns match against the path as it appears in the archive (hence `./cache`
when archiving `.`). Put `--exclude` **before** the paths; after them GNU tar 1.35 warns
"--exclude '*.log' has no effect" and archives everything (tested).

## 4. Preserving everything
```bash
tar --xattrs --acls --selinux -cpzf full.tgz -C / etc home   # root only; needs a build with those features (the tar 1.35 tested here accepted --xattrs/--acls but reported "SELinux support is not available")
tar --numeric-owner -cpzf sys.tgz ...   # keep UIDs, not names — for restores onto other hosts
tar -cpzf f.tgz --one-file-system /     # don't descend into /proc, /sys, NFS mounts
```
Hard links are stored as links (restored correctly if both members are in the same archive);
sparse files need `-S` to stay sparse.

## 5. Incremental with --listed-incremental
```bash
tar --listed-incremental=/var/backups/home.snar -cpzf home-L0.tgz -C / home   # level 0 (full)
cp /var/backups/home.snar /var/backups/home.snar-0                              # keep the L0 state
tar --listed-incremental=/var/backups/home.snar -cpzf home-L1-$(date +%F).tgz -C / home  # next = L1
# restore: extract L0 then each L1 in order, each with --listed-incremental=/dev/null
tar -xpzf home-L0.tgz --listed-incremental=/dev/null -C /restore
tar -xpzf home-L1-2026-10-17.tgz --listed-incremental=/dev/null -C /restore
```
- The `.snar` file is mutated by every run (tested: a second run archived only changes since the first); to repeat "differential from L0" copy the L0
  snar back before each run (tested: the L1 then contained everything changed since L0).
- Incrementals record deletions, so restoring in order removes files that vanished.
- Changing `-C` or the path form between runs can make tar treat everything as new (gated: unconfirmed, source is paywalled or blocked).

## 6. Verify and compare
```bash
tar -tzvf f.tgz >/dev/null && echo archive readable
tar -dzf f.tgz -C /srv                 # --diff: report differences vs filesystem
gzip -t f.tgz                          # compressed stream integrity
sha256sum f.tgz > f.tgz.sha256
```

## Failure modes
- "Cannot open: No such file" during create: paths relative to the wrong directory — `-C`.
- Extract overwrote newer files: add `--keep-newer-files` (skip only newer ones) or `-k` (never replace existing files; errors "Cannot open: File exists").
- "tar: Removing leading '/' from member names": informational; or you archived absolute paths.
- Timestamps in the future warnings: clock skew between hosts; harmless but `make` may loop (gated: unconfirmed, source is paywalled or blocked).
- Ownership all root after restore: extracted as non-root or `--no-same-owner`.

## Verify
- [ ] `tar -tf` lists expected relative paths with no leading `/`.
- [ ] Extract to a scratch dir and `diff -r`/`rsync -nic` against the source shows no differences.
- [ ] For incrementals: a file deleted between L0 and L1 is absent after sequential restore.
