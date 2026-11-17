---
id: computing-software.systems-network-administration.linux.fuser-and-lsof-who-holds-files-and-ports
name: fuser-and-lsof-who-holds-files-and-ports
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, fuser, lsof-usage, lsof, device-busy, umount-busy, open-files, port-owner]
level: practitioner
status: docs-checked
description: "Find which processes hold a file, mount or port with fuser and lsof: target is busy on umount, deleted-but-open files, port owners, and killing safely."
sources:
  - https://manpages.debian.org/trixie/psmisc/fuser.1.en.html
  - https://github.com/lsof-org/lsof/blob/master/Lsof.8
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fuser and lsof

## "umount: /mnt/data: target is busy"
```bash
fuser -vm /mnt/data            # every process using anything on that filesystem (-m), verbose
#                 USER  PID ACCESS COMMAND
# /mnt/data:      alice 2210 ..c.. bash        (c = cwd, e = executable, f = open file, F = open for writing, m = mmap or library, r = root)
lsof +f -- /mnt/data           # same via lsof (mount point)
lsof +D /srv/app               # everything open under a directory (recursive; slow on big trees)
fuser -km /mnt/data            # -k sends SIGKILL by default — last resort; prefer asking/stopping services
umount -l /mnt/data            # lazy unmount (umount(8)): hides the problem, find the holder first
```
Often the culprit is your own shell's cwd, an NFS client process, or a systemd service.

## Ports
```bash
fuser -v 8080/tcp
lsof -nP -iTCP:8080 -sTCP:LISTEN
lsof -nP -i @10.0.0.5          # connections to a host
ss -ltnp 'sport = :8080'       # often faster and always installed
```
## Files
```bash
lsof /var/log/app.log          # who has it open (e.g. after logrotate without reload)
lsof -p 1234                   # all files of a process
lsof -u postgres -a -d cwd     # AND with -a
lsof +L1                       # deleted but still open (disk not freed)
lsof -nP -c nginx              # by command name
```
`-n -P` skip DNS/port name lookups — much faster.

## Gotchas
- Without root you may only see your own processes — results can look empty.
- `lsof` can be blocked by some kernel functions (stat, lstat on hung file systems); `-b` avoids calls that might block (lsof(8)).
- Containers: processes appear with host PIDs on the host.

## Verify
- [ ] After stopping the reported processes, `fuser -vm` is empty and `umount` succeeds.

## Checked
2026-10-27. Checked against the Debian trixie fuser(1) page (psmisc 23.7) and the lsof manual source (lsof-org/lsof Lsof.8). Confirmed: fuser -m, -v with ACCESS letters c, e, f, F, r, m, -k default SIGKILL, the 80/tcp style port form; lsof +f -- for a file system, +D recursive search, +L1 for unlinked open files, -n and -P, -b to avoid blocking kernel calls, -c, -d, -p, -u, -a, -i @host. Removed: the nsenter remark and the claim that results are empty without root (softened) because the documents do not state them. The man7.org links in sources were replaced because man7.org does not host these pages.

Method: documentation only; no commands were run.
