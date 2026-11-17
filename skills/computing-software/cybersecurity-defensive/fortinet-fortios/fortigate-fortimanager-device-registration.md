---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-fortimanager-device-registration
name: fortigate-fortimanager-device-registration
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [fortimanager, fortios, fgfm, central-management, adom, device-manager, fmg]
level: practitioner
status: draft
description: "Register FortiGate with FortiManager using FGFM, authorize it into an ADOM and check the management connection."
sources: ["https://docs.fortinet.com/document/fortimanager/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: a FortiGate that is centrally managed and visible in Device Manager.

On the FortiGate:
```
config system central-management
    set type fortimanager
    set fmg "192.0.2.70"
    set mode normal
end
```
Then on the FortiManager: Device Manager > Add Device (or authorize from the Unauthorized list), select the ADOM, optionally import existing policy and objects, and install.

Troubleshoot the FGFM tunnel (TCP 541):
```
get system central-management
diagnose debug application fgfmsd -1
diagnose debug enable
diagnose fdsm contract-controller-update
```
Disable debug afterwards. On the FortiManager: `diagnose dvm device list` shows connection state.

Gotchas
- ADOM version must match the managed FortiOS major version; new firmware needs the FortiManager at a compatible release.
- Without NTP, certificates fail and the tunnel refuses.
- If the FortiGate is behind NAT, set `fmg-source-ip` or use the FortiManager's `nat` device option.
- Importing policy first avoids overwriting local settings on the first install.

## Verify
FortiManager Device Manager shows the device Connection Up and configuration status Synchronised; `get system central-management` reports `connected`.
