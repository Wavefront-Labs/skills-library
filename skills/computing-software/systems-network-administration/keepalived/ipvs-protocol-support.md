---
id: computing-software.systems-network-administration.keepalived.ipvs-protocol-support
name: ipvs-protocol-support
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, ipvs, protocol-support, tcp, udp, esp, ah, sip-persistence-engine]
level: advanced
status: docs-checked
description: "Transport protocols IPVS can balance (TCP, UDP, ESP, AH) and the application helpers page: FTP helper, netfilter connection tracking, SIP persistence engine."
sources:
  - https://keepalived.readthedocs.io/en/latest/protocol_support.html
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPVS protocol support

Transport protocols IPVS can load balance: TCP, UDP, ESP (Encapsulation Security Payload) and AH (Authentication Header).

Keepalived's `virtual_server protocol` keyword documents TCP and UDP in the synopsis.

Application helpers in the docs:
- FTP protocol helper and Netfilter connection tracking: headings only, no description in the fetched page.
- SIP persistence engine: depends on UDP support and SIP netfilter connection tracking.

The page carries two open to-do notes (mention connection tracking, mention the ipip kernel module), so treat it as incomplete.

## Checked

2026-11-04: protocol list, helper headings, SIP engine dependency and to-do notes confirmed against the IPVS Protocol Support page; the protocol keyword against the configuration synopsis. Removed the Verify line.
Method: documentation only; no commands were run.
