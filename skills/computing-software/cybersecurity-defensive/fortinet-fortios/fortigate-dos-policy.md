---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-dos-policy
name: fortigate-dos-policy
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [dos-policy, fortios, anomaly, syn-flood, tcp-syn-flood, rate-limit, ddos-protection]
level: practitioner
status: draft
description: "Protect FortiGate-facing networks with a DoS policy using anomaly thresholds for SYN, UDP and ICMP floods."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: drop volumetric attacks before the policy lookup path is overwhelmed.

```
config firewall DoS-policy
    edit 1
        set name "wan-dos"
        set interface "port1"
        set srcaddr "all"
        set dstaddr "all"
        set service "ALL"
        config anomaly
            edit "tcp_syn_flood"
                set status enable
                set log enable
                set action block
                set threshold 2000
            next
            edit "udp_flood"
                set status enable
                set log enable
                set action block
                set threshold 2000
            next
            edit "icmp_flood"
                set status enable
                set action block
                set threshold 250
            next
        end
    next
end
```
DoS policies are evaluated at the earliest stage on the ingress interface. Thresholds are packets per second per destination (for floods), so size them from baselined peaks, not defaults.

Gotchas
- Set action `monitor` first and review logs; blocking with a low threshold takes down legitimate bursts.
- NP-accelerated units can offload DoS protection (`config system np6`/`npu` settings; confirm).
- DoS policy does not replace ISP/Cloud DDoS scrubbing.

## Verify
```
diagnose firewall dos-policy status
get firewall dos-policy
```
(Confirm exact command for your release.) Anomaly logs list the type, source and action.
