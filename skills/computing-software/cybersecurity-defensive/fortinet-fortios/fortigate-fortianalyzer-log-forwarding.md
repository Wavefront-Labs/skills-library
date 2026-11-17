---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-fortianalyzer-log-forwarding
name: fortigate-fortianalyzer-log-forwarding
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [fortianalyzer, fortios, faz, log-forwarding, reliable-logging, upload-option, log-device-authorization]
level: practitioner
status: draft
description: "Send FortiGate logs to FortiAnalyzer with reliable transport and authorize the device on the FortiAnalyzer side."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: central log storage with reports and event handlers.

```
config log fortianalyzer setting
    set status enable
    set server "192.0.2.60"
    set serial "FL-EXAMPLE0001"
    set upload-option realtime
    set reliable enable
    set enc-algorithm high
    set ssl-min-proto-version default
end
execute log fortianalyzer test-connectivity
```
Then authorize the FortiGate in FortiAnalyzer (Device Manager > Unauthorized Devices) and assign it to an ADOM. Reliable mode uses TCP/TLS and queues logs while the connection is down.

Gotchas
- Unauthorized devices have their logs dropped; check the FortiAnalyzer side after enabling.
- The FortiAnalyzer needs the same time source and, for Security Fabric, the same fabric root.
- FortiGate source IP/interface for logging uses `set interface-select-method specify` when the default route is not right.
- ADOM/version mismatch shows a log "unsupported" message.

## Verify
`execute log fortianalyzer test-connectivity` reports Connected and registered; in FortiAnalyzer Log View shows new entries; `diagnose test application miglogd 6` shows the log queue (confirm).
