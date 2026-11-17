---
id: computing-software.cloud-infrastructure-engineering.google-cloud.troubleshooting-cloud-nat-port-exhaustion
name: troubleshooting-cloud-nat-port-exhaustion
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-nat, nat-port-exhaustion, nat-allocation-failed, dropped-sent-packets, endpoint-independent-mapping, dynamic-port-allocation]
level: practitioner
status: docs-checked
description: "Diagnose Cloud NAT dropped connections: OUT_OF_RESOURCES and allocation-failed metrics, port math per VM, dynamic port allocation, EIM, timeouts and adding NAT IPs."
sources: ["https://cloud.google.com/nat/docs/troubleshooting", "https://cloud.google.com/nat/docs/ports-and-addresses", "https://cloud.google.com/nat/docs/monitoring", "https://cloud.google.com/sdk/gcloud/reference/compute/routers/nats/update"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting Cloud NAT port exhaustion

Symptom: intermittent outbound timeouts from VMs/GKE pods without external IPs, especially to
one popular destination (an API, a registry).

## Confirm
Metrics:
- `compute.googleapis.com/nat/dropped_sent_packets_count` per VM with reason `OUT_OF_RESOURCES` = out of NAT IPs or ports (the other reason is `ENDPOINT_INDEPENDENCE_CONFLICT`).
- `router.googleapis.com/nat/nat_allocation_failed` = true when NAT IPs could not be allocated to a VM in the gateway.
- `compute.googleapis.com/nat/port_usage` (maximum connections from a VM to one internet endpoint) vs `nat/allocated_ports`.
Logs (enable `--enable-logging --log-filter=ERRORS_ONLY`; TCP and UDP only, throttled under heavy egress):
```
resource.type="nat_gateway"
```

## Port math
Each NAT IP offers 64,512 TCP and 64,512 UDP source ports. With static allocation, each VM gets `--min-ports-per-vm` (default 64).
A NAT 5-tuple (NAT IP, source port, destination 3-tuple) cannot be reused within the TCP TIME_WAIT timeout, so many connections to the
**same destination IP:port** each need a distinct source port; with **endpoint-independent mapping (EIM)** enabled the number of
simultaneous connections to a destination can be reduced. VMs supported = (IPs x 64,512) / ports-per-VM.

## Fixes
```bash
gcloud compute routers nats update egress-nat --router=cr-ew2 --region=europe-west2 \
  --enable-dynamic-port-allocation --min-ports-per-vm=256 --max-ports-per-vm=8192 \
  --no-enable-endpoint-independent-mapping \
  --tcp-time-wait-timeout=30s --tcp-established-idle-timeout=600s
# more IPs (manual) or let auto-allocation add them
gcloud compute routers nats update egress-nat --router=cr-ew2 --region=europe-west2 \
  --nat-external-ip-pool=nat-1,nat-2,nat-3
```
- Dynamic port allocation detects a VM nearing exhaustion and doubles its ports, up to max; packets can drop while ports are being added, so ramp connections up gradually.
- Shorter TIME_WAIT timeout frees ports sooner (default is 30 s or 120 s depending on when the gateway was created).
- App side: connection pooling and keep-alive; avoid opening a new TCP connection per request.

## Gotchas
- DPA and EIM cannot both be enabled (EIM needs static allocation).
- Increasing min ports reduces how many VMs an IP pool supports; with automatic IP allocation the gateway acquires more addresses for you, with manual assignment you must add them.
- Ports are allocated per VM or GKE node.

## Verify
- [ ] `OUT_OF_RESOURCES` drops at zero under peak; `nat_allocation_failed` false for all VMs.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Found wrong: metrics were all given the router.googleapis.com prefix (only nat_allocation_failed is a router metric; the others are compute.googleapis.com), TIME_WAIT default was stated as 120 s only, and the log filter jsonPayload.allocation_status is not documented.
- Confirmed (troubleshooting page): OUT_OF_RESOURCES reason, TIME_WAIT 5-tuple reuse delay, DPA doubling ports and transient drops, logging throttled under heavy egress.
- Confirmed (ports and addresses page): 64,512 ports per IP, EIM requires static allocation and cannot combine with DPA; automatic assignment acquires more IPs when min ports increases.
- Confirmed (gcloud reference, nats update): --enable-dynamic-port-allocation, --min-ports-per-vm, --max-ports-per-vm, --no-enable-endpoint-independent-mapping, --tcp-time-wait-timeout, --tcp-established-idle-timeout, --nat-external-ip-pool.
- Removed: the Private Google Access 'does not use NAT ports' and 'GKE count per node, not per pod' statements (not found in the pages read).

Method: documentation only; no commands were run.
