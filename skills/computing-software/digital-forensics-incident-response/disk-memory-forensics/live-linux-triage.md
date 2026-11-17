---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.live-linux-triage
name: live-linux-triage
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [proc-filesystem, live-response, linux-forensics, deleted-binary, hidden-process, volatile-data, dfir]
level: practitioner
status: draft
description: "Triage a live Linux system: processes via /proc, deleted-but-running binaries, network sockets, open files, hidden processes, and collecting volatile data with trusted tools."
sources: ["https://man7.org/linux/man-pages/man5/proc.5.html", "https://github.com/tclahr/uac", "https://www.sans.org/cyber-security-courses/linux-threat-hunting-incident-response/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Live Linux triage

**Goal:** capture volatile evidence and spot malicious processes on a running Linux host
before containment, using trusted tools and /proc directly.

## Prepare
Use statically linked tools from your own media (busybox, static `ss`/`lsof` builds) or UAC;
write output to external storage or stream over the network (`| nc collector 9000`). Capture
memory first if possible (LiME/AVML).

## Processes
```bash
ps auxwwf                                 # tree with full args (may be trojaned; compare with /proc)
ls -la /proc/*/exe 2>/dev/null | grep -E '\(deleted\)|/tmp/|/dev/shm/|/var/tmp/'
for p in /proc/[0-9]*; do echo "$p $(tr '\0' ' ' < $p/cmdline)"; done
cat /proc/<pid>/environ | tr '\0' '\n'    # LD_PRELOAD, attacker env
ls -la /proc/<pid>/fd/                    # open files and sockets
cat /proc/<pid>/maps                      # loaded libraries, anonymous executable regions
```
- **Deleted binary still running**: recover it with `cp /proc/<pid>/exe /evid/pid.bin` and hash.
- **Hidden processes** (userland rootkit hiding from ps): compare PIDs in `/proc` with `ps`
  output; also check `/etc/ld.so.preload`. Kernel rootkits need memory analysis.
- Process names faking kernel threads (`[kworker/0:1]`) but with an `exe` link: kernel
  threads have no exe.

## Network
```bash
ss -tunap        # sockets with owning process
cat /proc/net/tcp /proc/net/tcp6   # raw, if ss is untrusted
ip a; ip r; ip neigh; iptables-save; nft list ruleset
```

## Other volatile items
Logged-in users (`w`, `last -F | head`), `lsmod`, mounted filesystems, `crontab -l` per user,
`/tmp` and `/dev/shm` listings, shell history files of active users, `systemctl list-units --state=running`.

## Gotchas
- Every command you run changes the system; log it (see responder footprint).
- Container hosts: processes in namespaces; use `nsenter` or container runtime tools to
  inspect, and note container IDs in `/proc/<pid>/cgroup`.

## Verify
Recovered binaries hashed, process list from /proc and ps reconciled, and all output files
hashed with collection times recorded.
