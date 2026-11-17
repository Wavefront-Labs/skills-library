---
id: computing-software.digital-forensics-incident-response.volatility.linux-memory-forensics-with-volatility3
name: linux-memory-forensics-with-volatility3
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [linux-memory-forensics, volatility3, isf, dwarf2json, linux-pslist, linux-bash, linux-psaux, kernel-symbol-table, lime, avml, ebpf-rootkit, container-forensics, linux-kernel-module, dfir]
level: advanced
status: draft
description: "Triage a Linux RAM image with Volatility 3: build an exact-kernel ISF symbol table with dwarf2json, run the linux.* plugins, and know where Linux memory forensics falls short."
sources: ["https://volatility3.readthedocs.io/", "https://github.com/volatilityfoundation/dwarf2json"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Linux memory forensics with Volatility 3

**Goal:** apply the same triage discipline as
computing-software.digital-forensics-incident-response.volatility.memory-image-triage-with-volatility3
to Linux hosts — a materially harder starting point, because Linux has no stable,
versioned public symbol-table ecosystem like Windows' PDB-based ISF generation; every
kernel build effectively needs its own symbol table built by hand.

## 1. Acquisition first
`LiME` (Linux Memory Extractor, a loadable kernel module) is the standard live
acquisition tool; `AVML` (Microsoft's Azure VM memory loader, works without kernel
module compilation) is the alternative when building LiME against the exact running
kernel isn't practical. **Acquire before anything else disturbs memory** — same
order-of-volatility logic as
computing-software.digital-forensics-incident-response.evidence-handling.forensic-acquisition-and-chain-of-custody.

## 2. Symbol tables are the real obstacle
Volatility 3 needs an **ISF (Intermediate Symbol File)** matching the *exact* kernel
version, build, and often the exact distro package (kernel structures and offsets
vary not just by version number but by distro-specific compile config). There is no
single downloadable symbol set covering every Linux kernel the way Windows PDB
symbols are centrally available:
```
dwarf2json linux --elf /path/to/vmlinux --system-map /boot/System.map-$(uname -r) > linux_kernel.json
```
This requires a `vmlinux` file with debug symbols for the **exact running kernel** —
often not present by default on a production system (debug symbol packages are
frequently not installed) and sometimes needing to be built or pulled from a
distro's debug-symbol repository matching the exact kernel package version. **This
step, done wrong or skipped, is the most common reason Linux memory analysis fails
outright** rather than producing subtly wrong output — Volatility will often simply
error or return empty results without a correctly matched ISF, which is at least a
loud failure rather than the silent-wrong-answer risk Windows symbol mismatches pose.
Capture the exact kernel version (`uname -a`) and ideally a debug-symbol-capable
`vmlinux` *before* an incident, as part of a response-readiness baseline, since
obtaining it after the fact (especially from a now-compromised or rebuilt host) can
be impossible.

## 3. Core plugins
```
vol -f mem.lime linux.pslist          # process list; also linux.psaux for arg/cmdline detail
vol -f mem.lime linux.bash            # recovers bash history from a process's memory directly
vol -f mem.lime linux.sockstat        # socket/connection state (there is no linux.netstat plugin)
vol -f mem.lime linux.lsmod           # loaded kernel modules
vol -f mem.lime linux.malware.malfind         # injected/anomalous executable memory regions
```
`linux.bash` is distinctive and valuable: it recovers command history **directly from
a running bash process's memory**, including commands not yet flushed to
`~/.bash_history` on disk — closing exactly the gap named in
computing-software.digital-forensics-incident-response.log-analysis.linux-syslog-auditd-and-ssh-log-forensics
where disk-based bash history can be incomplete or cleared. This only works for
processes still resident in memory at capture time, so timing of acquisition matters.

## 4. Kernel module and eBPF-based threats
`linux.lsmod` enumerates loaded kernel modules — an unexpected or unsigned module is
the Linux kernel-rootkit equivalent of the Windows driver-scan work in
computing-software.digital-forensics-incident-response.volatility.rootkit-and-kernel-memory-analysis.
A newer and less tooled threat class is **eBPF-based rootkits/implants** (abusing
legitimate eBPF hooks for process/file hiding or syscall interception) — Volatility 3
support for directly enumerating loaded eBPF programs from a memory image is limited
and evolving; where this matters, supplement memory analysis with live `bpftool
prog list` output captured as part of initial live response (see
computing-software.digital-forensics-incident-response.evidence-handling.live-response-and-kape-triage-collection's
collection-before-memory ordering) rather than relying on memory-image analysis alone
for this specific threat class.

## 5. Containers complicate everything
A memory image of the host captures container processes too, but container
namespacing means PID/network views inside a container don't match the host's own
view directly — correlate via cgroup/namespace identifiers in `linux.pslist` output,
and separately capture a container's own filesystem layer (overlay diff) if
container-specific persistence is suspected, since a memory snapshot alone doesn't
show which container a given process belonged to as cleanly as host-native tooling
would.

## Verify
- Confirm the ISF symbol table was built against the *exact* running kernel build
  (not just major version) before trusting any plugin output; empty/error output is
  more often a symbol mismatch than "nothing to find."
- Cross-check `linux.bash` recovered commands against disk-based `.bash_history` and
  auth.log timing for consistency.
- For eBPF-based threat hypotheses, supplement with live `bpftool`/`ebpf` enumeration
  captured during live response rather than relying solely on memory-image plugins.

Unconfirmed: Volatility 3's Linux plugin coverage and eBPF support are actively
developing — verify current plugin availability against the installed Volatility
version before assuming a capability exists.
