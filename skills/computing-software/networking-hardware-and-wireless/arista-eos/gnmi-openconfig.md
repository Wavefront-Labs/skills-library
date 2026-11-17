---
id: computing-software.networking-hardware-and-wireless.arista-eos.gnmi-openconfig
name: gnmi-openconfig
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, gnmi, openconfig, gnmic, streaming]
level: practitioner
status: draft
description: "Enable the EOS gNMI server and query or subscribe to OpenConfig paths with gnmic."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# gNMI and OpenConfig on EOS
Goal: model-driven telemetry and config.

```
management api gnmi
   transport grpc default
      vrf MGMT
      ssl profile GNMI
   provider eos-native
```

```
gnmic -a 192.0.2.1:6030 -u automation -p <password> --skip-verify get --path /interfaces/interface[name=Ethernet1]/state/counters
gnmic -a 192.0.2.1:6030 -u automation -p <password> --skip-verify subscribe --path /interfaces/interface/state/counters --sample-interval 10s
```

- `provider eos-native` exposes EOS native paths in addition to OpenConfig (confirm availability on your release).
- Use TLS certificates in production; `--skip-verify` is for labs.
- `show management api gnmi` shows status.

Gotcha: forgetting `vrf MGMT` leaves the server listening in the default VRF only. Path support is partial and release dependent: confirm with `capabilities`.

Operational tip: use a gNMI collector such as gnmic into Prometheus or InfluxDB, start with interface counters on a 10-30 second sample, and verify supported paths via `capabilities` after each EOS upgrade. Secure the gRPC listener with TLS profiles and an ACL, and give the telemetry user a read-only role.

## Verify
- `gnmic capabilities` returns supported models; `get` returns counters.
