---
id: computing-software.systems-network-administration.samba.ad-dc-kerberos-and-verify
name: ad-dc-kerberos-and-verify
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, ad-dc-kerberos-and-verify, kinit, srv-records, krb5-conf, active-directory]
level: practitioner
status: docs-checked
description: "Install the generated krb5.conf on a Samba AD DC, start samba, and verify with smbclient, host SRV lookups, kinit and klist."
sources:
  - https://wiki.samba.org/index.php/Setting_up_Samba_as_an_Active_Directory_Domain_Controller
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ad dc kerberos and verify
Copy (do not symlink) the generated Kerberos config, using the path shown by provisioning:
`cp /usr/local/samba/private/krb5.conf /etc/krb5.conf`
Since Samba 4.7 the private directory is root-only, so a symlink breaks access for other users (for example BIND_DLZ dynamic updates).

Start Samba: run `samba`, or use the package's script or service file. Samba itself provides no init scripts, systemd, upstart or other service files.

Verification:
```
smbclient -L localhost -N
smbclient //localhost/netlogon -UAdministrator -c 'ls'
host -t SRV _ldap._tcp.samdom.example.com.
host -t SRV _kerberos._udp.samdom.example.com.
host -t A dc1.samdom.example.com.
host -t PTR 10.99.0.1
kinit administrator
klist
```
Expected shares: `netlogon` and `sysvol`. Always type the realm in uppercase for Kerberos.

If you do not pass `user@REALM` to `kinit`, the realm is appended automatically.

Kerberos requires synchronized time on all domain members; see ad-dc-time-sync.

## Checked
2026-11-04: krb5.conf copy and symlink warning, start notes, verification commands, expected shares and the uppercase realm rule compared with the Setting up Samba as an AD DC wiki page. Removed: a process-tree check, a samba -i tip and a five-minute clock figure the page does not state.
Method: documentation only; no commands were run.
