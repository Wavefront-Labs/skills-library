---
id: computing-software.networking-hardware-and-wireless.arista-eos.event-handler
name: event-handler
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, event-handler, eos-automation, on-intf, on-boot]
level: practitioner
status: draft
description: "Use EOS event-handler to run commands or scripts on triggers such as interface state change or schedule."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Event handlers
Goal: local automation without external tooling.

```
event-handler LINKDOWN
   trigger on-intf Ethernet1 operstatus
   action bash logger "Ethernet1 operstatus changed"
   delay 10
   asynchronous
event-handler BACKUP
   trigger on-boot
   action bash FastCli -p15 -c "copy running-config flash:boot.cfg"
```

```
show event-handler
show event-handler LINKDOWN
```

- Triggers: `on-boot`, `on-intf`, `on-startup-config`, `on-logging`, `on-maintenance`, `on-counters`.
- `action bash` runs in the Linux shell; use `FastCli -p15 -c` for CLI.
- `delay`, `repeat interval` and `asynchronous` shape execution.

Gotcha: handlers run as root-equivalent; a looping action (config change triggering itself) can cause a storm. Use `delay` and guard conditions.

Operational tip: log what the handler did via `logger` so the audit trail shows automated actions, and test with `trigger` in a lab before enabling on production devices. Review handlers during upgrades: syntax of `action` lines and FastCli behaviour can change between EOS releases, so confirm after each upgrade.

## Verify
- `show event-handler LINKDOWN` increments the `Total Action Count` after you flap the interface.
