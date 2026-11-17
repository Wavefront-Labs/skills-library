---
id: computing-software.cybersecurity-defensive.system-hardening.kernel-sysctl-hardening
name: kernel-sysctl-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [linux-hardening, sysctl-hardening, kernel-hardening, kptr-restrict, ptrace-scope, network-sysctl, kspp]
level: practitioner
status: docs-checked
description: "Harden Linux kernel parameters with sysctl: network spoofing and redirect protections, kernel pointer and dmesg restrictions, ptrace scope, BPF and core dump controls."
sources: ["https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/sysctl/kernel.rst", "https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/sysctl/fs.rst", "https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/sysctl/net.rst", "https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/LSM/Yama.rst", "https://github.com/torvalds/linux/blob/master/Documentation/networking/ip-sysctl.rst", "https://github.com/systemd/systemd/blob/main/man/sysctl.d.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kernel sysctl hardening

**Goal:** a reviewed sysctl baseline in `/etc/sysctl.d/` that removes easy kernel info leaks and network abuse paths.

## Baseline (`/etc/sysctl.d/60-hardening.conf`)
```
# network (hosts that are not routers)
net.ipv4.ip_forward = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv4.conf.all.secure_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.all.log_martians = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.tcp_syncookies = 1
net.ipv6.conf.all.accept_ra = 0
# kernel
kernel.kptr_restrict = 2
kernel.dmesg_restrict = 1
kernel.yama.ptrace_scope = 1
kernel.unprivileged_bpf_disabled = 1
net.core.bpf_jit_harden = 2
kernel.kexec_load_disabled = 1
kernel.randomize_va_space = 2
fs.protected_hardlinks = 1
fs.protected_symlinks = 1
fs.protected_fifos = 2
fs.protected_regular = 2
fs.suid_dumpable = 0
```
Apply: `sysctl --system`; check: `sysctl kernel.kptr_restrict`.

## Know the trade-offs
- `ip_forward=0` is wrong for routers, gateways and any node that must forward packets.
- `rp_filter=1` is strict mode (RFC 3704); the kernel documentation recommends loose mode (`2`) for asymmetric or complicated routing.
- `kernel.yama.ptrace_scope`: `1` restricts attach to descendants (plus declared debuggers), `2` allows only processes with `CAP_SYS_PTRACE`, `3` allows no attach at all and cannot be changed until reboot.
- `kexec_load_disabled=1` disables `kexec_load` and `kexec_file_load` and cannot be set back to 0 until reboot; a kexec image can still be loaded before the toggle is set.
- `accept_ra=0` on hosts that rely on router advertisements (SLAAC) loses autoconfiguration.
- `unprivileged_bpf_disabled=1` cannot be cleared until reboot; `2` also disables unprivileged `bpf()` but an admin can change it later.
- `user.max_user_namespaces=0` removes user namespaces, which anything relying on them (for example rootless containers) needs.

## Persistence gotchas
- Files must end in `.conf` and are sorted by file name across all sysctl.d directories; if several files set the same key, the lexicographically latest name wins (sysctl.d(5)), so a package `99-*.conf` can override yours.
- `conf/default/*` supplies the settings for interfaces created later and `conf/all/*` changes the settings of all interfaces, so set both; for `rp_filter` the larger of the `all` and per-interface values is used (ip-sysctl documentation).

## Verify
- [ ] `sysctl -a 2>/dev/null | grep -E 'kptr_restrict|dmesg_restrict|rp_filter'` matches baseline after reboot.
- [ ] `sysctl --system` reports no errors for any baseline key.

## Checked
Checked 2026-10-25 against the Linux kernel documentation (torvalds/linux, tree at 2026-10-25): sysctl/kernel.rst (kptr_restrict, dmesg_restrict, unprivileged_bpf_disabled, kexec_load_disabled, randomize_va_space), sysctl/fs.rst (protected_hardlinks, protected_symlinks, protected_fifos, protected_regular, suid_dumpable), sysctl/net.rst (bpf_jit_harden), sysctl/user.rst, LSM/Yama.rst (ptrace_scope 0-3) sysctl.d(5) precedence rules (systemd/systemd), and networking/ip-sysctl.rst (rp_filter, accept_redirects, secure_redirects, send_redirects, accept_source_route, log_martians, icmp_echo_ignore_broadcasts, tcp_syncookies, accept_ra, ip_forward). All keys in the baseline exist with the documented values. Corrected the ptrace_scope trade-off (only `3` also blocks administrators) and removed `unprivileged_userns_clone` (a distribution-specific knob not in the mainline documentation), the Docker/Kubernetes forwarding claim, the kdump claim and the CIS/OpenSCAP check lines.

Method: documentation only; no commands were run.
