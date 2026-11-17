---
id: computing-software.networking-hardware-and-wireless.arista-eos.cloudvision-telemetry
name: cloudvision-telemetry
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, telemetry, streaming-telemetry, state-streaming, cv-events]
level: practitioner
status: draft
description: "Use CloudVision's state streaming for device metrics, events and alerting."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CloudVision streaming telemetry and events
Goal: use streaming state instead of polling.

```
# TerminAttr streams state; view in CloudVision
Telemetry > Devices > select device > Interfaces / BGP / MAC
Events > filter severity > Create event rule
```

- Streaming gives second-level data without SNMP polling; events cover interface errors, BGP changes, config drift.
- Dashboards can alert via email, webhook, or ServiceNow integrations.
- Time machine view: browse the network state at a past time (retention depends on the license/tier: confirm).

Gotcha: excluded Sysdb paths in `-smashexcludes` reduce visible data; do not remove the defaults without reading the docs. Without correct time on devices events are mislabelled.

Operational tip: create alerts for the few conditions that matter (BGP down, MLAG inactive, optic power, CRC errors) rather than all events, and route them to a team channel with runbooks attached.

## Verify
- A deliberate link flap appears in Events with the correct timestamp and device.
