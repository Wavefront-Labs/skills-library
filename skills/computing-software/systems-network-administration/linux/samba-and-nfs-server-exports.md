---
id: computing-software.systems-network-administration.linux.samba-and-nfs-server-exports
name: samba-and-nfs-server-exports
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, samba, smb-server, smbd, smb-conf, testparm, smbpasswd, nfs-server, exports, exportfs, nfsv4, root-squash, no-root-squash, pseudo-root, sec-krb5, firewalld-nfs, selinux-samba, file-sharing, lpic-2, sysadmin, valid-users, idmap, smbclient, smbstatus]
level: practitioner
status: docs-checked
description: "Share directories from a Linux server: NFSv4 exports with squash/sec options, Samba shares for Windows/macOS clients, plus firewall, SELinux and permission alignment."
sources:
  - https://man7.org/linux/man-pages/man5/exports.5.html
  - https://man7.org/linux/man-pages/man8/exportfs.8.html
  - https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/deploying_different_types_of_servers/index
licence: Apache-2.0
version: 6
updated: 2026-11-17
---

# Samba and NFS server exports — share a directory without sharing root

**Goal:** export directories to Linux clients (NFS) and Windows/macOS clients (SMB)
with correct identity mapping, no accidental root access, and firewall/SELinux that
let it work.

## 1. NFS server (NFSv4 only unless legacy clients force v3)
```bash
dnf install nfs-utils          # apt install nfs-kernel-server
mkdir -p /export/data && chown nobody:nobody /export/data   # or a real group
```
`/etc/exports`:
```
/export            10.0.0.0/8(ro,fsid=0,crossmnt,sec=sys)        # v4 pseudo-root (optional on modern kernels)
/export/data       10.0.0.0/8(rw,sync,root_squash,no_subtree_check)
/export/homes      10.0.0.0/8(rw,sync,root_squash,no_subtree_check,sec=krb5p)
/export/backups    10.0.5.9(rw,sync,no_root_squash,no_subtree_check)   # one trusted host only
```
```bash
exportfs -rav                  # re-read exports; -s shows effective options
systemctl enable --now nfs-server
firewall-cmd --add-service=nfs --permanent && firewall-cmd --reload      # v3 needs more services (mountd, rpc-bind) than v4
```
- `root_squash` (default) maps client root to the anonymous uid/gid; `no_root_squash` only for backup
  hosts you trust as root. `all_squash,anonuid=1500,anongid=1500` makes every client
  user one local user (simple shared drop folders).
- `sync` is the safe default; `async` risks losing acknowledged writes on crash.
- `no_subtree_check` on everything (subtree checks cause stale handles on renames).
- Options are host-specific and **whitespace matters**: `host (rw)` (space) exports rw
  to the world and ro to host.
- Identity: v4 sends user *names*, so the idmap domain must match on server and clients (see idmapd.conf(5)),
  or owners show as the anonymous user. With `sec=sys` UIDs must match anyway (use SSSD/LDAP for consistency).
  `sec=` takes a colon-delimited list of flavours (`sys`, `krb5`, `krb5i`, `krb5p`).
- SELinux: exported directories may need an SELinux boolean or label; read the audit log for the denial.

## 2. Samba server
```bash
dnf install samba samba-common-tools     # apt install samba
```
`/etc/samba/smb.conf`:
```ini
[global]
    workgroup = WORKGROUP
    server string = files
    security = user
    server min protocol = SMB3_00
    smb encrypt = desired
    map to guest = Bad User          # unknown users become guest only on guest-ok shares
    log file = /var/log/samba/%m.log
    max log size = 1000
    # AD member instead: security = ADS, realm = CORP.EXAMPLE, idmap config * : backend = tdb, idmap config CORP : backend = rid, idmap config CORP : range = 100000-999999 ; join with net ads join -U Administrator

[data]
    path = /srv/samba/data
    browseable = yes
    read only = no
    valid users = @staff
    force group = staff
    create mask = 0664
    directory mask = 2775
    vfs objects = acl_xattr
    map acl inherit = yes

[homes]
    comment = Home Directories
    browseable = no
    read only = no
    valid users = %S

[public]
    path = /srv/samba/public
    guest ok = yes
    read only = yes
```
```bash
testparm -s                                  # validates and prints effective config
smbpasswd -a alice                           # Samba keeps its own password DB (tdbsam); user must exist locally
pdbedit -L
mkdir -p /srv/samba/data && chgrp staff /srv/samba/data && chmod 2775 /srv/samba/data
systemctl enable --now smb nmb               # Debian: smbd nmbd; nmb only for NetBIOS browsing (optional)
firewall-cmd --add-service=samba --permanent && firewall-cmd --reload
smbclient -L localhost -U alice; smbclient //localhost/data -U alice -c 'ls'
smbstatus                                    # sessions, locked files
```
- Permissions are the intersection of Samba share rights and Unix mode/ACLs; the
  usual "access denied" is the directory lacking group write or the setgid bit.
- `force group` + `directory mask 2775` keep collaborative shares writable by all members.
- Windows ACL editing from the Security tab needs `vfs objects = acl_xattr` and `map acl inherit = yes`;
  the filesystem must support ACLs and extended attributes.
- macOS clients use the `vfs_fruit` module (see its man page for Time Machine and Finder metadata options).
- With no printers, set `load printers = no` (and `printcap name`) to stop printer enumeration.
- SMB1 is a legacy protocol; keep `server min protocol` at SMB2 or higher rather than re-enabling it for an old scanner — fix the scanner.
- SELinux: shared directories need a Samba share label, and `[homes]` needs the home-directory boolean; read the audit log for the denial.

## 3. Same directory over both
Export the same path over NFS (Linux) and SMB (Windows) with the same group ownership.
Samba's `kernel share modes` defaults to `no` (SMB2 durable handles need it off) and gives only minimal
interoperability with local processes and NFS, so do not rely on locks being shared between the two protocols.

## Checked
2026-11-01. Confirmed against exports(5) (squash options, `sec=`, `crossmnt`, `fsid=0`, `sync` default, `no_subtree_check`,
`anonuid`/`anongid`) and smb.conf(5) (parameter names, SMB3_00 value, `smb encrypt` desired, `kernel share modes`
default, `load printers`, `map acl inherit`). Removed: nfsd version-disable recipe, port lists, idmapd path,
Kerberos principal detail, macOS fruit options, mount-option detail, ss/nfsstat commands.
Method: documentation only; no commands were run.

## Verify
- [ ] `exportfs -s` lists the exports with the intended squash/sec options; a client mounts and files show real owners.
- [ ] `testparm -s` clean; `smbclient //server/data -U alice` can `put` a file and it lands with group `staff`, mode 0664.
- [ ] From an un-allowed subnet / unknown user, the mount or `smbclient` is refused.
