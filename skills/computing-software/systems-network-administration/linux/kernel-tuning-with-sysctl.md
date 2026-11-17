---
id: computing-software.systems-network-administration.linux.kernel-tuning-with-sysctl
name: kernel-tuning-with-sysctl
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kernel, sysctl, sysctl-d, proc-sys, kernel-parameters, tuning, vm-swappiness, vm-overcommit-memory, vm-max-map-count, vm-dirty-ratio, fs-file-max, nofile, ulimit, limitnofile, somaxconn, tcp-max-syn-backlog, ip-local-port-range, tcp-tw-reuse, rmem, wmem, bbr, ip-forward, rp-filter, conntrack, nf-conntrack-max, tuned, kernel-hardening, sysadmin, limits-conf]
level: practitioner
status: docs-checked
description: "Tune Linux kernel parameters with sysctl: persistent /etc/sysctl.d drop-ins, load order, memory/network/file-limit knobs with starting values, and when ulimits matter instead."
sources:
  - https://docs.kernel.org/admin-guide/sysctl/vm.html
  - https://docs.kernel.org/networking/ip-sysctl.html
  - https://docs.kernel.org/admin-guide/sysctl/kernel.html
  - https://docs.kernel.org/admin-guide/sysctl/fs.html
  - https://gitlab.com/procps-ng/procps/-/blob/master/man/sysctl.8
  - https://github.com/linux-pam/linux-pam/blob/master/modules/pam_limits/pam_limits.8.xml
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Kernel tuning with sysctl — change one knob, for a measured reason, persistently

**Goal:** change kernel runtime parameters in a way that survives reboots, wins the
load-order fight, and is justified by a symptom rather than a blog post.

## 1. Read, set, persist
```bash
sysctl net.core.somaxconn                  # read (same as cat /proc/sys/net/core/somaxconn)
sysctl -w net.core.somaxconn=4096          # runtime only — lost on reboot
echo 'net.core.somaxconn = 4096' > /etc/sysctl.d/90-app.conf
sysctl --system                            # reload ALL sysctl.d dirs in order, prints each file
```
- `sysctl --system` reads the sysctl configuration directories in order, sorts all files
  **by filename regardless of directory**, and reads `/etc/sysctl.conf` last; the last
  write of a key wins. Name your file `90-…` or `99-…` so it overrides vendor defaults.
- `sysctl -p` loads only the file given, or `/etc/sysctl.conf` if none — use `sysctl --system`
  to load the drop-in directories.
- Keys for modules (e.g. `net.netfilter.nf_conntrack_max`, `net.bridge.*`) do not exist
  until the module is loaded, so a setting applied before the module loads fails.

## 2. Knobs worth knowing (starting points, not commandments)
| Symptom | Key | Typical change |
|---|---|---|
| Application needs more memory map areas than the default (65530) | `vm.max_map_count` | raise to the value the application documents |
| DB server swapping while page cache is huge | `vm.swappiness` | lower it (range 0-200; at 0 the kernel does not start swapping until free plus file-backed pages fall below the high watermark) |
| Large allocations refused although memory is mostly unused | `vm.overcommit_memory` | `1` pretends there is always enough memory (default `0` rejects obvious overcommits; `2` never overcommits) |
| Long write stalls when dirty pages flush | `vm.dirty_background_bytes` / `vm.dirty_bytes` | set in bytes instead of ratios (only one of each bytes/ratio pair is active; the other reads 0) |
| SYN drops / `listen queue overflow` under bursts | `net.core.somaxconn`, `net.ipv4.tcp_max_syn_backlog` | `somaxconn` defaults to 4096 (was 128 before kernel 5.4) — **and** the app's `listen()` backlog must be raised too |
| Outbound proxy runs out of ephemeral ports | `net.ipv4.ip_local_port_range` | widen the range; `tcp_tw_reuse` defaults to `2` (loopback only) and the kernel docs say not to change it without expert advice |
| Connection tracking table full | `net.netfilter.nf_conntrack_max` | default equals `nf_conntrack_buckets`; each connection is added to the table twice |
| Router/VPN/k8s node | `net.ipv4.ip_forward` | `1` |
| High-BDP links (long, fat pipes) | `net.core.rmem_max`/`wmem_max`, `net.ipv4.tcp_rmem`/`tcp_wmem`, `net.ipv4.tcp_congestion_control = bbr` | measure first |

Do not set `net.ipv4.tcp_tw_recycle`: it is absent from the current kernel `ip-sysctl` documentation, although old tuning guides still list it.

## 3. File limits: sysctl vs ulimit
"Too many open files" is usually the **per-process** limit, not `fs.file-max`
(system-wide; the kernel logs `VFS: file-max limit <number> reached` when it is hit). Check the running process:
```bash
cat /proc/<PID>/limits | grep -i 'open files'
```
For systemd services set `LimitNOFILE=65536` in a drop-in; `/etc/security/limits.conf`
is applied by `pam_limits` in PAM user sessions, so it does not reach services started
directly by systemd; use `LimitNOFILE=`.

## 4. Security-relevant defaults to keep
`kernel.kptr_restrict=1`, `kernel.dmesg_restrict=1`, `net.ipv4.conf.all.rp_filter=1`
(or `2` loose for asymmetric routing), `net.ipv4.conf.all.accept_redirects=0`,
`fs.protected_symlinks=1`. Check what a key does in the kernel documentation before loosening it.

## 5. Discipline
- One drop-in per purpose, with a comment saying **why** and the symptom/ticket.
- Change one key at a time and measure before/after with a metric tied to the symptom.
- On RHEL-family hosts, `tuned` profiles (`tuned-adm active`) also set sysctls and can
  override yours; check `tuned-adm active` before blaming sysctl.d.

## Verify
- [ ] `sysctl --system` lists your file and no "cannot stat" errors for its keys.
- [ ] After reboot, `sysctl <key>` shows your value (not a vendor or tuned override).
- [ ] For nofile issues, `/proc/<PID>/limits` of the *running* service shows the new limit.
- [ ] The original symptom metric (drops, overflows, OOM, stalls) improved.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) and the procps `sysctl(8)` man page on 2026-10-26. Confirmed: `vm.swappiness` range and zero behaviour, `vm.max_map_count` default 65530, `vm.overcommit_memory` modes and default, `dirty_*bytes`/ratio pairing, `somaxconn` default 4096 (was 128 before 5.4), `tcp_tw_reuse` values and default 2, `nf_conntrack_max` default, `--system` ordering and `/etc/sysctl.conf` last, `kptr_restrict`/`dmesg_restrict`/`protected_symlinks` existence, `file-max` log message, `pam_limits` as a PAM module. Removed: distro-specific and application-specific values that no kernel document covers.

Method: documentation only; no commands were run.
