---
id: computing-software.systems-network-administration.cisco-networking.sampled-netflow
name: sampled-netflow
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, netflow, sampled-netflow, flow-sampler, random-sampling, flow-monitor, psamp]
level: practitioner
status: docs-checked
description: "Understand sampled Flexible NetFlow: what a flow sampler does, its accuracy trade-off, the sampler ID record field, and PSAMP random n-out-of-N sampling."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/fnetflow/configuration/xe-16/fnf-xe-16-book/fnf-fnetflow.html
  - https://www.rfc-editor.org/rfc/rfc5476
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sampled NetFlow

## What the Cisco guide says
- Flow samplers are created as separate components in a router's configuration. They reduce the load on the device
  running Flexible NetFlow by limiting the number of packets selected for analysis.
- Sampling exchanges monitoring accuracy for router performance: fewer packets analysed means a corresponding
  reduction in the accuracy of the information in the flow monitor cache.
- A sampler is combined with a flow monitor when applied to an interface with the `ip flow monitor` command.
- Original NetFlow's Random Packet Sampled NetFlow is available in Flexible NetFlow through sampling.
- Predefined records include a Flow Sampler ID field: the ID number of the flow sampler, if sampling is enabled.
  Carrying it lets the collector know a flow came from a sampled monitor.

## Random n-out-of-N sampling (RFC 5476)
In PSAMP random n-out-of-N sampling, n packets are selected out of a parent population of N packets. The required
information elements are `samplingSize` (packets selected) and `samplingPopulation` (packets in the population); the
RFC's example is a 1-out-of-10 selector. The selector is reported to the collector in an IPFIX options template
record, so the collector can learn the sampling parameters.

## Practice
- Counts from a sampled monitor represent only the selected packets. A collector must scale by the sampling ratio
  (N divided by n) to estimate totals; confirm how your collector learns or is told the rate.
- Because accuracy falls with fewer analysed packets, small or short flows are the least reliably seen.
- Compare scaled collector totals against interface counters (for example SNMP octet counters) to validate the rate.
- The sampler configuration commands and recommended rates are platform- and release-specific; take them from the
  command reference for your release.

## Checked
Checked 2026-11-08 against the Cisco Flexible NetFlow configuration guide (Flow Samplers section, feature comparison
table, record field tables) and RFC 5476 section 6.5.2.3. Removed: `sampler`/`mode random` and `option sampler-table`
commands, 1:100 and 1:1000 rate guidance, CPU monitoring commands, and DNS-flow example, because the Cisco sampling
page returned 404 and the sources do not state them.
Method: documentation only; no commands were run.
