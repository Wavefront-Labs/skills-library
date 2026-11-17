---
id: computing-software.networking-hardware-and-wireless.network-device-administration.nda-streaming-telemetry-gnmi-netconf
name: nda-streaming-telemetry-gnmi-netconf
category: computing-software
field: networking-hardware-and-wireless
product: network-device-administration
tags: [gnmi-telemetry, netconf-yang, model-driven-programmability]
level: advanced
status: docs-checked
description: "Use NETCONF and gNMI with YANG models for structured config and streaming telemetry instead of CLI scraping."
sources:
  - https://www.rfc-editor.org/rfc/rfc6241
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Model-driven management

- NETCONF (RFC 6241) uses an XML-based encoding for configuration data and protocol messages, and can run over secure transports such as SSH or TLS; connections must be authenticated.
- NETCONF defines a candidate configuration datastore that can be manipulated without impacting the device's current configuration, and provides primitives on which transaction-oriented operations can be built.
- Confirm the supported YANG models for your release and test against a lab device; keep CLI access and logs, and pick one source of truth because mixed methods fight over config ownership.

## Verify
- [ ] A subscription delivers interface counters at the configured interval and matches CLI counters.
## Checked
2026-11-02. Confirmed against RFC 6241 (XML encoding, SSH/TLS transports, authentication requirement, candidate datastore, transaction primitives). Removed: the port 830 value, gNMI/gRPC/TLS statements, streaming-telemetry-vs-SNMP claims, `ncclient`/`gnmic` tooling (gNMI and OpenConfig specifications were not read).
Method: documentation only; no commands were run.
