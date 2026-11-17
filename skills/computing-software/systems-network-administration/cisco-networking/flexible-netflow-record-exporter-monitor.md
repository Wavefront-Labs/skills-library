---
id: computing-software.systems-network-administration.cisco-networking.flexible-netflow-record-exporter-monitor
name: flexible-netflow-record-exporter-monitor
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, netflow, flexible-netflow, flow-record, flow-exporter, flow-monitor, traffic-visibility]
level: practitioner
status: draft
description: "Configure Flexible NetFlow on IOS-XE: custom flow record keys and fields, an exporter to a collector, a monitor with cache timeouts, applied per interface."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/fnetflow/configuration/xe-16/fnf-xe-16-book/fnf-fnetflow.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/nmgmt/b_179_nmgmt_9300_cg/configuring_flexible_netflow.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Flexible NetFlow: record, exporter, monitor

Three objects: a **record** (what makes a flow unique and what to count), an **exporter**
(where to send), a **monitor** (cache + record + exporters) applied to interfaces.

```
flow record FR-V4
 match ipv4 source address
 match ipv4 destination address
 match ipv4 protocol
 match transport source-port
 match transport destination-port
 match ipv4 tos
 match interface input
 collect interface output
 collect counter bytes long
 collect counter packets long
 collect timestamp absolute first
 collect timestamp absolute last
 collect transport tcp flags
!
flow exporter FE-COLLECTOR
 destination 10.99.0.60
 source Loopback0
 transport udp 2055
 export-protocol ipfix
 template data timeout 60
 option interface-table
!
flow monitor FM-V4
 record FR-V4
 exporter FE-COLLECTOR
 cache timeout active 60
 cache timeout inactive 15
!
interface GigabitEthernet0/0/0
 ip flow monitor FM-V4 input
 ip flow monitor FM-V4 output
```
- `match` fields are the key; `collect` fields are counted/recorded. Adding keys multiplies
  cache entries.
- `cache timeout active 60` makes long flows report every minute; the default 1800 s makes
  graphs spiky and late.
- `option interface-table` lets the collector map ifIndex to names.
- On Catalyst 9000 switches, the `match` fields supported in hardware are limited; check the
  platform guide, and `datalink` records exist for L2.
- IPv6 needs its own record and `ipv6 flow monitor`.

## Verify
```
show flow monitor FM-V4 cache format table | begin IPV4
show flow exporter FE-COLLECTOR statistics     ! packets sent, no errors
show flow interface Gi0/0/0
```
- [ ] Cache populates, exporter counters rise, collector shows flows with interface names.
