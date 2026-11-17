---
id: computing-software.systems-network-administration.cisco-networking.ise-device-administration-policy-sets
name: ise-device-administration-policy-sets
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ise, ise-device-admin, tacacs-plus, device-administration, policy-sets, command-sets, shell-profiles, network-device-groups]
level: practitioner
status: draft
description: "Set up Cisco ISE device administration (TACACS+): network device groups, policy sets, shell profiles and command sets, and the matching IOS AAA config."
sources:
  - https://www.cisco.com/c/en/us/td/docs/security/ise/3-2/admin_guide/b_ise_admin_3_2/b_ISE_admin_32_device_admin.html
  - https://www.cisco.com/c/en/us/support/docs/security/identity-services-engine/200208-Configure-ISE-2-0-IOS-TACACS-Authentic.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ISE device administration policy sets

## Enable
Administration > Deployment > (PSN) > enable **Device Admin Service** (licence: Device Admin).
Work Centers > Device Administration is where everything lives.

## Objects
| Object | Purpose |
|---|---|
| Network Device Groups (Location, Device Type) | match devices in policy: `DEVICE:Device Type EQUALS Routers` |
| Network Devices | IP/range, TACACS+ shared secret, NDGs |
| TACACS Profiles (shell profiles) | default/maximum privilege, custom attributes |
| TACACS Command Sets | permit/deny commands by regex (`permit show .*`, `deny reload`) |
| Policy Sets | condition on device/NDG/protocol; authentication policy (identity source: AD) and authorization rules |

## Example authorization rules (policy set "Network Devices")
| Rule | Condition | Command set | Shell profile |
|---|---|---|---|
| NetAdmins | AD group Network-Admins | PermitAll | Priv15 |
| NOC | AD group NOC | ShowOnly (`show .*`, `ping .*`, `traceroute .*`) | Priv1 |
| Default | any | DenyAll | DenyAccess |

## IOS side
```
aaa new-model
tacacs server ISE-1
 address ipv4 10.0.0.31
 key <SECRET>
aaa group server tacacs+ ISE-TACACS
 server name ISE-1
 ip tacacs source-interface Loopback0
aaa authentication login VTY group ISE-TACACS local
aaa authorization exec VTY group ISE-TACACS local if-authenticated
aaa authorization commands 1 VTY group ISE-TACACS local if-authenticated
aaa authorization commands 15 VTY group ISE-TACACS local if-authenticated
aaa accounting commands 15 default start-stop group ISE-TACACS
aaa authorization console                      ! only if you want command authz on console too
line vty 0 15
 login authentication VTY
 authorization exec VTY
 authorization commands 1 VTY
 authorization commands 15 VTY
```
Keep a local emergency user and test console access before applying command authorization.

## Verify
- ISE: Operations > TACACS > Live Logs shows authentication and per-command authorization.
- Device: `show tacacs`, `test aaa group ISE-TACACS <user> <pw> legacy`.
- [ ] NOC user cannot run `configure terminal`; admin can; local fallback works with ISE unreachable.
