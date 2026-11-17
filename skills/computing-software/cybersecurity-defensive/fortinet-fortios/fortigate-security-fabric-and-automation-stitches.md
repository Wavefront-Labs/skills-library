---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-security-fabric-and-automation-stitches
name: fortigate-security-fabric-and-automation-stitches
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [security-fabric, fortios, csf, fabric-connector, automation-stitch, upstream-fortigate, fabric-root]
level: practitioner
status: draft
description: "Join a Fortinet Security Fabric, authorize downstream devices and build automation stitches that react to events."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: a topology-aware fabric with shared objects and event-driven responses.

Root:
```
config system csf
    set status enable
    set group-name "corp-fabric"
    set group-password <PASSWORD>
    set configuration-sync default
    set fabric-object-unification default
end
```
Downstream:
```
config system csf
    set status enable
    set upstream-ip 192.0.2.1
    set upstream-port 8013
    set group-name "corp-fabric"
end
```
Authorize the downstream from the root (Security Fabric > Fabric Connectors). Automation stitch:
```
config system automation-trigger
    edit "high-ips"
        set event-type ips-logs
        set ips-severity high critical
    next
end
config system automation-action
    edit "email-soc"
        set action-type email
        set email-to "soc@example.com"
        set email-subject "IPS high alert"
    next
end
config system automation-stitch
    edit "ips-to-email"
        set trigger "high-ips"
        set action "email-soc"
    next
end
```
Gotchas
- Fabric needs TCP 8013 between members and consistent time.
- `configuration-sync local` keeps local settings; `default` pulls from the root for some objects.
- Stitches can create action storms; add a `delay` and limit frequency.

## Verify
```
diagnose sys csf downstream
diagnose sys csf upstream
diagnose test application csfd 1
```
(Confirm exact commands.) The topology view shows the downstream connected.
