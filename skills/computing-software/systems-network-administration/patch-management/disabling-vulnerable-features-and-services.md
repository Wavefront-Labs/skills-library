---
id: computing-software.systems-network-administration.patch-management.disabling-vulnerable-features-and-services
name: disabling-vulnerable-features-and-services
category: computing-software
field: systems-network-administration
product: patch-management
tags: [disable-vulnerable-feature, mitigation, attack-surface-reduction, patch-risk-responses, workaround, patch-management]
level: practitioner
status: draft
description: "Mitigate unpatched flaws by disabling the vulnerable feature: SMBv1, Print Spooler, MSDT, legacy protocols and modules, deployed by GPO/Ansible with impact checks and rollback."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3
  - https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-34527
  - https://httpd.apache.org/docs/2.4/mod/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Disabling vulnerable features and services

When a fix is late, broken or the feature is unused, turning it off removes the attack path. Vendor advisories usually list the exact workaround.

## Common examples
| Feature | Disable | Impact to check |
|---|---|---|
| SMBv1 | `Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart` | Old NAS, copiers, XP-era devices |
| Print Spooler (PrintNightmare) | `Stop-Service Spooler; Set-Service Spooler -StartupType Disabled` on DCs/servers that do not print | Print servers obviously; some apps that render PDFs |
| MSDT URL protocol (Follina) | `reg delete HKCR\ms-msdt /f` (export first) | Troubleshooter links |
| WebDAV client | `Set-Service WebClient -StartupType Disabled` | SharePoint "open in Explorer" |
| Apache module | `a2dismod status` / comment `LoadModule` | Monitoring that scrapes it |
| OpenSSH agent forwarding / old ciphers | `sshd_config` `AllowAgentForwarding no`, `Ciphers` list | Old clients |
| Log4j JNDI lookups (pre-fix) | remove `JndiLookup.class` from the jar | None normally |

## Deploy
- Windows: GPO (services, registry preferences) or Intune settings catalog; Linux: Ansible task with `notify` restart handler.
- Always capture prior state (export registry key, `systemctl is-enabled`) for rollback.
- Pilot group, then broad, same as a patch.

## Detect usage first
- SMBv1: `Set-SmbServerConfiguration -AuditSmb1Access $true`, then event 3000 in `Microsoft-Windows-SMBServer/Audit`.
- Spooler: Print Service operational log; who printed in 30 days.

## Gotchas
- Some mitigations are reverted by the next update or app repair (registry ACL resets, jar rebuilt by redeploy).
- Scanners may still flag the CVE by version; record a mitigation deviation with evidence.
- Disabling is a mitigation, not remediation; keep the patch ticket open with a due date.

## Verify
Feature confirmed off on all targets (`Get-WindowsOptionalFeature`, `systemctl is-active`, config grep), vendor test for the vuln negative, no break tickets after a week.
