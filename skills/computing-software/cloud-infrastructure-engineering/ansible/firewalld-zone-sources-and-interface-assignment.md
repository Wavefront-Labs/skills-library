---
id: computing-software.cloud-infrastructure-engineering.ansible.firewalld-zone-sources-and-interface-assignment
name: firewalld-zone-sources-and-interface-assignment
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, firewalld, firewalld-source, firewalld-interface, firewall-zones, ansible-posix, nmcli, network-manager, rhel]
level: practitioner
status: docs-checked
description: "Bind firewalld zones to source networks and interfaces with Ansible so traffic lands in the intended zone, survives reboots and NetworkManager, and is verified."
sources: ["https://github.com/ansible-collections/ansible.posix/blob/main/plugins/modules/firewalld.py", "https://firewalld.org/documentation/zone/", "https://github.com/firewalld/firewalld/blob/main/doc/xml/firewalld.zones.xml", "https://github.com/ansible-collections/community.general/blob/main/plugins/modules/nmcli.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# firewalld zone sources and interface assignment

Goal: decide which zone a packet is judged by. firewalld zones can be bound to connections, interfaces
and source addresses, and an interface without a zone uses the default zone. Getting the bindings
wrong means your carefully opened `internal` zone is never used.

## Bind a source network to a zone
```yaml
- name: Admin network gets the internal zone
  ansible.posix.firewalld:
    zone: internal
    source: 10.10.0.0/16
    permanent: true
    immediate: true
    state: enabled

- name: Only internal allows ssh
  ansible.posix.firewalld:
    zone: internal
    service: ssh
    permanent: true
    immediate: true
    state: enabled

- name: Public zone does not
  ansible.posix.firewalld:
    zone: public
    service: ssh
    permanent: true
    immediate: true
    state: disabled
```
Result: SSH only from 10.10.0.0/16, everything else on the NIC stays in `public`.
The module's `source` option takes the network to add to or remove from the zone.

## Assign an interface to a zone
On NetworkManager systems the connection profile owns the zone; set it there so it survives
`nmcli con up` and reboots:
```yaml
- community.general.nmcli:
    conn_name: ens224
    ifname: ens224
    type: ethernet
    zone: dmz
    state: present
```
Fallback without NM control:
```yaml
- ansible.posix.firewalld: {zone: dmz, interface: ens224, permanent: true, immediate: true, state: enabled}
```
The `firewall` system role (`rhel-system-roles.firewall`) can also assign zones.

## Gotchas
- `permanent: true` alone changes only the saved config (`immediate` defaults to false when `permanent` is true); add `immediate: true` or reload, or the running firewall is unchanged until reload or reboot.
- A connection, interface or source can only be part of one zone. Remove it from the old zone in the same play first.
- With NetworkManager the zone is stored in the connection profile (the ifcfg `ZONE=` setting), so pick one owner for the assignment rather than setting it in both places.
- Avoid overlapping sources across zones.
- Changing the default zone moves every interface that has no zone binding at once.

## Verify
- [ ] `firewall-cmd --get-active-zones` lists the source/interface under the expected zone.
- [ ] `firewall-cmd --zone=internal --list-all` shows the source and services; from an outside address `nc -zv host 22` is refused.
- [ ] After `nmcli con up ens224` or a reboot the assignment is still there.

## Checked

Checked 2026-10-26 against the ansible.posix `firewalld` module source (main), the firewalld manual sources and firewalld.org zone documentation. Confirmed: module options `zone`, `source`, `interface`, `service`, `permanent` (default false), `immediate` (default false; true when permanent is false), `state`; a connection, interface or source can only be part of one zone; the NetworkManager `ZONE=` ifcfg storage; community.general `nmcli` has a `zone` option. Removed the zone-selection order claim (source before interface), the ipset source claim (the module has no ipset option) and the overlapping-prefix remark, which no page states.

Method: documentation only; no commands were run.
