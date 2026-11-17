---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-ips-sensors
name: fortigate-ips-sensors
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [ips-sensor, fortios, ips, signatures, rate-based-signature, fail-open, ips-engine]
level: practitioner
status: draft
description: "Build FortiGate IPS sensors by severity and target, tune rate-based signatures, and manage fail-open behaviour."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: block high-risk exploits with controlled false-positive handling.

```
config ips sensor
    edit "ips-std"
        config entries
            edit 1
                set severity high critical
                set location server
                set action block
                set status enable
                set log-packet enable
            next
            edit 2
                set severity medium
                set action pass
                set log enable
            next
        end
    next
end
config firewall policy
    edit 20
        set ips-sensor "ips-std"
    next
end
```
Tune by exempting a specific signature via `config exempt-ip` or `config override` (set `action pass` for a single rule id) rather than lowering severity globally. Use `set location server` on inbound policies and `client` on outbound policies.

Gotchas
- IPS engine failure behaviour is set globally (`config ips global; set fail-open enable`) so traffic keeps flowing if the engine crashes; confirm your compliance requirement before enabling.
- Packet logging fills disk; enable it on specific entries only.
- Signature updates add new blocks: review IPS logs after each update.

## Verify
```
diagnose ips anomaly list
diagnose test application ipsmonitor 1
get ips rule status
```
(Confirm exact commands.) The IPS log shows attacks with signature id and action.
