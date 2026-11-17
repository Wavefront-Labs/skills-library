---
id: computing-software.it-support-helpdesk.device-provisioning.multicast-os-deployment
name: multicast-os-deployment
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, multicast-deployment, wds, configmgr, imaging, igmp-snooping]
level: advanced
status: draft
description: "Deploy OS images by multicast with WDS or ConfigMgr: when it pays off, auto-cast vs scheduled sessions, network prerequisites like IGMP snooping, and slow-client problems."
sources:
  - https://learn.microsoft.com/en-us/intune/configmgr/osd/deploy-use/use-multicast-to-deploy-windows-over-the-network
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/dd637994(v=ws.10)
  - https://learn.microsoft.com/en-us/windows/deployment/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multicast OS deployment

**When it pays off:** imaging many machines at once (classroom refresh, 50 laptops on a bench). One stream serves all clients instead of N unicast copies. For a handful of devices, unicast or cloud provisioning (Autopilot) is simpler.

## Options
- **WDS multicast transmissions** for install images (WDS console > Multicast Transmissions > Create):
  - **Auto-Cast**: starts when the first client joins; late joiners pick up mid-stream and get the missed part afterwards.
  - **Scheduled-Cast**: waits for N clients or a time, then starts; best for planned bench imaging.
- **ConfigMgr**: enable multicast on the distribution point (Properties > Multicast tab, address range, UDP port range, max clients), then on the OS image package: "Allow this package to be transferred via multicast", and the task sequence deployment uses "Download content locally when needed".
- Third-party: FOG, Clonezilla SE (UDPcast) for non-Windows or lab environments.

## Network prerequisites
- Switches with **IGMP snooping** and an **IGMP querier** on the VLAN, or multicast floods every port.
- Routing multicast across subnets needs PIM; simpler to keep clients on the server's VLAN or use a DP per site.
- Allow UDP port range in firewalls; Wi-Fi multicast is slow and unreliable, use wired.

## Tuning
- WDS: set multicast transfer speed policy to separate clients into slow/medium/fast streams (Server Properties > Multicast) so one slow NIC does not throttle everyone.
- Set a minimum client count for scheduled casts.

## Troubleshooting
| Symptom | Cause |
|---|---|
| Clients stuck "Waiting for server" | IGMP querier missing, port range blocked |
| Very slow for all | One slow client; enable stream splitting |
| Network-wide slowdown during imaging | No IGMP snooping, flooding |
| Falls back to unicast | Package not multicast-enabled or DP multicast off |

## Verify
Monitor the transmission in the WDS console (clients connected, speed); switch shows IGMP group memberships only on ports with clients.
