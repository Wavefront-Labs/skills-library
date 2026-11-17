---
id: computing-software.cybersecurity-defensive.system-hardening.ntlm-restriction
name: ntlm-restriction
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [windows-hardening, ntlm-restriction, ntlmv1, kerberos, ntlm-auditing, lan-manager-authentication, pass-the-hash]
level: advanced
status: docs-checked
description: "Reduce and restrict NTLM in Active Directory: audit NTLM usage, enforce NTLMv2 only, block NTLM per server with exceptions and move applications to Kerberos."
sources: ["https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/network-security-lan-manager-authentication-level", "https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/network-security-restrict-ntlm-ntlm-authentication-in-this-domain"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NTLM restriction

**Goal:** NTLMv1/LM are gone, NTLMv2 use is known and shrinking, and high-value servers refuse NTLM.

## Step 1: LM/NTLMv1 off
GPO Security Options: "Network security: LAN Manager authentication level" = **Send NTLMv2 response only. Refuse LM & NTLM**. Audit for NTLMv1 and LM use before enforcing.

## Step 2: audit NTLM
- "Network security: Restrict NTLM: Audit NTLM authentication in this domain" = Enable all (on DCs).
- Review the NTLM Operational log to see which authentication attempts reach member servers, and aggregate in SIEM by source host, target and account.

## Step 3: fix callers
- Applications using IP addresses instead of names (Kerberos needs an SPN), missing SPNs, cross-forest without trust, local accounts, non-domain devices.
- Configure apps for Negotiate/Kerberos.

## Step 4: block
- Add the member servers that still need NTLM to the server exception list ("Add server exceptions") before denying.
- Domain-wide: "Restrict NTLM: NTLM authentication in this domain" = Deny for domain accounts to domain servers (after audit is clean).

## Verify
- [ ] No NTLMv1 events in DC logs.
- [ ] NTLM audit volume trending down; exceptions list documented.
- [ ] Tier 0 servers deny incoming NTLM.

## Checked
2026-10-28. Confirmed against official pages: LAN Manager authentication level option name, the Restrict NTLM audit-then-exception-list-then-deny sequence and the Deny for domain accounts to domain servers option (Microsoft Learn security policy pages).
Removed or rewritten: the numeric level, the LM hash setting, event IDs (4624, 4776, 8001-8004), Audit Incoming NTLM Traffic, Incoming NTLM traffic, setspn, Protected Users and relay-protection notes (not in the fetched pages).
Method: documentation only; no commands were run.
