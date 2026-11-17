---
id: computing-software.cloud-infrastructure-engineering.google-cloud.vm-network-throughput-and-drop-metrics
name: vm-network-throughput-and-drop-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, network-observability, vm-network-metrics, egress-bandwidth-cap, packet-drops, tier-1-networking, gvnic]
level: practitioner
status: docs-checked
description: "Read Compute Engine network metrics to diagnose throughput limits and drops: sent/received bytes, VM egress caps, Tier_1 networking, gVNIC, and guest-side counters."
sources: ["https://docs.cloud.google.com/compute/docs/networking/configure-vm-with-high-bandwidth-configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM network throughput and drop metrics

## Metrics
Use the Compute Engine network metrics in Cloud Monitoring (sent and received bytes and packets per VM; look up the exact metric
names in the Google Cloud metrics list) and the Ops Agent interface metrics for guest-side errors. Small packets hit
packets-per-second limits before bandwidth, so plot both bytes and packets.

## Know the caps
- Default per-VM egress bandwidth limits range from 10 Gbps to 400 Gbps, depending on machine type and size. Tier_1
  networking raises the maximum egress limit to between 50 Gbps and 200 Gbps, depending on machine type and size.
- Tier_1 is supported on N2, N2D, C2, C2D, C3, C3D, C4, C4A, C4D, M3 and Z3 machine types with the minimum vCPU count. For VMs it
  requires the gVNIC driver and a gVNIC-compatible OS or custom image; third generation and later VMs need gVNIC driver 1.4.2 or later
  for the highest bandwidth.
- Limits differ for internal and external IP traffic: the per-series tables on the Tier_1 page and the Network bandwidth page give the
  figures (for example, a 2-vCPU C4 VM has 10 Gbps internal and 7 Gbps external).
- Tier_1 SKUs are excluded from committed use discounts; see the vendor's pricing page for cost.

## High bandwidth config
```bash
gcloud compute instances create big-net --machine-type=c3-standard-88 --zone=<Z> \
  --network-interface=nic-type=GVNIC,subnet=prod-ew2 --network-performance-configs=total-egress-bandwidth-tier=TIER_1
```
The image must support gVNIC.

## Diagnosing "slow network"
1. Plot sent bytes in Gbps: flat-topped at a round number suggests a cap; compare with the table for your series.
2. Check packets per second: high pps with low Gbps means a small-packet workload; tune batching.
3. In the guest, check interface drop and retransmit counters (`ethtool -S`, `nstat`, `sar -n DEV`).
4. Use the Performance Dashboard for zone-to-zone loss and latency, and Connectivity Tests for configuration.
5. Run `iperf3` with parallel streams between VMs in the same zone to establish a baseline.

## Verify
- [ ] The iperf3 baseline is in line with the documented limit for the machine series; app throughput compared against it.

## Checked
2026-10-28. Confirmed against the Compute Engine "Configure per VM Tier_1 networking performance" page: default and Tier_1 bandwidth ranges,
supported series, gVNIC requirement and driver version, CUD exclusion, the 2-vCPU C4 example. Command flags verified against the gcloud
reference. Removed: metric names (metrics list page not readable in this review), 2 Gbps per vCPU rule, single-flow and ingress claims,
sampling-interval and disk-throughput notes.
Method: documentation only; no commands were run.
