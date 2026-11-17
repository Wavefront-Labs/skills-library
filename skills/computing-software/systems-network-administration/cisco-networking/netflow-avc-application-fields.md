---
id: computing-software.systems-network-administration.cisco-networking.netflow-avc-application-fields
name: netflow-avc-application-fields
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, netflow, avc, application-visibility, nbar2, application-name, flexible-netflow, performance-monitor]
level: practitioner
status: draft
description: "Export application identity from IOS XE with AVC: NBAR2 protocol discovery, application name fields in FNF records, option templates and collector mapping."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/avc/configuration/xe-16/avc-xe-16-book.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/qos_nbar/configuration/xe-16/qos-nbar-xe-16-book.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AVC application fields in flow records

## What AVC adds
Application Visibility and Control uses NBAR2 deep packet inspection to identify applications
(over 1,400 protocols: ms-teams, webex-media, youtube...) and exports the application ID in
NetFlow/IPFIX, so collectors report by application instead of port.

## Record with application name
```
flow record AVC-REC
 match ipv4 source address
 match ipv4 destination address
 match ipv4 protocol
 match transport source-port
 match transport destination-port
 match interface input
 match application name
 collect interface output
 collect counter bytes long
 collect counter packets long
 collect timestamp absolute first
 collect timestamp absolute last
flow exporter AVC-EXP
 destination 10.0.0.70
 transport udp 2055
 export-protocol ipfix
 option application-table timeout 600        ! maps application ID -> name
 option application-attributes timeout 600   ! category, sub-category
flow monitor AVC-MON
 record AVC-REC
 exporter AVC-EXP
interface Gi0/0/0
 ip flow monitor AVC-MON input
 ip flow monitor AVC-MON output
```
Simpler on IOS XE 16.3+: Easy Performance Monitor (`performance monitor context ... profile application-experience`).

## Notes
- `match application name` exports a numeric ID (classification engine + selector). Without the
  option application-table the collector shows numbers.
- NBAR2 protocol packs update separately from IOS (`show ip nbar protocol-pack active`).
- Encrypted traffic is classified by SNI/DNS/flow patterns; accuracy is lower for unknown SaaS.
- CPU cost: NBAR on many interfaces at high rates; check platform capacity.

## Verify
```
show flow monitor AVC-MON cache format table | include webex|teams
show ip nbar protocol-discovery top-n 10
show flow exporter AVC-EXP statistics
```
- [ ] Collector displays application names (not IDs) for top flows.
