---
id: computing-software.systems-network-administration.patch-management.patch-supersedence-and-finding-deduplication
name: patch-supersedence-and-finding-deduplication
category: computing-software
field: systems-network-administration
product: patch-management
tags: [patch-supersedence, finding-deduplication, prioritisation, vulnerability-scanner, cumulative-update, remediation]
level: practitioner
status: draft
description: "Turn thousands of scanner findings into a short list of actual patches: map CVEs to fixing updates, collapse by supersedence (latest cumulative), and group by remediation action."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Supersedence and finding deduplication

A scan report with 40,000 findings is usually 200 remediation actions. Work in actions.

## 1. Normalise findings
Key each finding by `(asset, product, fixing-update or fixed-version)` rather than by CVE.
Most scanners expose a "solution" or "patch" field (Tenable plugin "Solution", Qualys
"Patchable" + KB, Defender TVM "Security recommendation").

## 2. Collapse by supersedence
- **Windows**: monthly cumulative updates (LCU) supersede all previous ones. Twenty "missing
  KB" findings on one server = one action: install the latest LCU (plus SSU if separate,
  .NET CU, and any non-cumulative component). The Microsoft Update Catalog and WSUS show
  "superseded by".
- **Linux**: one package upgrade to the latest version fixes every older CVE in that
  package: action = `dnf upgrade openssl` / `apt install --only-upgrade openssl`.
- **Applications**: latest version of Chrome/Java/Office channel fixes all older CVEs.
- **Firmware**: latest vendor bundle.

## 3. Group by remediation owner and window
| Action | Assets | Max severity | KEV? | Owner | Window |
|---|---|---|---|---|---|
| Install 2026-10 LCU | 412 servers | Critical | yes | Wintel | ring schedule |
| Upgrade OpenSSL on RHEL 9 | 85 | High | no | Linux | weekly |
| Remove Java 8u202 | 37 desktops | Critical | yes | EUC | emergency |
Priority of the action = highest priority among its findings (CVSS/EPSS/KEV/exposure).

## 4. Separate non-patch findings
Config findings (weak TLS, SMBv1 enabled, default creds) aren't fixed by patches: route to
the baseline/hardening backlog.

## Gotchas
- Superseded-but-required: some updates are prerequisites (SSU before LCU on older
  Windows, kernel + kernel-modules matching). Supersedence ≠ always skip.
- Scanner "fixed" detection may lag after patching until rescan or reboot (Windows pending
  reboot keeps old file versions).
- Don't close findings by CVE count; close by verifying the action on each asset.

## Verify
Action list size and coverage: sum of findings mapped to actions ≥ 95% of the report;
after executing actions and rescanning, residual findings are mostly config or exceptions.
