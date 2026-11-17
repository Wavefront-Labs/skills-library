---
id: computing-software.networking-hardware-and-wireless.arista-eos.logging-syslog
name: logging-syslog
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, logging, syslog, logging-host, severity]
level: practitioner
status: draft
description: "Send EOS logs to remote syslog, set severity and source interface, and read local log buffers."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Syslog and logging
Goal: reliable logs both locally and remote.

```
logging buffered 64000 informational
logging host 192.0.2.60 514 protocol udp
logging vrf MGMT host 192.0.2.60
logging source-interface Management1
logging trap informational
logging format timestamp traditional year
```

```
show logging
show logging last 30 minutes
show logging | include LINEPROTO
```

- Severity: emergencies(0) through debugging(7).
- Timestamps with year and timezone help correlation: `logging format timestamp high-resolution` (confirm).
- Use `logging event link-status global` to control interface up/down messages.

Gotcha: logging to a host reachable only via the management VRF requires `logging vrf MGMT host`; plain `logging host` uses the default VRF and silently fails.

Operational tip: forward logs to at least two collectors, keep timestamps in UTC, and alert on repeated `BGP-3-NOTIFICATION`, `MLAG` and `STP` messages instead of reading logs by hand. Keep an eye on log volume: a flapping link or debug logging can fill the buffer and hide the original event, so size the buffer and rate-limit noisy facilities.

## Verify
- Flap a test port and see `LINEPROTO` messages locally and at the collector.
