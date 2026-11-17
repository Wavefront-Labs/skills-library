---
id: computing-software.it-support-helpdesk.intune-mdm.windows-firewall-policy-from-intune
name: windows-firewall-policy-from-intune
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, firewall-policy, windows-firewall, firewall-rules, endpoint-security, network-profiles, local-rule-merge, intune, windows-defender-firewall]
level: practitioner
status: docs-checked
description: "Configure Windows Firewall with Intune endpoint security: profile settings, rules profiles, local rule merge, policy conflicts, reports, and port and protocol rule errors."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/protect/endpoint-security-firewall-policy"
  - "https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/configure"
  - "https://learn.microsoft.com/en-us/windows/client-management/mdm/firewall-csp"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# windows-firewall-policy-from-intune

Two profile types under Endpoint security > Firewall:
- **Windows Firewall**: settings per network profile (Domain, Private, Public).
- **Windows Firewall rules**: individual rules, up to 150 rules per profile.

## Windows Firewall CSP defaults (per profile)
These are the CSP defaults when nothing is configured, not recommended values:
| Setting | CSP default |
|---|---|
| DefaultInboundAction | 1 (Block) |
| DefaultOutboundAction | 0 (Allow) |
| AllowLocalPolicyMerge | true |
| EnableLogDroppedPackets | false |
| LogMaxFileSize | 1024 (kilobytes) |
| LogFilePath | `%systemroot%\system32\LogFiles\Firewall\pfirewall.log` |
| Shielded | false |

- AllowLocalPolicyMerge false: firewall rules from the local store are ignored and not enforced. This is why rules an app
  creates at install stop applying; deliver the rule from Intune instead.
- Shielded true (with EnableFirewall on): blocks all incoming traffic regardless of other policy settings.
- Log settings depend on EnableFirewall being true. The log records dropped packets and successful connections.
- Merge law for most settings: a Group Policy value wins if configured, then the MDM store, then the local store.

## Conflicts and merging (Intune page)
- Firewall settings profiles: if two policies set the same setting differently, the conflicting setting is not sent to the device.
- Firewall rules profiles: rules merge across profiles. Conflicting rules are both delivered, so check what the device ends up with.
- Where both Group Policy and Intune manage the firewall, see profile-conflicts-and-gpo-vs-mdm-precedence.

## Writing a rule
Rule creation steps in the Windows Firewall console (the configure page) mirror the Intune rule fields:
- Choose direction, action (allow or block), program path or service, protocol, ports, scope and the profiles it applies to.
- To restrict a rule to a port you must pick TCP or UDP.
- For a program path, use environment variables so installs in different locations work.
- Service rules need the service to have a SID type of RESTRICTED or UNRESTRICTED (`sc qsidtype <ServiceName>`); NONE cannot be used in a firewall rule.
- By default outbound traffic is allowed unless a rule blocks it.

## Rule errors and troubleshooting (Intune page)
- Port ranges: ascending, within 0-65535.
- Ports set on a rule require protocol 6 (TCP) or 17 (UDP).
- Edge traversal needs the inbound direction.
- The "All" interface type excludes the other interface types, so do not combine it with them.
- On Windows 11 21H2 and 22H2 and Windows 10 21H2 the CSP applies a rules block atomically: one bad rule can fail the whole block.

## Reporting
- Endpoint security > Firewall > Summary.
- MDM Firewall status for Windows report: Enabled, Disabled, Limited, Temporarily Disabled, Not applicable.

## Verify
The profile shows Succeeded for the device, the firewall status report shows Enabled, and the app's traffic works with the rule present.

## Checked
Date: 2026-11-08. Read in full: "Firewall policy for endpoint security in Intune", "Configure rules with group policy" and the
Firewall CSP page (settings sections for Private and Public profiles). Removed as unconfirmed: the recommended defaults
table, 16 MB log size (CSP default is 1024 KB), the Teams port example, Get-NetFirewallProfile and ActiveStore steps,
auditpol and event 5152/5157 steps, Get-NetConnectionProfile advice, and the MpsSvc comment.
Method: documentation only; no commands were run.
