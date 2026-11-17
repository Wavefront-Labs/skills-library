---
id: computing-software.systems-network-administration.bash.find-by-time-size-and-permissions
name: find-by-time-size-and-permissions
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, find, find-mtime, find-size, find-newer, find-perm, mmin, newermt, find-user, find-empty, find-type, file-management, lfcs, lpic-1, sysadmin]
level: practitioner
status: gated
description: "Select files with find's tests: -mtime/-mmin/-newermt time windows, -size with units and +/- semantics, -perm modes (exact, -all, /any), owner tests, -empty, -type and -links."
sources:
  - https://man7.org/linux/man-pages/man1/find.1.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# find tests — time, size, permission and ownership selectors

**Goal:** express "files changed in the last 2 hours", "bigger than 1 GiB", "world-writable",
"owned by nobody" precisely, knowing how find rounds and what `+`/`-` mean.

## 1. Time
```bash
find /var/log -mtime -1          # modified within the last 24h (less than 1 full day ago)
find /var/log -mtime +7          # modified more than 7 full days ago (8+ days)
find /etc -mmin -120             # last 120 minutes
find /srv -newermt '2026-10-01' ! -newermt '2026-10-08'   # absolute window
find /srv -newer /tmp/marker     # changed after marker's mtime (touch -d '3 hours ago' /tmp/marker)
find / -ctime -1                 # inode change (chmod/chown/rename) — what "last modified" misses
find . -atime +90                # not read in 90 days (only meaningful without noatime/relatime caveats)
```
- `-mtime N` is measured in 24h units with the fraction **discarded**: `-mtime 1` = 24–47h ago.
  `-daystart` makes units align to midnight.
- `-newerXY`: X/Y ∈ a,c,m,t — `-newerct` compares ctime to a timestamp string.
- `relatime` (default mount option) updates atime only if the previous atime is earlier than or equal to mtime/ctime, or more than a day old (mount(8)), so
  `-atime` is coarse; `noatime` disables it entirely.

## 2. Size
```bash
find / -xdev -type f -size +1G                 # more than 1 GiB
find . -size -10k                              # less than 10 KiB — rounds UP to units! see below
find . -size 0  -o -empty                      # empty files and directories
find . -type f -size +100M -printf '%s %p\n' | sort -rn | head
```
- Units: `c` bytes, `k`, `M`, `G` (powers of 1024), none = 512-byte blocks.
- Sizes are rounded **up** to the unit before comparing: `-size -1M` matches only empty
  files (anything 1 byte..1 MiB rounds to 1M, which is not less than 1). Use `-size -1048576c`.
- `-printf '%s'` gives exact bytes, `%k` KiB on disk, `%b` 512-byte blocks (sparse files differ).

## 3. Permissions
```bash
find / -xdev -type f -perm -4000               # setuid (all of these bits set)
find / -xdev -type f -perm -2000               # setgid
find /srv -perm -o+w ! -type l                 # world-writable (Linux symlinks report mode 777 (gated: unconfirmed, source is paywalled or blocked))
find /srv -perm /o+w                           # ANY of the listed bits (here same as above)
find /etc -perm 644                            # exactly 0644
find /home -type d ! -perm -g+s                # directories lacking setgid
find / -xdev -nouser -o -nogroup               # orphaned ownership (deleted users)
find /var/www -user www-data ! -group www-data
```
- `-perm mode`: exact. `-perm -mode`: all bits present. `-perm /mode`: any bit present.
- Symbolic (`-perm -u+x`) and octal are both accepted; `-perm +mode` is no longer supported (deprecated since 2005, find(1)). Permission bits could not be exercised on this NTFS host, so the `-perm` examples rest on the man page.

## 4. Type, links, names
```bash
find . -type l ! -exec test -e {} \; -print    # dangling symlinks  (or: find -L . -type l)
find . -type f -links +1                       # hard-linked files
find . -samefile /etc/passwd                   # same inode
find . -iname '*.JPG' -regex '.*/IMG_[0-9]+\.jpg'   # -regex matches the whole path
find . -type f -name '*.py' -not -path '*/venv/*'
```
`-type` accepts `f d l b c p s`; GNU `-type f,l` matches several.

## 5. Output for reports
```bash
find /home -type f -printf '%TY-%Tm-%Td %TH:%TM %10s %u %p\n' | sort | tail
find . -printf '%M %n %u %g %s %p\n'           # ls -l-like without ls
find . -newermt '-30 minutes' -ls              # -ls: built-in long listing
```

## Failure modes
- Expected recent files missing with `-mtime -1`: cp/rsync `-a` preserved old mtimes — use `-cmin`.
- `-size -1M` returns nothing: rounding (see above).
- Permission denied noise: `2>/dev/null`, or run as root with `-xdev` to avoid `/proc`.
- `-perm -o+w` lists every symlink: exclude `-type l`.

## Verify
- [ ] Spot-check one hit with `stat -c '%y %s %A %U' <file>` — time, size and mode agree with the test.
- [ ] Count with the negated test adds up: `find X -t` + `find X ! -t` == `find X`.
