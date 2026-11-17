---
id: computing-software.cloud-infrastructure-engineering.ansible.interfaces-and-vlans-with-resource-modules
name: interfaces-and-vlans-with-resource-modules
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, network-automation, ios-vlans, ios-interfaces, ios-l2-interfaces, resource-module-states, switchport]
level: practitioner
status: docs-checked
description: "Configure VLANs, interface descriptions and access/trunk switchports with cisco.ios resource modules, choosing merged, replaced, overridden or deleted state safely."
sources: ["https://github.com/ansible-collections/cisco.ios/blob/main/plugins/modules/ios_vlans.py", "https://github.com/ansible-collections/cisco.ios/blob/main/plugins/modules/ios_interfaces.py", "https://github.com/ansible-collections/cisco.ios/blob/main/plugins/modules/ios_l2_interfaces.py", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/network/user_guide/network_resource_modules.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interfaces and VLANs with resource modules

Data model in host_vars (source of truth):
```yaml
vlans:
  - {vlan_id: 10, name: users}
  - {vlan_id: 20, name: voice}
  - {vlan_id: 99, name: mgmt}
interfaces:
  - {name: GigabitEthernet1/0/1, description: "desk 1A", enabled: true}
  - {name: GigabitEthernet1/0/48, description: "uplink core1", enabled: true, mtu: 9198}
l2_interfaces:
  - {name: GigabitEthernet1/0/1, mode: access, access: {vlan: 10}, voice: {vlan: 20}}
  - name: GigabitEthernet1/0/48
    mode: trunk
    trunk: {allowed_vlans: "10,20,99", native_vlan: 99}
```
```yaml
- cisco.ios.ios_vlans:
    config: "{{ vlans }}"
    state: merged
- cisco.ios.ios_interfaces:
    config: "{{ interfaces }}"
    state: replaced
- cisco.ios.ios_l2_interfaces:
    config: "{{ l2_interfaces }}"
    state: replaced
- cisco.ios.ios_config:
    save_when: modified
```

## States
| State | Effect |
|---|---|
| `merged` | add/update given attributes; never removes |
| `replaced` | for each listed item, make it exactly as given (removes unlisted attributes of that item) |
| `overridden` | whole resource = exactly the list: unlisted VLANs/interfaces config removed |
| `deleted` | remove given items (or all if config empty) |
| `gathered` / `rendered` / `parsed` | read from the device / render CLI offline / parse supplied text (`running_config`) |

Use `merged` while onboarding, `replaced` for managed ports, `overridden` only when the data is
complete (it will delete VLANs not in your list — including ones other teams use).

## Rollout safety
- Run `--check` first and read `commands`.
- Never touch the uplink/management interface in the same batch as access ports; keep `serial` small.
- `save_when: modified` saves when running differs from startup; `changed` saves only when this task changed something.

Equivalent modules exist for other platforms (`arista.eos.eos_vlans`, `cisco.nxos.nxos_vlans`,
`junipernetworks.junos.junos_vlans`) with the same state names.

## Gotchas
- Give interface names in full (the module docs use `GigabitEthernet0/2`), not abbreviations.
- `allowed_vlans` lists the only VLANs configured on the trunk, so `replaced` overwrites the list; use `merged` to add one VLAN.

## Verify
- [ ] Second run: `changed=0`.
- [ ] `show vlan brief` and `show interfaces trunk` match the data.

## Checked

Checked 2026-10-26 against the cisco.ios `ios_vlans`, `ios_interfaces` and `ios_l2_interfaces` module sources (main) and the Ansible network resource module page. Confirmed: `vlan_id`, `name` and `state` (active or suspend) on VLANs; `name`, `description`, `enabled`, `mtu` on interfaces; `mode`, `access.vlan`, `voice.vlan`, `trunk.allowed_vlans` (list of strings, ranges such as `10-20,40` allowed) and `native_vlan` on L2 interfaces; the states merged, replaced, overridden, deleted, rendered, gathered and parsed; resource modules have no save option, so a final `ios_config` save task is needed. Removed the unconfirmed VTP remark.

Method: documentation only; no commands were run.
