---
id: computing-software.systems-network-administration.network-design.95th-percentile-utilisation-and-billing
name: 95th-percentile-utilisation-and-billing
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, monitoring, 95th-percentile, burstable-billing, utilisation, snmp-counters]
level: practitioner
status: verified
description: "Calculate and use 95th percentile utilisation: the burstable billing method, computing it from 5-minute samples, per-direction vs max, and capacity planning use."
sources:
  - https://en.wikipedia.org/wiki/Burstable_billing
  - https://www.cisco.com/c/en/us/support/docs/ip/simple-network-management-protocol-snmp/8141-calculate-bandwidth-snmp.html
  - https://docs.librenms.org/Extensions/Billing-Module/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 95th percentile utilisation and billing

## Method (burstable billing)
1. Sample interface rate every **5 minutes** for the billing month (8640 samples for 30 days).
2. Sort samples high to low, discard the top **5 %** (432 samples = 36 hours of bursting free).
3. The highest remaining sample is the 95th percentile; bill on it (often the greater of in or out
   95th, or the 95th of max(in, out) per sample; check the contract).

## Computing it
SNMP 64-bit counters (`ifHCInOctets`, `ifHCOutOctets`): rate = delta octets x 8 / delta seconds.
Missing samples and counter wraps distort results; use HC counters and consistent polling.
```
# Prometheus (5m samples over 30d)
quantile_over_time(0.95, (rate(ifHCOutOctets{ifName="xe-0/0/0"}[5m]) * 8)[30d:5m])
```
LibreNMS has a billing module; its docs say it uses the higher of the input and output 95th by
default, with an "Aggregate" option that sums in and out per bill. Most carriers publish their own
figures: compare monthly and dispute discrepancies with your data. Note the PromQL query above
interpolates between samples (`quantile_over_time`) whereas billing discards the top 5 % and takes
the highest remaining sample; on 8,640 synthetic samples the two differed by 0.02 (230.35 vs 230.37),
negligible but not identical. The query parses (checked with a PromQL parser); metric and label names
depend on your exporter.

## Gotchas
- Averaging samples to 1-hour before computing hides bursts and lowers the number; carriers typically use
  5-minute samples.
- Commit vs burst: you pay the commit rate even if 95th is lower; above it costs per Mbps.
- A daily backup that runs > 36 h per month at line rate will set your bill.
- Aggregate billing across several ports: sum per sample first, then compute the 95th.

## Planning use
Monthly 95th percentile is the standard input for capacity planning; compare to link capacity
(upgrade at ~70 %).

## Verify
- [ ] Your computed monthly 95th matches the carrier invoice within a few percent.
