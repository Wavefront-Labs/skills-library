---
id: computing-software.systems-network-administration.linux.nfsv4-idmapd-domain
name: nfsv4-idmapd-domain
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, nfs, idmapd, nfsidmap, nfsv4, nobody-ownership, idmapd-conf, nfs4-domain]
level: practitioner
status: docs-checked
description: "Fix files showing as nobody:nobody on NFSv4: Domain in idmapd.conf on client and server, nfsidmap cache, sec=sys numeric ID fallback, and AD/LDAP name consistency."
sources:
  - https://man.archlinux.org/man/idmapd.conf.5
  - https://man7.org/linux/man-pages/man8/nfsidmap.8.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# NFSv4 ID mapping

**Symptom:** on an NFSv4 mount every file is owned by `nobody:nobody` (or similar), and `chown` fails.

## How it works
NFSv4 sends owners as `user@domain` names. Per idmapd.conf(5), an NFSv4 domain is a namespace with one unique
username-to-UID and groupname-to-GID mapping, so client and server must use the same domain and resolve the same user
names. Mismatch leads to the unmapped (nobody) identity.

## Fix
`/etc/idmapd.conf` on **both** sides:
```ini
[General]
Domain = example.com
```
The `Domain` default is the host's fully qualified DNS domain name (per the man page), so hosts in different DNS
domains (`corp.example.com` vs `example.com`) disagree unless you set it.
```bash
nfsidmap -c                         # clear the keyring of all keys (client-side idmap cache)
umount /srv/share && mount /srv/share
```
The kernel uses the request-key mechanism to call `/usr/sbin/nfsidmap` for name lookups. Check that the same user
name resolves to the same UID on client and server.

## Gotchas
- A user that exists only on one side maps to nobody on the other.
- Restart or reload procedure for the server idmap service, and numeric-ID behaviour with `sec=sys`, depend on the
  distribution and kernel: check the distribution's NFS documentation.

## Verify
- [ ] `ls -ln` and `ls -l` on the mount show real owners; a file created on the client shows the same owner on the server.

## Checked
2026-10-28. Confirmed in idmapd.conf(5) and nfsidmap(8): `Domain` meaning and default, `nfsidmap -c`, request-key
upcall. Removed as unconfirmed (the Red Hat chapter was a landing page without these details): `nfs-idmapd` service
restart, `nfs4_disable_idmapping` module parameters, the sec=sys numeric ID fallback and Kerberos statements, container
UID-namespace note, EPERM behaviour.
Method: documentation only; no commands were run.
