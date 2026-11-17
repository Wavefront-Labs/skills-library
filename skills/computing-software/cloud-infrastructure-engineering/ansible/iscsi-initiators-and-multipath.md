---
id: computing-software.cloud-infrastructure-engineering.ansible.iscsi-initiators-and-multipath
name: iscsi-initiators-and-multipath
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, storage-filesystems, iscsi, multipath, open-iscsi, dm-multipath, san]
level: advanced
status: docs-checked
description: "Attach SAN LUNs over iSCSI with community.general.open_iscsi (discovery, CHAP login, auto startup) and configure dm-multipath before creating filesystems."
sources: ["https://docs.ansible.com/ansible/latest/collections/community/general/open_iscsi_module.html", "https://man.archlinux.org/man/multipath.conf.5"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# iSCSI initiators and multipath

```yaml
- name: Multipath config before logging in
  ansible.builtin.copy:
    dest: /etc/multipath.conf
    content: |
      defaults {
        user_friendly_names yes
        find_multipaths yes
      }
  notify: Reload multipathd

- name: Discover and log in on both portals
  community.general.open_iscsi:
    portal: "{{ item }}"
    discover: true
    login: true
    auto_node_startup: true
    node_auth: CHAP
    node_user: "{{ iscsi_chap_user }}"
    node_pass: "{{ vault_iscsi_chap_pass }}"
  loop: [portal-a.example.com, portal-b.example.com]   # two fabrics = two paths
  no_log: true
```
Module facts from its page:
- `discover` (re)discovers targets on the portal and adds them to the persistent iSCSI database. Discovery resets configuration such as `node.startup` to manual, so combined with `auto_node_startup: true` it always reports changed. Run discovery once, then log in without `discover` on later runs if idempotent output matters.
- `login` (alias `state`) connects the target; when `target` is omitted it logs in to all available targets.
- `node_auth` sets `node.session.auth.authmethod` (default `CHAP`); `node_user` and `node_pass` set the session username and password; `node_user_in` sets the incoming username for mutual CHAP.
- `port` defaults to 3260. `show_nodes` returns the nodes in the persistent database; `rescan` rescans established sessions.

## Use the multipath device, never sdX
The multipath.conf(5) manual describes `multipaths` entries that match a LUN by `wwid` and assign an `alias`, so the mapper name stays stable. Build filesystems and mounts on the multipath device, not on one underlying path device.

## Gotchas
- CHAP credentials are secrets: use `no_log` and a vault for `node_pass`.
- The array's host and initiator mapping is an array-side task that must precede login.

## Checked
2026-11-01. Confirmed on the open_iscsi module page (options and defaults listed above, discovery resetting `node.startup`) and the multipath.conf(5) manual (`defaults`, `user_friendly_names`, `find_multipaths`, `multipaths`, `wwid`, `alias`). Removed (not on those pages): package names, initiator-name file, nvme blacklist, `mpathconf`, mount options such as `_netdev`, `multipath -ll`/`iscsiadm` checks, node file paths and real portal addresses.
Method: documentation only; no commands were run.
