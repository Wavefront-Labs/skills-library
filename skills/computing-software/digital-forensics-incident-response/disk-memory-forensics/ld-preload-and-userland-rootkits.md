---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.ld-preload-and-userland-rootkits
name: ld-preload-and-userland-rootkits
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [ld-preload-rootkit, linux-forensics, linux-persistence, rootkit, dfir]
level: advanced
status: docs-checked
description: "Detect Linux userland rootkits that preload libraries via /etc/ld.so.preload and LD_PRELOAD: how the loader applies them, dead-box checks and live cross-views."
sources: ["https://man7.org/linux/man-pages/man8/ld.so.8.html", "https://attack.mitre.org/techniques/T1574/006/", "https://github.com/volatilityfoundation/volatility3"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LD_PRELOAD and userland rootkits

**Goal:** a shared library named in `/etc/ld.so.preload` (ATT&CK T1574.006, dynamic linker hijacking) is loaded before the
program's own libraries in every dynamically linked process, so it can override libc functions and hide files, processes and
connections from `ls`, `ps` and similar tools. Live triage on the host can therefore lie to you.

## How the loader applies preloads (ld.so(8))
- `LD_PRELOAD` is a list of additional ELF shared objects loaded before all others; separators are spaces or colons, with no
  escaping. Order of handling: the `LD_PRELOAD` variable, then the `--preload` option when invoking the loader directly, then
  `/etc/ld.so.preload`.
- `/etc/ld.so.preload` is a whitespace-separated list of shared objects with a system-wide effect.
- In secure-execution mode (for example set-user-ID programs) preload names containing slashes are ignored and libraries are
  preloaded only from standard directories and only if they have the set-user-ID bit, so env-var preloads do not act on such
  programs.
- Statically linked programs do not use the dynamic loader, so a static binary is not affected by a preload.
- ATT&CK examples: Rocke modified `/etc/ld.so.preload` to hook libc functions and hide its dropper and miner from process lists;
  Hildegard modified it to intercept library imports; Ebury uses `LD_PRELOAD` to inject into programs launched by SSH sessions.

## Dead-box checks (image or mounted disk, not affected by the rootkit)
- `/etc/ld.so.preload`: any entry is suspect until attributed to a known product or package; check where the listed object lives
  and when it was created.
- Look for `LD_PRELOAD` set in environment files, shell start-up files and service definitions.
- Review the library's imported and overridden functions (directory-reading and file-opening functions are typical targets).

## Live detection when the host is suspect
- Use statically linked tools (not subject to a preload) or read `/proc` directly, and compare the process count they see with
  what `ps` reports.
- The loader's `LD_DEBUG` variable with the `libs` category prints library search paths and can show what is loaded for a
  command; it is ignored in secure-execution mode, so run it on a non-privileged binary.
- Brute-force cross-view tools can compare `/proc` against other process listings.

## Memory
Volatility 3 (see its repository for the current Linux plugin list) can enumerate per-process memory mappings; a preload library
shows up as a mapping in every dynamically linked process.

## Remediation
Remove the entry from a trusted environment (rescue boot), because the live system may hide or hook the edit; rebuild is
preferred after a rootkit.

## Gotchas
- Some security and monitoring agents legitimately preload libraries: verify vendor and package.
- Statically linked binaries ignore preloads: useful for triage, and also usable by an attacker to avoid a hook.

## Verify
The review of `ld.so.preload` and loader environment is clean, or every preloaded library is attributed.

## Checked
Date: 2026-11-08.
Confirmed in ld.so(8): LD_PRELOAD semantics and separators, handling order, `/etc/ld.so.preload` description, secure-execution
rules, `LD_DEBUG` `libs` category and its secure-mode behaviour. Confirmed in T1574.006: Rocke, Hildegard and Ebury behaviour.
Removed because the cited pages do not state them: the specific commands (dpkg, rpm, debsums, unhide, awk pipelines), example
library paths and named rootkits, `/etc/profile.d` as a location, and the named Volatility plugins and the kernel-rootkit (DKOM)
comparison.
Method: docs-only read of cited pages, 2026-11-08
