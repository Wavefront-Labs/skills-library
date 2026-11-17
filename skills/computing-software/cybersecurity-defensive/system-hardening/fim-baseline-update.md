---
id: computing-software.cybersecurity-defensive.system-hardening.fim-baseline-update
name: fim-baseline-update
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [fim-baseline-update, file-integrity-monitoring, patching, change-management, aide, wazuh]
level: practitioner
status: draft
description: "Update FIM baselines after patching without blessing tampering: verify changes against package databases and change tickets, then re-baseline AIDE, Tripwire or Wazuh."
sources: ["https://aide.github.io/", "https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/index.html", "https://www.pcisecuritystandards.org/document_library/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FIM baseline updates after patching

Patch night changes hundreds of binaries. If you just re-initialise the FIM database afterwards, you also bless
any malicious change made before or during the window. The goal: accept only changes explained by the approved
change.

## Procedure
1. **Pre-patch check**: run a FIM check immediately before the window. It must be clean (or all differences
   explained); otherwise investigate first.
2. **Patch** under a change ticket listing packages/KBs.
3. **Post-patch check**: run FIM and collect the report.
4. **Verify the differences** are explained:
   - Linux: verify changed files against the package manager's signed metadata:
     `rpm -Va` (lines with `5` = digest changed; on patched hosts, files of updated packages should verify
     clean against the new package), `dpkg --verify` or `debsums -c`. Every changed binary should belong to a
     package updated in this change (`rpm -qf <file>`, `dpkg -S <file>`, compare with `dnf history info last`
     or `/var/log/apt/history.log`).
   - Windows: changed system files should be signed by Microsoft (`Get-AuthenticodeSignature`), match the
     installed KB list (`Get-HotFix`), and be listed in the KB file manifest when needed.
   - Anything not owned by an updated package, unsigned, or outside the change scope is an incident lead.
5. **Accept into baseline**:
   - AIDE: `aide --update` writes `aide.db.new.gz`; review output, then move it to `aide.db.gz`; copy the new
     DB off-host.
   - Tripwire: `tripwire --update --twrfile <report>` and accept only verified entries.
   - Wazuh syscheck: no manual baseline; changes alert as they happen. Tag/suppress via change window
     correlation rules (e.g. a CDB list of hosts in maintenance) and attach the ticket to the alerts.
6. **Record**: ticket links to the FIM report and the verification evidence.

## Automate
- Hook re-baseline into the patch pipeline (Ansible play: pre-check, patch, `rpm -Va` filter, aide update)
  that stops and pages if unexplained changes exist.
- Prefer immutable infrastructure where possible: rebuild from a new golden image instead of patching in place,
  and FIM compares to the image manifest.

## Gotchas
- Config files changed by package scripts (`.rpmnew`, `.dpkg-dist`) need human review.
- Keeping the FIM database only on the host lets an attacker update it; store signed or off-host copies.
- PCI DSS 11.5.2 expects critical file comparisons at least weekly and alerting; document how patch changes are
  handled.

## Verify
Last patch ticket includes pre and post FIM reports and the package verification output, and the post-update
FIM check is clean.
