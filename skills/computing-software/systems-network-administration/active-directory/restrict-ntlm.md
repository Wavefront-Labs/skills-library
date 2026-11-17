---
id: computing-software.systems-network-administration.active-directory.restrict-ntlm
name: restrict-ntlm
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, authentication-policies, restrict-ntlm, ntlm-auditing, ntlmv1]
level: advanced
status: docs-checked
description: "Audit then restrict NTLM: audit policies and the NTLM operational log, find NTLMv1 in 4624 events, add exceptions, then deny NTLM in stages."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/network-security-restrict-ntlm-ntlm-authentication-in-this-domain
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/network-security-restrict-ntlm-audit-ntlm-authentication-in-this-domain
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/windows-security/audit-domain-controller-ntlmv1
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-ntlm-blocking
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Restricting NTLM

NTLM is a legacy protocol that Microsoft is moving away from (NTLMv1 was deprecated in June 2024). Removing it is a
project: audit, exceptions, enforce in stages.

## 1. Audit (no impact)
Group Policy Security Options:
- **Network security: Restrict NTLM: Audit NTLM authentication in this domain** (set on DCs): Enable for domain
  accounts to domain servers, Enable for domain accounts, Enable for domain servers, or **Enable all**. It logs only
  traffic to that DC.
- **Network security: Restrict NTLM: Audit Incoming NTLM Traffic** (set on servers): Enable auditing for domain accounts,
  or **Enable auditing for all accounts**. It logs only traffic to the server where it applies.
- **Network security: Restrict NTLM: Outgoing NTLM traffic to remote servers**: Allow all, **Audit all**, Deny all.

Events are recorded in Applications and Services Logs > Microsoft > Windows > NTLM > Operational. Watch the size of that
log, restrict access to it (it reveals which devices use NTLM), and collect it with an event-collection system.

## 2. Find and remove NTLMv1 first
`Network security: LAN Manager authentication level` options run from "Send LM & NTLM responses" up to **Send NTLMv2
response only. Refuse LM & NTLM**. To find NTLMv1 users, enable Logon success auditing on the DC and review event 4624:
`Package Name (NTLM only): NTLM V1`. Ignore that value for **ANONYMOUS LOGON**, because the audit logic reports NTLMv1
whenever it finds no NTLMv2 key material, including anonymous sessions.

## 3. Fix sources
- Replace NTLM calls with Negotiate, which tries Kerberos and falls back to NTLM only when necessary.
- Use the audit log to find each application or client that still calls NTLM and fix it at the source before denying.

## 4. Enforce progressively
- First audit with the domain-level policy, then add the servers that still need NTLM to
  **Network security: Restrict NTLM: Add server exceptions in this domain**.
- **Network security: Restrict NTLM: NTLM authentication in this domain** options: Disable, Deny for domain accounts
  to domain servers, Deny for domain accounts, Deny for domain servers, **Deny all**. It does not affect interactive
  logon to the DC.
- Windows Server 2025 and Windows 11 24H2 and later let the SMB client block NTLM for outbound connections
  (`Set-SmbClientConfiguration -BlockNTLM $true`, or Group Policy) with an exception list.

## Verify
- [ ] Operational-log volume trending to zero outside listed exceptions.
- [ ] Deny mode on DCs with an exception list that has owners and end dates.

## Checked

Date: 2026-10-27. Documentation: the four "Network security: Restrict NTLM" and "LAN Manager authentication level"
policy pages (Windows 10 archive pages), Microsoft Support "Audit use of NTLMv1 on a domain controller" (2026), Block
NTLM connections on SMB in Windows Server 2025.
Confirmed: policy names and their option lists, scope of each audit policy, the NTLM operational log path, 4624
`Package Name (NTLM only)` field and the anonymous caveat, NTLMv1 deprecation date, SMB client NTLM blocking and its
versions.
Removed unconfirmed claims: the meaning assigned to events 8001-8004, WEF grouping advice, the IAKerb/local KDC remark,
and the SPN/alias and local-account remarks.

Method: documentation only; no commands were run.
