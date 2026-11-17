---
id: computing-software.systems-network-administration.cisco-networking.openconfig-vs-native-vs-ietf-yang-models
name: openconfig-vs-native-vs-ietf-yang-models
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, yang, openconfig, ietf-yang, cisco-native-yang, netconf, restconf, gnmi, model-driven-programmability, ios-xe]
level: practitioner
status: draft
description: "Choose between Cisco native, IETF and OpenConfig YANG models on IOS XE: coverage, portability, mixing in one transaction, and finding the path you need."
sources:
  - https://github.com/YangModels/yang/tree/main/vendor/cisco/xe
  - https://www.openconfig.net/projects/models/
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/1712/b_1712_programmability_cg/m_1712_prog_yang_netconf.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Native vs OpenConfig vs IETF YANG models

## The three families on IOS XE
| Family | Example module | Strength | Weakness |
|---|---|---|---|
| Cisco native | `Cisco-IOS-XE-native` (config), `Cisco-IOS-XE-*-oper` (state) | covers nearly every CLI feature; maps closely to CLI | vendor-specific; changes across releases |
| IETF | `ietf-interfaces`, `ietf-ip`, `ietf-routing` | standard, stable | small feature coverage |
| OpenConfig | `openconfig-interfaces`, `openconfig-network-instance`, `openconfig-bgp` | vendor-neutral, operator-designed, good for telemetry | partial feature coverage per vendor; deviations |

## Choosing
- Multi-vendor estate with common features (interfaces, BGP, LLDP, telemetry): OpenConfig, plus
  native for gaps.
- Cisco-only, broad feature use: native models (fastest path; mirrors CLI).
- Avoid configuring the same object through two families in different tools: they are the same
  datastore underneath, and one tool will see unexplained changes.

## Finding paths
- Device capabilities: NETCONF hello lists supported modules and **deviations**
  (`Cisco-IOS-XE-openconfig-*-deviation`); deviations say what OpenConfig leaves are not supported.
- YANG Suite (Cisco) or `pyang -f tree openconfig-interfaces.yang` to browse.
- Get the native model for a CLI line: configure it, then
  `show running-config | format netconf-xml` (or `restconf-json`) on IOS XE 17.x.
- Operational data: `Cisco-IOS-XE-*-oper` models or OpenConfig state containers.

## Gotchas
- OpenConfig on IOS XE may require `netconf-yang` with `openconfig` features enabled per release.
- Model versions are pinned to IOS XE releases (github YangModels vendor/cisco/xe/<release>).
- Some OpenConfig edits translate to multiple native lines; read back with native to confirm.

## Verify
- [ ] `get` of the same interface via native and OpenConfig returns consistent values.
