---
id: computing-software.cybersecurity-defensive.identity-access-management.ad-trusts
name: ad-trusts
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [ad-trusts, forest-trust, sid-filtering, selective-authentication, quarantine, trust-security, active-directory-security]
level: advanced
status: gated
description: "Secure AD domain and forest trusts: inventory, SID filtering/quarantine, selective authentication, removing stale trusts, TGT delegation across trusts and monitoring."
sources: ["https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-pac/55fc19f2-55ba-4251-8a6a-103dd7c66280", "https://learn.microsoft.com/en-us/entra/identity/domain-services/concepts-forest-trust", "https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/configure-selective-authentication"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Domain and forest trust security

## Facts that matter
- The **forest**, not the domain, is the security boundary. Any domain admin in a child domain can become enterprise admin of the forest (SID history injection of the Enterprise Admins SID in the forest - SID filtering does not apply within a forest).
- Across forest/external trusts, **SID filtering** (quarantine) strips foreign SIDs from other domains - keep it on.

## Inventory
```
Get-ADTrust -Filter * | Select Name, Direction, TrustType, ForestTransitive, SIDFilteringQuarantined, SelectiveAuthentication, TGTDelegation, Created
nltest /domain_trusts /all_trusts
```
Each trust: business owner, purpose, direction needed (often one-way is enough), review date.

## Harden
- Remove trusts no longer needed (M&A leftovers are common).
- One-way trust where only one side needs access.
- **Selective authentication** on forest/external trusts: users from the trusted forest can authenticate only to computers where they are granted "Allowed to Authenticate" (gated: unconfirmed, source is paywalled or blocked).
- SID filtering enabled on external trusts (`netdom trust <trusting> /domain:<trusted> /quarantine:yes`); for forest trusts avoid `/enablesidhistory:yes` unless migrating, and turn it off afterwards (gated: unconfirmed, source is paywalled or blocked).
- Disable TGT delegation across forest trusts (`netdom trust ... /EnableTGTDelegation:No`) (gated: unconfirmed, source is paywalled or blocked) - unconstrained delegation hosts in the trusting forest otherwise capture TGTs of the other forest.
- Restrict trusted-forest users from privileged groups.

## Monitor
- Audit events for trust creation, removal and modification; 4769 with cross-realm tickets from unusual accounts.

## Gotchas
- Extending a trust to a less-secure forest imports its risk; a compromised trusted forest can reach anything its users are granted.
- Entra Domain Services forest trusts: check the current concept page for supported trust directions (one-way incoming or outgoing, with two-way in preview when checked).

## Verify
- [ ] Trust inventory with owners; stale trusts removed.
- [ ] SID filtering and selective authentication confirmed with `Get-ADTrust` output.

## Checked

2026-10-28. Confirmed: SID filtering and trust boundary types in the MS-PAC specification page; Entra Domain Services forest trust concept page (one-way trusts, incoming or outgoing, with two-way in preview). The selective authentication troubleshoot page returned 404. Gated: selective authentication, netdom commands, TGT delegation switch. Removed: event ids 4706/4707/4716, 'default since 2019 updates' claim, and the incorrect 'one-way outbound only' claim for Entra Domain Services.

Method: documentation only; no commands were run.
