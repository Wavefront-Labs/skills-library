---
id: computing-software.systems-network-administration.linux.iscsi-initiator-iscsiadm-and-sessions
name: iscsi-initiator-iscsiadm-and-sessions
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, iscsi, iscsiadm, iscsi-initiator, iscsid, iscsi-session, open-iscsi, initiatorname, chap, netdev, lpic-2, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Attach iSCSI LUNs with open-iscsi: initiator name, discovery, CHAP, login and automatic startup, persistent mounts with _netdev, and recovering or rescanning sessions."
sources:
  - https://github.com/open-iscsi/open-iscsi/blob/master/README
  - https://github.com/open-iscsi/open-iscsi/blob/master/etc/iscsid.conf
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# iSCSI initiator: iscsiadm and sessions

**Goal:** a host that logs in to its iSCSI LUNs at boot, mounts them only after the network is
up, and recovers cleanly from path or target outages.

## 1. Identity and service
```bash
dnf install iscsi-initiator-utils   # Debian/Ubuntu: open-iscsi
cat /etc/iscsi/initiatorname.iscsi  # InitiatorName=iqn.1994-05.com.redhat:… — target ACLs use this
systemctl enable --now iscsid.socket iscsi.service     # iscsi.service logs in to "automatic" nodes at boot
```
If the storage team assigned an IQN, set it in `initiatorname.iscsi` before the first login (restart iscsid afterwards).

## 2. Discover and log in
```bash
iscsiadm -m discovery -t sendtargets -p 10.0.10.5:3260
iscsiadm -m node                                    # discovered target/portal records
# CHAP (if the target requires it)
iscsiadm -m node -T iqn.2026-10.com.example:san1 -p 10.0.10.5 --op update -n node.session.auth.authmethod -v CHAP
iscsiadm -m node -T iqn.2026-10.com.example:san1 -p 10.0.10.5 --op update -n node.session.auth.username -v host01
iscsiadm -m node -T iqn.2026-10.com.example:san1 -p 10.0.10.5 --op update -n node.session.auth.password -v 'S3cret-12-16ch'
iscsiadm -m node -T iqn.2026-10.com.example:san1 -p 10.0.10.5 --login
iscsiadm -m node -T iqn.2026-10.com.example:san1 --op update -n node.startup -v automatic
lsblk                                               # the new sdX disk
```
`/etc/iscsi/iscsid.conf` holds the defaults (commented `node.session.auth.*` examples); per-node
values are set with `iscsiadm -m node --op update`. Mutual CHAP adds `username_in`/`password_in`.
`node.session.auth.authmethod` is currently ignored: CHAP is used whenever credentials are set, a
behaviour the file calls deprecated. The `iscsid.conf` default for `node.startup` is `manual`.

## 3. Sessions
```bash
iscsiadm -m session                       # active sessions
iscsiadm -m session -P 3                  # detail: state, attached disks, iface, timeouts
iscsiadm -m session -r <sid> --rescan     # SCSI scan of one session for new LUNs (sid from -m session)
iscsiadm -m node -T <iqn> -p <portal> --logout
iscsiadm -m node -o delete -T <iqn>       # forget the record
```
Timeouts: `node.session.timeo.replacement_timeout` (default 120 s in `iscsid.conf`) — how long to
wait for session re-establishment before SCSI commands fail up to multipath, the filesystem or the
application. With dm-multipath the README says to fail commands quickly to the multipath layer
(and use queue_if_no_path there); for a root disk or no multipath it says the opposite, for
example 86400 with NOP-Out pings off.

## 4. Persistent mounts
```
UUID=…  /data  xfs  _netdev,nofail  0 0
```
`_netdev` orders the mount after network and iSCSI login. Reference by UUID or
`/dev/disk/by-path/ip-…-iscsi-…-lun-0` / `by-id` (sdX changes).

## Gotchas
- Login works but no disk appears → target ACL doesn't contain this IQN, or LUN not mapped.
- Two NICs to the same target without multipath → the same LUN appears twice; use multipath.
- Cloned VMs share the same InitiatorName; generate a new one with `iscsi-iname` (shipped with open-iscsi) and put it in `initiatorname.iscsi`.

## Verify
- [ ] `iscsiadm -m session -P 3` shows "LOGGED IN" and the attached disk.
- [ ] Reboot: session restores automatically and the fs mounts without manual steps.

## Checked

Checked 2026-10-26 against the open-iscsi README and etc/iscsid.conf (open-iscsi/open-iscsi master, last commit 2026-10-06). Confirmed: discovery, login, logout and node delete commands, CHAP parameter names (authmethod, username, password, username_in, password_in), node.startup default manual, replacement_timeout default 120 and the multipath versus root-disk guidance (section 8.1), per-session rescan with -r sid --rescan, _netdev in fstab, socket-activated iscsid and iscsi.service, iscsi-iname. Corrected: the claimed 5-15 s replacement timeout figure and the session -R form; authmethod is currently ignored when credentials are set; removed the lsblk TRAN claim and the double-login claim.

Method: documentation only; no commands were run.
