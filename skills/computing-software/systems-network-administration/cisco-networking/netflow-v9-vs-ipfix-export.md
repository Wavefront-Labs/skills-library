---
id: computing-software.systems-network-administration.cisco-networking.netflow-v9-vs-ipfix-export
name: netflow-v9-vs-ipfix-export
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, netflow, netflow-v9, ipfix, templates, flow-export, collector-compatibility, template-refresh, rfc3954, rfc7011]
level: practitioner
status: docs-checked
description: "NetFlow v9 (RFC 3954) vs IPFIX (RFC 7011) export: template sets, transports and ports, template refresh over UDP, enterprise fields and variable length."
sources:
  - https://www.rfc-editor.org/rfc/rfc3954
  - https://www.rfc-editor.org/rfc/rfc7011
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/fnetflow/configuration/xe-16/fnf-xe-16-book/fnf-fnetflow.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# NetFlow v9 vs IPFIX export

## What the two protocols share
Both are template based. The exporter first describes the record layout in a template, then sends data records that
only make sense with that template. A collector that has not seen (or has expired) the template cannot decode the data.

| | NetFlow v9 (RFC 3954) | IPFIX (RFC 7011) |
|---|---|---|
| Set types | Template FlowSet (ID 0), Options Template FlowSet (ID 1), Data FlowSets (ID above 255) | Template Set (ID 2), Options Template Set (ID 3), Data Sets (ID 256 and up) |
| Version field | 9 | 10 (0x000a) |
| Stream identifier | 32-bit Source ID (Observation Domain); collectors SHOULD key streams on source IP plus Source ID | 32-bit Observation Domain ID in the message header |
| Transport | Designed to be transport independent; UDP, or SCTP | SCTP, TCP or UDP; UDP is not congestion-aware, so contain or provision the path |
| Default port | None in the RFC | Collector listens on 4739 (SCTP/TCP/UDP); 4740 for secure connections; ports must be configurable |
| Vendor fields | Not described | Enterprise bit in the field specifier plus a 32-bit Enterprise Number (bit 0 means IANA element) |
| Variable-length fields | Not described | Length 65535 is reserved to mean variable length; the length is carried in the data (one octet for under 255, else 255 then two octets) |
| Template withdrawal | Not described | Defined for SCTP and TCP; MUST NOT be sent over UDP and MUST be ignored there |

Choose IPFIX when the collector supports it; v9 is what older collectors speak. Cisco's Flexible NetFlow chapter says
exporters use UDP and the Version 9 format by default, and its exporter command accepts
`export-protocol {netflow-v5 | netflow-v9 | ipfix}` with `transport udp <port>`. Which of those values a given
platform accepts is not confirmed here.

## Template refresh (the usual cause of undecodable data)
- v9 (RFC 3954 section 7): the exporter sends a new template as soon as possible, SHOULD send changed templates at an
  accelerated rate after a configuration change, and MUST resend all templates and options templates regularly,
  either every N export packets or every N minutes. Both options MUST be user-configurable on the exporter.
- A v9 or IPFIX collector expires templates it has not seen refreshed within a timeout, and MUST NOT decode data with
  an expired template (RFC 3954 section 9).
- IPFIX over UDP (RFC 7011 8.4): the exporter MUST retransmit each active template periodically, and the interval
  MUST be configurable (templateRefreshTimeout and optionsTemplateRefreshTimeout from RFC 6728). Default values are
  deployment specific. Before sending data for a template, especially after Template ID reuse, the exporter SHOULD send
  multiple copies of the template. A collector deriving lifetime from observed retransmissions SHOULD default to at
  least three times the retransmission interval.
- Over TCP and SCTP the end of the transport session withdraws all templates; they must be resent in the next session.
- Collector symptom "no template for ID 256" after a collector restart therefore means: data arrived before the next
  scheduled refresh. Shorten the exporter's refresh interval, or restart the collector first.
- Because streams are keyed on exporter address plus Source ID or Observation Domain ID, a change of source address on
  the exporter looks like a new stream with no templates.

## Options templates
Options Template FlowSets carry exporter metadata such as the sampling rate (RFC 3954 section 6.1); IPFIX defines
Options Template Sets and optional Metering Process statistics options templates. A collector that needs the sampling
rate to scale counts must receive these, so check the options data is exported.

## Verify
- [ ] Collector shows templates for every exporter address and Source/Observation Domain ID in use.
- [ ] After a collector restart, decoding resumes within one configured refresh interval.
- [ ] The UDP port on exporter and collector agree (IPFIX default 4739).

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read RFC 3954 sections 3.3, 4, 5 (Source ID), 6.1 and 7 (template
management) and 9 (collector rules), RFC 7011 sections on information element specifiers (enterprise bit), variable
length encoding, template withdrawal, UDP template management (8.4) and transport defaults (10), and the Cisco Flexible
NetFlow chapter (exporter transport, export-protocol values). Removed as unconfirmed: the v5 column and the v5 port
numbers, the claim that v9 lacks variable length or has limited enterprise support, `template data timeout` syntax
and its defaults, sFlow remarks, Wireshark decode steps, and show flow exporter commands.
