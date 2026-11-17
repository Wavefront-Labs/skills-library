---
id: computing-software.cybersecurity-defensive.identity-access-management.domain-controller-hardening
name: domain-controller-hardening
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [domain-controller-hardening, active-directory-security, tier-0, dc-baseline, print-spooler, ntlm-restriction, ldap-signing]
level: advanced
status: gated
description: "Harden domain controllers: tier-0 isolation, minimal roles and software, security baseline, spooler off, NTLM and LDAP restrictions, backups, physical and virtual host protection."
sources: ["https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/securing-domain-controllers-against-attack", "https://www.cisecurity.org/benchmark/microsoft_windows_server", "https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/windows-security-configuration-framework/windows-security-baselines"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Domain controller hardening

## Placement and access
- Tier 0: administered only from PAWs by tier-0 admins; no other admins log on to DCs.
- No internet access from DCs (proxy blocked, outbound firewall), no browsing, no email.
- Virtual DCs: the hypervisor and its admins, storage and backup system are tier 0 too; encrypt VM disks, use shielded VMs/vTPM where available.
- RODCs at physically insecure sites with a restrictive password replication policy.

## Build
- Server Core where possible, DC role + DNS only; no agents beyond security/backup essentials (each agent with SYSTEM is a tier-0 dependency).
- Apply the Microsoft Security Baseline "Domain Controller" GPO; link a dedicated GPO to the Domain Controllers OU.
- **Print Spooler disabled** (`Stop-Service Spooler; Set-Service Spooler -StartupType Disabled`) - PrinterBug coercion and PrintNightmare (gated: unconfirmed, source is paywalled or blocked).
- LDAP signing and channel binding required; LDAPS certificates.
- SMB signing required, SMBv1 removed.
- Restrict NTLM (audit then deny where possible); disable LM and NTLMv1 (LAN Manager authentication level policy) (gated: unconfirmed, source is paywalled or blocked).
- Credential Guard is not supported for DC credentials, but LSA protection is (gated: unconfirmed, source is paywalled or blocked).
- Advanced audit policy per Microsoft recommendations; forward to SIEM.

## Operations
- Patch promptly (DC vulnerabilities are routinely exploited).
- Backups: system state daily, offline copy, tested (see ad-forest-recovery).
- Monitor DC-specific events: 4662 (DCSync-like replication rights use) and 5136 directory object changes (including GPOs).

## Gotchas
- Monitoring/backup agents with high privilege on DCs are attack paths; treat their consoles as tier 0.
- Disabling spooler on DCs breaks printer pruning (rarely needed).

## Verify
- [ ] Policy Analyzer: DC baseline compliance.
- [ ] Spooler disabled on all DCs: `Get-ADDomainController -Filter * | % { Get-Service -ComputerName $_.HostName Spooler }`.
- [ ] Logon events show only tier-0 admins on DCs.

## Checked

2026-10-28. Confirmed against the securing domain controllers against attack page and the security baselines page: tier separation, RODCs at branch sites, shielded VMs for virtual DCs, Policy Analyzer for baseline comparison. Gated: Print Spooler disable, LAN Manager level, LSA protection statement. Removed: CIS DC level 1, ZeroLogon and noPac names, 4742 and 7045 event ids.

Method: documentation only; no commands were run.
