---
id: computing-software.systems-network-administration.linux.capabilities-vs-root
name: capabilities-vs-root
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, capabilities, setcap, getcap, cap-net-bind-service, cap-sys-admin, suid, privilege-escalation, ambient-capabilities, file-capabilities, prctl, least-privilege, security, sysadmin]
level: advanced
status: docs-checked
description: "Grant a process exactly the privilege it needs with Linux capabilities (setcap/getcap) instead of full root or a SUID binary."
sources:
  - https://man7.org/linux/man-pages/man7/capabilities.7.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux capabilities — root, split into pieces

**Goal:** give a process the one or two privileged operations it genuinely
needs (bind to port 80, adjust the system clock, trace another process)
without running it as root or making its binary SUID — and understand why
"just chmod it SUID" is the pattern capabilities exist to replace.

## 1. The problem capabilities solve
Historically, any operation needing privilege (binding a low port, raising
process priority, raw sockets) required the whole process to run as UID 0,
or the binary to be SUID root (so any user running it gets full root for
the process's lifetime). Both hand over *all* of root's power for a
*single* needed permission. Capabilities split root's power into
discrete units — a process can hold exactly the one it needs and nothing
else, even while running as an unprivileged UID.

## 2. Checking and granting capabilities on a binary
```bash
getcap /usr/bin/ping                 # shows capabilities baked into the binary itself
sudo setcap 'cap_net_raw+ep' /usr/bin/ping     # grant: raw sockets, effective+permitted
sudo setcap 'cap_net_bind_service=+ep' /opt/app/myserver   # bind ports <1024 as a non-root user
getcap -r /usr/bin                    # recursively audit every capability-bearing binary on the box
```
`+ep` means **e**ffective (active immediately on exec) and **p**ermitted
(allowed to be made effective) — the combination almost always wanted for
"just make this work." A capability that's `permitted` but not `effective`
has to be explicitly raised by the process itself (via `prctl`/`libcap`),
which most ordinary binaries never bother doing — if a `setcap`'d binary
still fails with `EPERM`, check the exact flags with `getcap`, not just
whether something is "capable" at all.

## 3. The capabilities worth actually knowing
| Capability | Grants | Common use |
|---|---|---|
| `CAP_NET_BIND_SERVICE` | bind ports < 1024 | a web server running as non-root needing port 80/443 |
| `CAP_NET_RAW` | raw/packet sockets | `ping`, packet capture tools |
| `CAP_NET_ADMIN` | network config (interfaces, routes, firewall) | software needing to manage its own interfaces |
| `CAP_SYS_PTRACE` | `ptrace()` another process | debuggers, strace, APM/profiling agents |
| `CAP_SYS_ADMIN` | **huge grab-bag** — mount, many ioctls, more | avoid; it's "almost root," audit anything requesting it closely |
| `CAP_CHOWN` | change file ownership arbitrarily | package managers, backup/restore tools |
| `CAP_DAC_OVERRIDE` | bypass file read/write/execute permission checks | also a huge footgun — almost full DAC bypass |
| `CAP_SETUID`/`CAP_SETGID` | change process UID/GID | process supervisors dropping privilege after start |

**`CAP_SYS_ADMIN` and `CAP_DAC_OVERRIDE` are the two to be suspicious of** —
each covers so much ground that granting either is not meaningfully
different from granting root for most practical attack-surface purposes.
A request for one of these is a signal to ask whether a narrower capability
(or a namespace-based approach instead) actually covers the real need.

## 4. Ambient capabilities — surviving `execve()` without SUID
```bash
setcap 'cap_net_bind_service=+eip' /opt/app/myserver
# or programmatically: prctl(PR_CAP_AMBIENT, PR_CAP_AMBIENT_RAISE, CAP_NET_BIND_SERVICE, 0, 0)
```
Before ambient capabilities (Linux 4.3+), a non-root process's capabilities
were lost across `execve()` of a non-capability-aware child unless the
binary itself was SUID or had file capabilities set — meaning a supervisor
process (systemd, a custom launcher) that wanted to hand down a capability
to a plain script couldn't, without SUID. Ambient capabilities fix this:
they're preserved across exec for non-SUID, non-capability-aware
executables, which is what lets systemd's `AmbientCapabilities=` directive
work:
```ini
[Service]
AmbientCapabilities=CAP_NET_BIND_SERVICE
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
User=myapp
```
This is the modern, preferred way to grant a capability to a systemd
service — narrower and more auditable than `setcap` on the binary itself,
and it survives a binary update (the capability lives in the unit file, not
re-attached to a replaced file's extended attributes).

## 5. Gotchas
- **`setcap` capabilities on a binary are extended-file attributes** — they
  vanish on copies that don't preserve xattrs (they live in the
  `security.capability` attribute), and can be lost by packaging or CI
  pipelines that don't keep xattrs, unless explicitly reapplied post-install —
  a very common "it worked in testing, broke after deployment" cause.
- A capability-bearing binary combined with world-writable permissions or a
  writable `PATH` ahead of it is a privilege escalation path just like a
  SUID binary would be — capabilities narrow *what* privilege is available,
  they don't make a mistake in file permissions safe.
- Capabilities are **per-process**, dropped by `fork()`+`exec()` of a
  non-capability-aware child unless ambient capabilities or explicit
  `prctl` calls propagate them — a shell script calling a capable binary
  doesn't itself gain the capability, only the binary it directly execs does.
- Containers intersect with this: a capability set on a binary inside an image
  only works if the container runtime's own capability set includes it; check
  your runtime's documentation.

## Verify
- [ ] `getcap <binary>` shows exactly the capabilities intended — no `CAP_SYS_ADMIN`/`CAP_DAC_OVERRIDE` granted "just in case."
- [ ] The granting process is documented in deployment automation (setcap re-applied post-deploy, or `AmbientCapabilities=` in the unit file) — not a one-off manual `setcap` that a redeploy silently loses.
- [ ] The process actually runs as a non-root UID alongside the capability — capabilities add nothing if the process is root anyway.
- [ ] A capability-dropped test (run the binary as a totally different non-root user with no capability set) fails exactly where expected, confirming the capability is load-bearing and not redundant with some other permission already granted.

## Checked

Checked 2026-10-27 against Linux man-pages (capabilities(7), signal(7), proc(5), kill(2), xattr(7); mkerrisk/man-pages master), systemd systemd.kill, systemd.service and systemd.exec man pages, 2026-10-27. Confirmed: ambient capabilities since Linux 4.3, CAP_NET_BIND_SERVICE for ports below 1024, CAP_SYS_ADMIN overloaded note, file capabilities stored in the security.capability xattr, AmbientCapabilities= and CapabilityBoundingSet= directives. Removed or softened: the ~40 count, getcap -v flag, the cp and CI-pipeline specifics, the Docker defaults paragraph.

Method: documentation only; no commands were run.
