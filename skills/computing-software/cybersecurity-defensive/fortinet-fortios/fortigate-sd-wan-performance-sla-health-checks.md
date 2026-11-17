---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-sd-wan-performance-sla-health-checks
name: fortigate-sd-wan-performance-sla-health-checks
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [performance-sla, fortios, sdwan-health-check, latency-jitter-packet-loss, sla-target, probe]
level: practitioner
status: draft
description: "Configure FortiGate SD-WAN performance SLA health checks with latency, jitter and loss thresholds that drive rule steering."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: measure link quality and let rules pick links that meet an SLA.

```
config system sdwan
    config health-check
        edit "hc1"
            set server "192.0.2.1" "198.51.100.1"
            set protocol ping
            set interval 500
            set failtimes 5
            set recoverytime 5
            set members 1 2
            config sla
                edit 1
                    set latency-threshold 150
                    set jitter-threshold 30
                    set packetloss-threshold 2
                next
            end
        next
    end
    config service
        edit 2
            set name "teams-sla"
            set mode sla
            config sla
                edit "hc1"
                    set id 1
                next
            end
            set priority-members 1 2
        next
    end
end
```
Use a probe target that represents the path (a cloud service or provider IP), not the local gateway. Choose `protocol http` or `dns` when ICMP is filtered.

Gotchas
- Aggressive intervals on many branches create load and noisy logs; start at 500-1000 ms.
- `failtimes` too low causes flapping; test link recovery.
- SLA ID in service must exist in the health check (`set id 1`).

## Verify
```
diagnose sys sdwan health-check
diagnose sys sdwan sla-log hc1 1
```
The output shows each member alive or dead with latency, jitter and loss figures that match the thresholds.
