---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-traffic-shapers-and-shaping-policy
name: fortigate-traffic-shapers-and-shaping-policy
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [traffic-shaper, fortios, shaping-policy, per-ip-shaper, guaranteed-bandwidth, qos-dscp, bandwidth-limit]
level: practitioner
status: draft
description: "Create FortiGate shared and per-IP traffic shapers and shaping policies to guarantee voice and cap bulk traffic."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: control bandwidth by service, application or user.

```
config firewall shaper traffic-shaper
    edit "voice-guaranteed"
        set guaranteed-bandwidth 2000
        set maximum-bandwidth 10000
        set priority high
        set per-policy disable
    next
    edit "bulk-limit"
        set maximum-bandwidth 20000
        set priority low
    next
end
config firewall shaper per-ip-shaper
    edit "per-user-5m"
        set max-bandwidth 5000
        set max-concurrent-session 500
    next
end
config firewall shaping-policy
    edit 1
        set name "voice-shape"
        set service "SIP"
        set srcintf "port2"
        set dstintf "port1"
        set traffic-shaper "voice-guaranteed"
        set traffic-shaper-reverse "voice-guaranteed"
        set per-ip-shaper "per-user-5m"
    next
end
config system interface
    edit "port1"
        set outbandwidth 100000
    next
end
```
Bandwidth units are kbps. Shaping policies match on service, app, URL category, user and DSCP.

Gotchas
- Shapers only matter when the interface bandwidth is set (`outbandwidth`) and congestion occurs.
- NP offload may bypass shaping; configure and test per model.
- Shapers apply to forward traffic; local-out is not shaped.

## Verify
```
diagnose firewall shaper traffic-shaper list
diagnose firewall shaper per-ip-shaper list
```
Counters show bytes and drops per shaper while a test transfer is running.
