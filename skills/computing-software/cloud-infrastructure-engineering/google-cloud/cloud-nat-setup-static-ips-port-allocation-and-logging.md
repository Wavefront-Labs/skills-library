---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-nat-setup-static-ips-port-allocation-and-logging
name: cloud-nat-setup-static-ips-port-allocation-and-logging
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-nat, cloud-nat-setup, gcloud-compute-routers-nats, nat-static-ips, manual-nat-ips, nat-port-allocation, dynamic-port-allocation, nat-logging, nat-monitoring]
level: practitioner
status: docs-checked
description: "Build Cloud NAT with gcloud, use manual static IPs for allowlisting with safe draining, size port allocation (static vs dynamic), and log and monitor NAT drops."
sources: ["https://cloud.google.com/nat/docs/set-up-manage-network-address-translation", "https://cloud.google.com/nat/docs/ports-and-addresses", "https://cloud.google.com/nat/docs/monitoring", "https://cloud.google.com/sdk/gcloud/reference/compute/routers/nats/create", "https://cloud.google.com/sdk/gcloud/reference/compute/routers/nats/update"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud NAT: setup, static IPs, ports and logging

## 1. Create
```bash
gcloud compute routers create nat-rtr --network=prod --region=europe-west2
gcloud compute addresses create nat-ip-1 nat-ip-2 --region=europe-west2
gcloud compute routers nats create prod-nat --router=nat-rtr --region=europe-west2 \
  --nat-all-subnet-ip-ranges \
  --nat-external-ip-pool=nat-ip-1,nat-ip-2 \
  --enable-dynamic-port-allocation --min-ports-per-vm=128 --max-ports-per-vm=4096 \
  --enable-logging --log-filter=ERRORS_ONLY
```
`--auto-allocate-nat-external-ips` is simpler; with manual assignment you reserve the regional external addresses yourself, so use
manual IPs whenever partners allowlist you. Restrict to specific subnets with `--nat-custom-subnet-ip-ranges=app-subnet,gke-subnet:pods`.

## 2. Change IPs without breaking connections
```bash
gcloud compute routers nats update prod-nat --router=nat-rtr --region=europe-west2 \
  --nat-external-ip-pool=nat-ip-2,nat-ip-3 --nat-external-drain-ip-pool=nat-ip-1
```
Draining IPs serve existing connections only; remove from the drain pool after connections age out.

## 3. Port maths
Each NAT IP offers 64,512 TCP and 64,512 UDP source ports (ports 0-1,023 are not used). VMs per IP = 64,512 / min-ports-per-vm (static allocation).
A source port can be reused for connections to different destination 3-tuples (IP, port, protocol), so exhaustion shows up first when many connections go to one destination.
- Static allocation: predictable, wasteful for uneven load.
- **Dynamic port allocation (DPA)**: disabled by default; starts at `--min-ports-per-vm` (default 32 with DPA, 64 without) and grows toward `--max-ports-per-vm` (default 65536; a power of 2) on demand. Suits uneven fleets.
- Endpoint-independent mapping (`--enable-endpoint-independent-mapping`, off by default) cannot be combined with DPA; leave it off unless a protocol needs it.
- Tune timeouts (`--tcp-established-idle-timeout`, `--tcp-time-wait-timeout`) for high-churn clients; the default TIME_WAIT is 30 or 120 seconds depending on when the gateway was created.

## 4. Log and monitor
- Logs (`resource.type="nat_gateway"`, TCP and UDP only): `--log-filter` is `ALL` (default), `ERRORS_ONLY` (a packet dropped because no port was available) or `TRANSLATIONS_ONLY` (connections created).
- VM metrics (prefix `compute.googleapis.com/`): `nat/dropped_sent_packets_count` (reason `OUT_OF_RESOURCES` or `ENDPOINT_INDEPENDENCE_CONFLICT`), `nat/allocated_ports`, `nat/port_usage`.
- Gateway metric (prefix `router.googleapis.com/`): `nat/nat_allocation_failed`.
Alert on `OUT_OF_RESOURCES` drops and on `nat_allocation_failed`.

## Gotchas
- A Cloud NAT gateway is regional and hosted by a Cloud Router; each region needs its own.
- With manual assignment, if the gateway runs out of NAT IPs it drops packets; the drops are logged when error logging is on.

## Verify
- [ ] From a private VM, an external IP echo service returns one of the manual NAT IPs.
- [ ] A load test to a single endpoint shows no `OUT_OF_RESOURCES` drops at peak connections.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Found wrong: all metrics were given the router.googleapis.com prefix; the monitoring page puts dropped_sent_packets_count, allocated_ports and port_usage under compute.googleapis.com/ and only nat/nat_allocation_failed under router.googleapis.com/. The TIME_WAIT default is 30 or 120 seconds by gateway creation date, not a single value.
- Confirmed (gcloud reference, nats create/update): --enable-dynamic-port-allocation, --min-ports-per-vm and --max-ports-per-vm defaults and power-of-2 rule, --enable-endpoint-independent-mapping, --log-filter values, --nat-custom-subnet-ip-ranges form, --nat-external-drain-ip-pool on update, TCP timeout flags.
- Confirmed (ports and addresses page): 64,512 TCP and 64,512 UDP source ports per NAT IP; EIM and DPA cannot be combined; DPA is for varying egress.
- Confirmed (monitoring page): log filter semantics, TCP and UDP only logging, reason label values.
- Removed: the 'VMs with external IPs bypass NAT' and 'no egress at all' statements and the per-VM same-destination connection claim (not stated on the pages read).

Method: documentation only; no commands were run.
