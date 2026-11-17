---
id: computing-software.systems-network-administration.samba.member-dns-kerberos
name: member-dns-kerberos
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, member-dns-kerberos, krb5-conf, member-preparation, dns, kerberos, domain-member]
level: practitioner
status: docs-checked
description: "Prepare a Unix host to be a Samba domain member: check processes, DNS resolution tests, minimal krb5.conf, hostname resolution, and crypto policy note."
sources:
  - https://wiki.samba.org/index.php/Setting_up_Samba_as_a_Domain_Member
  - https://wiki.samba.org/index.php/Troubleshooting_Samba_Domain_Members
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# member dns kerberos
Check nothing is running and find the config: `ps ax | egrep "samba|smbd|nmbd|winbindd"`, `smbd -b | grep CONFIGFILE`.

DNS (`/etc/resolv.conf`):
```
nameserver 10.99.0.1
search samdom.example.com
```
Test: `nslookup DC1.samdom.example.com`, `host DC1.samdom.example.com`, `host 10.99.0.1`, `host -t SRV _ldap._tcp.samdom.example.com`.

Hostname: `getent hosts M1` should return the LAN IP via `/etc/hosts`:
`10.99.0.5      M1.samdom.example.com    M1`

`/etc/krb5.conf` (set nothing more; remove any `include` line):
```
[libdefaults]
	default_realm = SAMDOM.EXAMPLE.COM
	dns_lookup_realm = false
	dns_lookup_kdc = true
```
Some MIT Kerberos systems need a `[plugins]` localauth section for winbind, and `krb5_auth = yes` plus `krb5_ccache_type = FILE` in `/etc/security/pam_winbind.conf`. On crypto-policy distributions run `update-crypto-policies --set DEFAULT:AD-SUPPORT`.

Gotcha: an `includedir` in krb5.conf can break Samba (`NT_STATUS_CONNECTION_RESET` at log level 3+); remove it.

## Checked

2026-11-04. Confirmed against the Samba wiki Setting up Samba as a Domain Member page: the ps and smbd -b checks, nslookup and host tests including the SRV query, getent hosts, the krb5.conf libdefaults, the advice to set nothing more and remove any include line, the MIT localauth plugins and pam_winbind.conf lines, and the update-crypto-policies command. The includedir gotcha is on the Troubleshooting Samba Domain Members page (added as a source).
Method: documentation only; no commands were run.
