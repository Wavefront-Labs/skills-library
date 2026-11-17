---
id: computing-software.digital-forensics-incident-response.volatility.memory-credential-and-registry-extraction
name: memory-credential-and-registry-extraction
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [volatility3, hashdump, cachedump, lsadump, hivelist, printkey, lsass, credential-theft, ntlm-hash, dcc2, mimikatz-artifacts, registry-in-memory, secrets-dump, windows-memory, dfir]
level: advanced
status: docs-checked
description: "Extract registry hives and credential material from a Windows RAM image with Volatility 3: hivelist/printkey for registry, hashdump/cachedump/lsadump for secrets, LSASS caveats."
sources: ["https://volatility3.readthedocs.io/", "https://github.com/volatilityfoundation/volatility3"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Memory credential and registry extraction

**Goal:** go past
computing-software.digital-forensics-incident-response.volatility.memory-image-triage-with-volatility3's
process/network triage into two specific, high-value memory-forensics tasks: reading
registry state as it existed at capture time (sometimes different from the on-disk
hive — see
computing-software.digital-forensics-incident-response.disk-memory-forensics.registry-hive-forensics-and-deleted-key-recovery
for the disk-side equivalent) and recovering credential material an attacker may also
have been after.

## 1. Registry from memory
```
vol -f mem.dmp windows.registry.hivelist
vol -f mem.dmp windows.registry.printkey --offset <hive_offset> --key "Microsoft\Windows\CurrentVersion\Run"
```
Registry hives are mapped into memory as the kernel accesses them — `hivelist` finds
every hive present in the image by walking the kernel's registry HiveList.
`printkey` walks a specific key from a given hive offset (`--offset`, `--key`, optional
`--recurse`). This captures **in-memory state**, which can differ from the on-disk hive
when changes had not yet been flushed — worth checking when the disk-side hive looks
stale or the host was imaged live.

## 2. Credential extraction plugins
```
vol -f mem.dmp windows.registry.hashdump          # local user hashes, decrypted from the SAM hive using the SYSTEM bootkey
vol -f mem.dmp windows.registry.cachedump         # cached domain credentials, read from the SECURITY hive "Cache" key
vol -f mem.dmp windows.registry.lsadump           # LSA secrets, read and decrypted from the SECURITY hive
```
These plugins parse the same registry/LSA structures an attacker's own credential-
dumping tooling targets — running them is how a defender confirms **what an attacker
could have obtained**, not a routine step on every case. Results are only as strong
as the plugin's symbol-table match for the exact Windows build (see the troubleshooting
notes in
computing-software.digital-forensics-incident-response.volatility.memory-image-triage-with-volatility3)
— a mismatched or incomplete symbol table can produce partial or silently wrong output
here more consequentially than in process listing, because a missing hash is easy to
mistake for "none existed."

## 3. LSASS secrets — the harder, more consequential case
NTLM/cached hashes above come from registry structures; **plaintext credentials and
Kerberos tickets in LSASS process memory** (what tools like Mimikatz target live) are
a separate, much harder recovery target from a memory image:
- The Volatility 3 plugin set has no LSASS credential-extraction plugin comparable to live
  Mimikatz (the only LSASS-related plugin in the tree is the skeleton-key check) — this generally means locating the LSASS process (`windows.pslist`),
  dumping its memory region (`windows.memmap --dump` or `windows.vadyarascan`
  targeting known credential-structure patterns), and searching the dump for
  structures Mimikatz itself knows how to parse (WDigest, Kerberos ticket caches,
  etc.) — a nontrivial, version-dependent undertaking, not a one-command plugin run.
  **Unconfirmed in detail: the exact current best-practice tool/plugin chain for
  offline LSASS secret extraction from a Volatility-captured image changes with
  Windows mitigations (Credential Guard, LSA protection) — verify against current
  tooling and whether the target host had Credential Guard/RunAsPPL enabled, which
  can make this impossible without a kernel-level live attack, not just an offline
  memory read.**
- The practical takeaway for most IR engagements: confirming **evidence that
  credential-dumping tooling ran** (process creation for `mimikatz.exe`/renamed
  variants, LSASS handle access patterns via `malfind`/handle enumeration, Sysmon
  Event ID 10 process-access events targeting `lsass.exe`) is usually more actionable
  and more reliably obtainable than performing the dump yourself from the image.

## Verify
- Confirm the Volatility symbol table matches the exact OS build before trusting
  hashdump/cachedump/lsadump output as complete — a partial match can silently drop
  entries rather than erroring.
- State explicitly whether Credential Guard/LSA protection (RunAsPPL) was active on
  the source host, since this changes what's actually recoverable and what
  conclusions "we found no credentials" supports.
- Cross-check any extracted hash/secret against independent evidence (an actual
  observed authentication using that credential in logs) before treating extraction
  alone as proof of compromise of that specific account.

## Checked

- Confirmed: plugin names and printkey --offset/--key/--recurse options; hashdump uses SAM and SYSTEM hives, cachedump and lsadump read the SECURITY hive.

Method: docs-checked 2026-11-09 against volatility3 develop source plugins/windows/registry/{hashdump,cachedump,lsadump,hivelist,printkey}.py and a search of the plugin tree for LSASS/WDigest plugins (the MITRE source was unreadable and was dropped). Removed unconfirmed hive-offset requirement, DCC2/DPAPI specifics and USB/logged-off-hive examples; the Credential Guard and Sysmon notes are practitioner guidance, not from the cited pages.
