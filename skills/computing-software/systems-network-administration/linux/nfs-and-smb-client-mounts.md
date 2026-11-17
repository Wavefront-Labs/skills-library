---
id: computing-software.systems-network-administration.linux.nfs-and-smb-client-mounts
name: nfs-and-smb-client-mounts
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, nfs, nfs-mount, nfsv4, smb, cifs, cifs-utils, autofs, automount, systemd-automount, fstab, network-filesystem, credentials-file, kerberos-nfs, sec-krb5, mount-options, rhcsa, storage, sysadmin, showmount, autofs-maps, cifs-permissions, stale-file-handle, nfs-mount-options]
level: practitioner
status: docs-checked
description: "Mount NFS and SMB/CIFS shares on Linux clients: fstab options that don't hang boot, credentials files, autofs maps, systemd automount, and stale-handle recovery."
sources:
  - https://man7.org/linux/man-pages/man5/nfs.5.html
  - https://man7.org/linux/man-pages/man8/mount.cifs.8.html
  - https://man7.org/linux/man-pages/man5/autofs.5.html
  - https://man7.org/linux/man-pages/man5/systemd.automount.5.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# NFS and SMB client mounts — persistent, on-demand, and boot-safe

**Goal:** mount remote shares so they appear when needed, don't wedge boot when the
server is down, and carry the right identity.

## 1. NFS
```bash
dnf install nfs-utils          # apt install nfs-common
showmount -e nas.example       # NFSv3 export list (needs rpcbind on server); v4 just mount /
mount -t nfs -o vers=4.2 nas.example:/export/data /mnt/data
nfsstat -m                      # negotiated options per mount
```
fstab, non-root data share:
```
nas.example:/export/data  /mnt/data  nfs  vers=4.2,_netdev,nofail,x-systemd.automount,x-systemd.idle-timeout=600,noatime  0 0
```
- `_netdev` + `nofail`: wait for network, don't fail boot. `x-systemd.automount` mounts
  on first access (so boot doesn't block at all) — this pair is the sane default.
- `hard` (default) vs `soft`: `hard` retries forever and processes hang in `D` state
  while the server is down but data is never silently corrupted; `soft` returns an error
  after `retrans` retries. The nfs(5) page warns that a soft timeout can cause silent data corruption:
  use `hard` for application data and `soft` only where responsiveness matters more than integrity,
  never for databases or write workloads. `intr` is ignored since kernel 2.6.25.
- NFSv4 maps users by **name** (see `rpc.idmapd(8)`); if files show as `nobody`,
  the ID-mapping settings differ between client and server (or `sec=sys` is used with
  mismatched UIDs on v3).
- Kerberos: `sec=krb5p` (auth+integrity+privacy); the client needs a Kerberos
  host keytab (`/etc/krb5.keytab`) with the requisite service principals.
- `rsize`/`wsize` are negotiated to the largest value both sides support (at most 1048576 per nfs(5)); leave them unless the server is old.

## 2. SMB / CIFS
```bash
dnf install cifs-utils
mount -t cifs //fileserver/share /mnt/share -o credentials=/etc/samba/cred-share,vers=3.1.1,uid=1000,gid=1000,file_mode=0664,dir_mode=0775
```
`/etc/samba/cred-share` (mode `0600`):
```
username=svc_share
password=<PASSWORD>
domain=CORP
```
fstab:
```
//fileserver/share  /mnt/share  cifs  credentials=/etc/samba/cred-share,vers=3.1.1,_netdev,nofail,x-systemd.automount,uid=1000,gid=1000,iocharset=utf8  0 0
```
- Never put the password in fstab (world-readable). `credentials=` file only.
- `vers=1.0` is the classic SMB1 protocol; if an old NAS needs it, you
  have a security problem, not a mount problem.
- `uid=/gid=/file_mode=` only matter when the server doesn't return Unix ownership
  (CIFS Unix extensions unavailable). Use `multiuser` when
  several users share one mount and need their own credentials.
- Domain SSO: `sec=krb5` with a user ticket, or `cruid=` to pick whose ccache to use.
- `cache=none` for shared databases/lock-sensitive files; default `cache=strict` (the default since kernel 3.7) is fine
  for documents.

## 3. autofs (per-user home dirs, many shares)
```
# /etc/auto.master
/-          /etc/auto.direct   --timeout=300
/export/home /etc/auto.home
# /etc/auto.direct
/mnt/data   -fstype=nfs4,soft   nas.example:/export/data
# /etc/auto.home  (wildcard: /export/home/<user> -> nas:/export/home/<user>)
*  -fstype=nfs4   nas.example:/export/home/&
```
`systemctl enable --now autofs`; `automount -f -v` in the foreground for debugging map
syntax. autofs is still the right tool for wildcard/LDAP-driven maps; for a handful of
fixed shares, `x-systemd.automount` in fstab is simpler.

## 4. Diagnosing hangs and stale handles
```bash
findmnt -t nfs,nfs4,cifs
cat /proc/fs/nfsfs/servers; ss -tn state established '( dport = :2049 )'
dmesg | grep -iE 'nfs|cifs'          # "server not responding"
umount -f -l /mnt/data               # force + lazy when the server is gone
```
- `Stale file handle`: the export was re-created or the file replaced on the server;
  `umount -l` and remount.
- Boot stuck at "A start job is running for /mnt/data": you forgot `nofail`/`_netdev`.
  Edit fstab from the emergency shell (`mount -o remount,rw /`).
- Permission denied with correct creds on CIFS: check `vers=`, then whether the share
  requires signing/encryption (`seal`), then SELinux denials in the audit log for home directories.

## Verify
- [ ] Share mounts at boot without delay, and `findmnt` shows the intended `vers`/`sec`.
- [ ] Ownership on created files matches expectations (`ls -ln` vs server UID/username).
- [ ] With the server unreachable, the host still boots and `ls /mnt` returns within the timeout.

## Checked

2026-10-28

Confirmed: nfs(5) (hard/soft and the data-corruption warning, retrans, intr ignored since 2.6.25, nconnect, rsize/wsize negotiation, sec=krb5 and the host keytab), mount.cifs(8) (credentials, vers, cruid, multiuser, seal, cache modes and the 3.7 default, file_mode/dir_mode/uid/gid, Unix extensions, iocharset), autofs(5) and auto.master(5) (wildcard key and ampersand, --timeout), automount(8), systemd.mount(5) (_netdev, nofail, x-systemd.automount, idle-timeout), showmount(8).

Removed or corrected: The soft example in the fstab line (it contradicted the advice to use hard), the timeo*retrans formula, the nfs4_disable_idmapping and idmapd.conf Domain claims, rpc-gssd and nfs-client.target, cifscreds, the 'SMB3 norm' and 'disabled almost everywhere' claims, and the SELinux boolean names and STATUS_ACCESS_DENIED example.

Method: documentation only; no commands were run.
