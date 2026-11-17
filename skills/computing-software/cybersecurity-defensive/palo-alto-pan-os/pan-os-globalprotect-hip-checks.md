---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-globalprotect-hip-checks
name: pan-os-globalprotect-hip-checks
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [host-information-profile, pan-os, hip-object, hip-profile, endpoint-posture, globalprotect, compliance-check]
level: practitioner
status: draft
description: "Enforce GlobalProtect endpoint posture with HIP objects and profiles that drive security policy decisions on PAN-OS."
sources: ["https://docs.paloaltonetworks.com/globalprotect/11-1/globalprotect-admin/host-information"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: allow access only from managed, patched, encrypted devices.

Build
- HIP objects (Objects > GlobalProtect > HIP Objects): conditions on patch management, antivirus, disk encryption, firewall, anti-spyware, custom registry/plist keys, certificate, OS version.
- HIP profiles: boolean combinations of HIP objects, for example `has-encryption AND has-av AND NOT jailbroken`.
- Use the profile as a source HIP profile in security policy:

```
configure
set rulebase security rules allow-corp-apps from vpn-users to internal source any destination any source-hip [ hip-compliant ] application [ ssl web-browsing ] action allow
set rulebase security rules quarantine-vlan from vpn-users to internal source-hip [ hip-noncompliant ] application any action allow
commit
```

Agent-side: HIP data collection is controlled by the agent config HIP collection settings and the gateway must have a HIP notification message for the user.

Gotchas
- The HIP check is evaluated on connect and refreshed periodically (default one hour, confirm); posture changes may take time to reflect.
- HIP report content depends on the licence (GlobalProtect subscription) for full HIP checks.
- Logging matches in HIP Match log requires log forwarding for HIP.

## Verify
```
show global-protect-gateway current-user
show log hipmatch direction equal backward
```
Log shows which HIP profiles matched the user, and a noncompliant test host hits the restricted rule.
