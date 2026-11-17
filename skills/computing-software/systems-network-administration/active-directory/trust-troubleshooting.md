---
id: computing-software.systems-network-administration.active-directory.trust-troubleshooting
name: trust-troubleshooting
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-trusts, netdom-trust, name-suffix-routing, nltest, trust-password-reset, trust-verify, kerberos-referral, upn-suffix, forest-trust, netdom-resetoneside]
level: practitioner
status: gated
description: "Diagnose broken trusts: verify and reset the trust secret, fix DNS and ports, name suffix routing for UPN suffixes, and nltest checks for secure channels."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netdom-trust
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/config-firewall-for-ad-domains-and-trusts
  - https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Troubleshoot AD trusts

## Quick checks in order
1. **DNS:** from a DC in each forest the other domain's DCs resolve (`Resolve-DnsName _ldap._tcp.dc._msdcs.<other-domain> -Type SRV`; `nltest /dsgetdc:<other-domain>` (gated: unconfirmed, source is paywalled or blocked)). Fix conditional forwarders first; most "trust broken" tickets are DNS.
2. **Ports:** `Test-NetConnection <otherDC> -Port 88`, 389, 445, 135; RPC dynamic range open (see the Microsoft firewall article for the full table).
3. **Trust secret:**
```cmd
netdom trust ad.example.com /domain:fabrikam.example /verify
nltest /sc_verify:fabrikam.example        (gated: unconfirmed, source is paywalled or blocked)
```
4. **Time:** both forests within the Kerberos clock tolerance (5 minutes by default).

## Reset the trust password
If verify reports a bad password (for example after restoring a DC from an old backup), reset the trust secret:
```cmd
netdom trust ad.example.com /domain:fabrikam.example /reset /userd:FABRIKAM\admin /passwordd:* /usero:AD\admin /passwordo:*
```
`/reset` resets the trust secret between trusted domains. Resetting a one-sided or realm trust password uses `/oneside` and `/passwordt`, which are documented for non-Windows realm trusts and for `/add` and `/remove` only.

## Name suffix routing
Forest trusts route authentication by **name suffixes**. List and toggle them with netdom (valid for forest trusts); the status of a name in conflict cannot be changed until the conflicting name in the other trust is disabled. Always run `/namesuffixes` immediately before `/togglesuffix`, because the entry numbers can change.
```cmd
netdom trust ad.example.com /namesuffixes:fabrikam.example
```

## Common errors
- "The trust relationship between this workstation and the primary domain failed": that is a
  computer secure channel, not a forest trust; see the computer-account skill.
- `KDC_ERR_S_PRINCIPAL_UNKNOWN` across forests: the SPN is not associated with any account; check SPNs and suffix routing.

## Verify
- [ ] `netdom trust ... /verify` succeeds from both sides.
- [ ] `klist` on a client after accessing a cross-forest resource shows a service ticket for the resource.

## Checked
Checked 2026-10-27 against Microsoft Learn (netdom trust reference; Configure a firewall for Active Directory domains and trusts; Test-NetConnection reference; Kerberos policy page; event 4768).
- Confirmed: netdom /verify, /reset, /namesuffixes and /togglesuffix semantics; Test-NetConnection -Port; 5-minute default clock tolerance; KDC_ERR_S_PRINCIPAL_UNKNOWN meaning.
- Wrong in the earlier text: `/resetOneSide` is not a netdom parameter (`/reset` is), and `/oneside` is documented only with `/add` and `/remove`; `/verify /twoway` was dropped because /verify is documented without it.
- Gated: nltest commands. Reason: no readable Microsoft page covers nltest.
- Removed: the 0xC000018B code, the GUI Validate and Name Suffix Routing steps, and the by-IP remark.

Method: documentation only; no commands were run.
