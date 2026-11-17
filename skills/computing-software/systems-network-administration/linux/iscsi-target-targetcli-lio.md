---
id: computing-software.systems-network-administration.linux.iscsi-target-targetcli-lio
name: iscsi-target-targetcli-lio
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, iscsi, targetcli, iscsi-target, lio, chap, backstores, luns, acls, tpg, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Export block storage over iSCSI with the kernel LIO target via targetcli: backstores, IQNs, LUNs, initiator ACLs, CHAP authentication, portals, firewall and saving config."
sources:
  - https://github.com/open-iscsi/targetcli-fb/blob/master/targetcli.8
  - https://github.com/open-iscsi/targetcli-fb/blob/master/README.md
  - https://github.com/open-iscsi/targetcli-fb/tree/master/src/targetcli
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# iSCSI target with targetcli (LIO)

**Goal:** serve an LV or file as an iSCSI LUN to specific initiators, with CHAP, surviving
reboots.

## 1. Install
```bash
dnf install targetcli && systemctl enable --now target    # target.service restores saved config at boot
firewall-cmd --permanent --add-service=iscsi-target && firewall-cmd --reload   # 3260/tcp
```

## 2. Build the object tree
```bash
targetcli
/> backstores/block create name=lun_db dev=/dev/vg_san/db          # block device (preferred)
/> backstores/fileio create name=lun_lab file_or_dev=/srv/lab.img size=20G   # file-backed
/> iscsi/ create iqn.2026-10.com.example:san1                       # creates tpg1 + default portal on all addresses ([::0]) port 3260
/> cd iscsi/iqn.2026-10.com.example:san1/tpg1
/iscsi/…/tpg1> luns/ create /backstores/block/lun_db                # LUN 0
/iscsi/…/tpg1> acls/ create iqn.1994-05.com.redhat:host01           # only this initiator; LUN mappings auto-added while auto_add_mapped_luns is true
/iscsi/…/tpg1> portals/ delete ::0 3260                             # the default portal (address as shown by ls)
/iscsi/…/tpg1> portals/ create 10.0.10.5 3260                       # listen on the storage network only
/> ls                                                                # review the tree
/> saveconfig                                                        # → /etc/target/saveconfig.json
/> exit                                                              # also saves (auto_save_on_exit)
```

## 3. CHAP
Per ACL (recommended):
```bash
/iscsi/…/tpg1/acls/iqn.1994-05.com.redhat:host01> set auth userid=host01 password=S3cret-12-16ch
# mutual CHAP: set auth mutual_userid=san1 mutual_password=An0ther-12-16ch
/iscsi/…/tpg1> set attribute authentication=1
```
LIO uses the per-ACL credentials only when the TPG attribute `generate_node_acls` is 0; with `generate_node_acls=1`
("ignore ACLs mode") the TPG-wide `set auth` values and LUN mapping apply instead. Discovery-session CHAP is separate:
`set discovery_auth userid=... password=...` at the top-level `iscsi` node. Authentication is switched off with
`set attribute authentication=0`. TPG-wide mode with no ACLs is for labs only.

## 4. Operate
```bash
targetcli ls /iscsi                          # sessions show under ACLs when logged in
targetcli sessions detail
targetcli /backstores/block/lun_db info
targetcli clearconfig confirm=True           # wipe running config (careful)
```
Resizing: grow the LV, then initiators rescan (`iscsiadm -m session -r <sid> --rescan`). The fileio backstore
takes `write_back=` (default true, which enables the local filesystem cache: faster, higher risk of data loss on a crash).

## Gotchas
- Forgetting `saveconfig` (or exiting with auto-save off) → config gone after reboot.
- ACL IQN typo = initiator logs in but sees no LUNs.
- Exporting the same LV to two initiators without a cluster filesystem corrupts data — that's
  a design decision, not a bug.
- LVM filter: on the target host, exclude exported LVs from LVM scanning if initiators put LVM inside them.

## Verify
- [ ] `targetcli ls` shows LUN, ACL and portal on the storage IP; `/etc/target/saveconfig.json` updated.
- [ ] Initiator discovery + login succeeds with correct CHAP and fails with a wrong password.
- [ ] After `systemctl restart target` (or reboot) the config is intact.

## Checked

Checked 2026-10-26 against targetcli.8 and the src/targetcli sources of open-iscsi/targetcli-fb (master, last commit 2026-08-19) and firewalld's iscsi-target service definition. Confirmed: object tree and create commands (block, fileio with write_back default true), default portal on [::0]:3260, TPG and ACL authentication rules (generate_node_acls selects TPG versus ACL credentials, discovery_auth, authentication attribute), auto_save_on_exit default true, saveconfig path /etc/target/saveconfig.json, clearconfig confirm, sessions detail, auto_add_mapped_luns, target.service for restore on boot. Corrected: default portal address; removed the unconfirmed 12-16 character password rule.

Method: documentation only; no commands were run.
