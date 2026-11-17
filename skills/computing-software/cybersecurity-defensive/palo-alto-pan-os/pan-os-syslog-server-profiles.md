---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-syslog-server-profiles
name: pan-os-syslog-server-profiles
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [syslog-server-profile, pan-os, syslog, cef, tls-syslog, siem-forwarding, custom-log-format]
level: practitioner
status: draft
description: "Configure PAN-OS syslog server profiles over UDP, TCP or TLS with BSD, IETF or custom formats, and trace delivery with tcpdump."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/monitoring/configure-syslog-monitoring"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: reliable, parseable log delivery to a SIEM.

```
configure
set shared log-settings syslog SYSLOG-SIEM server siem1 server 192.0.2.50 transport SSL port 6514 format IETF facility LOG_USER
commit
```
Choose TCP or TLS (SSL) over UDP, which drops silently under load. For TLS, the SIEM certificate must chain to a CA in the firewall's trusted CA list, and a service route for syslog must exist (Device > Setup > Services > Service Route Configuration).

Formats: BSD, IETF; custom formats allow CEF or LEEF with escaping (Custom Log Format tab) when the SIEM expects them. Keep field order stable between releases (confirm).

Delivery check:
```
tcpdump filter "host 192.0.2.50 and port 6514"
view-pcap mgmt-pcap mgmt.pcap
```
Run the capture for a short period, then delete it: `delete mgmt-pcap mgmt.pcap`.

Gotchas
- Logs leave from the management interface unless a service route says otherwise; firewall rules between the management network and SIEM often miss.
- The log forwarding profile, not the syslog profile, decides which logs are sent.
- Event-log timestamps follow the device time zone; set NTP and time zone consistently.

## Verify
```
show logging-status
```
Syslog destination shows connected (TCP/TLS), and the SIEM receives events from a test commit (a config log).
