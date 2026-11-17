---
id: computing-software.systems-network-administration.netbird.dns-troubleshooting
name: dns-troubleshooting
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, dns-troubleshooting, resolvectl, nrpt, flush-dns, isolation-test]
level: practitioner
status: docs-checked
description: "Troubleshoot NetBird DNS: confirm managed mode, quick checks, per-OS resolver tests and fixes for internal names, public domains, macOS NXDOMAIN and Windows NRPT."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/dns/troubleshooting.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
1. Is DNS managed? Check DNS > DNS Settings for the peer's groups; `netbird status -d` with an empty Nameservers section suggests unmanaged mode; clear a stale flag with `netbird down` then `netbird up --disable-dns=false`.
2. Quick checks: `netbird status -d`, `cat /etc/resolv.conf`, `dig @<ns-ip> <name>`. Test the system resolver with `resolvectl query <name>` (Linux), `dscacheutil -q host -a name <name>` (macOS), `Resolve-DnsName <name>` (Windows). On macOS and Windows dig/host/nslookup use a different path and can show NXDOMAIN while the system resolver works.
3. Fixes:
- Internal names fail: restart NetBird; Android set Private DNS to Off.
- Wrong nameserver: confirm the peer's group is assigned; use `company.internal`, not `*.company.internal`.
- Public domains fail: add a primary nameserver with empty match domains plus backups.
- Short names: enable search domains (match-domain groups only).
- macOS NXDOMAIN: add a primary group pointing at the same internal servers.
- Intermittent: flush caches (`sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder`; `ipconfig /flushdns`).
- Broken after `netbird down`: if `/etc/resolv.conf` still points to a `100.x.255.254` address, restore DNS manually.
- Windows NRPT ignored: `Get-DnsClientNrptPolicy -Effective`; a Group Policy container (`DnsPolicyConfig`) overrides NetBird's local rule. Clear the stale container, or reconnect the device to the company network and run `gpupdate /force`.
- AD login fails: domain resources resolve only A/AAAA, so add a nameserver for the AD domain pointing at a domain controller.
4. Isolation: `netbird down; netbird up --disable-dns`. If the problem vanishes, it is your NetBird DNS config. Undo with `netbird down; netbird up --disable-dns=false`.

## Checked

2026-11-04: read the DNS troubleshooting page in full. Confirmed the managed-mode check, quick checks, per-OS resolver tests, each fix listed, the isolation test and the NRPT and Group Policy explanation. Reworded the NRPT fix, which was too thin on the cause.

Method: documentation only; no commands were run.
