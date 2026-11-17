---
id: computing-software.digital-forensics-incident-response.incident-response-process.blocking-lateral-movement-during-containment
name: blocking-lateral-movement-during-containment
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [lateral-movement-blocking, containment, lateral-movement, group-policy, dfir]
level: advanced
status: draft
description: "Restrict SMB, RDP, WinRM, WMI and admin logons enterprise-wide during containment with GPO, host firewall and tiering, without breaking recovery."
sources: ["https://learn.microsoft.com/en-us/windows-server/identity/securing-privileged-access/securing-privileged-access-reference-material", "https://www.cisa.gov/stopransomware/ransomware-guide", "https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Blocking lateral movement during containment

**Goal:** stop an attacker (or ransomware operator) with valid credentials from spreading host to
host while the team scopes and eradicates.

## Quick wins (hours)
- **Host firewall via GPO:** on workstations, block inbound TCP 445, 135, 139, 3389, 5985/5986
  except from defined admin jump hosts / management subnets. Workstation-to-workstation SMB is
  rarely needed.
- **Deny logon rights:** GPO "Deny access to this computer from the network" and "Deny log on
  through Remote Desktop Services" for Domain Admins / Enterprise Admins on all non-DC tiers.
  Add `Local account and member of Administrators group` (S-1-5-114) to network deny to kill
  local-admin pass-the-hash.
- **Disable remote services on endpoints:** stop/disable WinRM, Remote Registry where unused.
- **EDR:** enable built-in "contain" policies on hosts seen in scope; block PsExec/Impacket
  patterns via attack-surface-reduction rules (`Block process creations originating from PSExec and WMI commands`).

## Network level
- ACLs between segments allowing only management protocols from jump hosts.
- Block SMB/RDP from VPN pools to servers except admin pools.

## Rollout
1. Pilot on an IT OU for 1 h; check helpdesk tools and backup agents still work.
2. Push to all workstations, then servers; force `gpupdate /force` via EDR or Velociraptor.
3. Monitor 4625/5157 events for blocked legitimate traffic and adjust.

## Verify
- From a workstation: `Test-NetConnection <other-ws> -Port 445` fails; from the jump host it succeeds.
- Domain Admin network logon to a workstation fails with 4625 logon type 3, status 0xC000015B.

## Gotchas
- Blocking SMB to DCs breaks Group Policy and logon scripts; never apply workstation rules to DCs.
- Backup, patching and EDR agents may use SMB/RPC; whitelist their servers.
- Attackers already on a jump host bypass this; contain jump hosts first.
