---
id: computing-software.systems-network-administration.samba.ad-dc-network-prereqs
name: ad-dc-network-prereqs
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, ad-dc-network-prereqs, hosts-file, resolv-conf, active-directory, dns]
level: intro
status: docs-checked
description: "Prepare a host for a Samba AD DC: static IP, hostname, /etc/hosts and /etc/resolv.conf entries, and removing tools that rewrite resolv.conf."
sources:
  - https://wiki.samba.org/index.php/Setting_up_Samba_as_an_Active_Directory_Domain_Controller
  - https://wiki.samba.org/index.php/Joining_a_Samba_DC_to_an_Existing_Active_Directory
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ad dc network prereqs
- Use a static IP (reserve it outside the DHCP pool) and a hostname under 15 characters.
- Disable tools such as `resolvconf` that rewrite `/etc/resolv.conf`.

`/etc/hosts` on the DC (example values from the wiki):
```
127.0.0.1     localhost
10.99.0.1     DC1.samdom.example.com     DC1
```
The hostname and FQDN must not resolve to 127.0.0.1 or any address other than the LAN IP.

`/etc/resolv.conf` on the first DC:
```
search samdom.example.com
nameserver 10.99.0.1
```
The DC should list only itself as nameserver.

For an additional DC: before the join, point the first nameserver at an existing DC (the join needs it to find a KDC); after the join succeeds, change it to the new DC's own IP, not 127.0.0.1.

Debian/Ubuntu gotcha: if `systemd-resolved` holds port 53, stop and disable it, replace `/etc/resolv.conf`, restart Samba, then confirm only Samba listens: `netstat -tupln | grep :53`.

Time must be synchronised too (see ad-dc-time-sync). Do not use `.local` as the TLD; Avahi uses it. Samba does not support renaming the AD DNS zone and Kerberos realm.

## Checked
2026-11-04: static IP, hostname length, resolvconf, hosts and resolv.conf contents, additional-DC nameserver order and the systemd-resolved steps compared with the AD DC and Joining a DC wiki pages. Nothing removed.
Method: documentation only; no commands were run.
