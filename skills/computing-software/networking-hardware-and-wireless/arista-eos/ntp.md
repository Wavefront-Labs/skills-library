---
id: computing-software.networking-hardware-and-wireless.arista-eos.ntp
name: ntp
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, ntp, time-sync, clock-timezone, ntp-server]
level: practitioner
status: draft
description: "Configure NTP on EOS with servers, VRF, source interface and verify synchronisation."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NTP
Goal: accurate time across the fabric.

```
clock timezone UTC
ntp server vrf MGMT 192.0.2.10 prefer iburst
ntp server vrf MGMT 192.0.2.11 iburst
ntp local-interface vrf MGMT Management1
```

```
show ntp status
show ntp associations
show clock
```

- `iburst` speeds the initial sync.
- Place NTP in the VRF that has reachability to the servers.
- Certificates (eAPI HTTPS, CloudVision) depend on correct time.

Gotcha: Using `ntp server` without `vrf MGMT` when the servers sit behind the management interface leaves `show ntp status` as unsynchronised, and logs and TLS suffer.

Operational tip: use at least three sources, and watch `show ntp associations` offset values. A drift of a few seconds already breaks certificate checks and makes incident timelines unreliable. After fixing time, restart dependent sessions such as TLS to CloudVision and check that log timestamps now agree with the collector.

## Verify
- `show ntp status` reports `synchronised to NTP server` with stratum and a low offset.
