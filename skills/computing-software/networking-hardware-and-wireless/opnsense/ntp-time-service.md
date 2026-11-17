---
id: computing-software.networking-hardware-and-wireless.opnsense.ntp-time-service
name: ntp-time-service
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [ntp, ntpd, time-servers, gps, pps]
level: practitioner
status: docs-checked
description: "Configure OPNsense network time: listening interfaces, time servers, orphan mode, access restrictions, GPS/PPS and reading the status table."
sources: ["https://docs.opnsense.org/manual/ntpd.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Network time (NTPd)

OPNsense runs a standard NTPd that syncs with upstream servers and serves clients. New installs have NTP enabled on all interfaces (the firewall blocks non-LAN access by default), forwarding to X.opnsense.pool.ntp.org (X = 0 to 3). There is no enable toggle: NTP is disabled if no time servers are configured.

Interface(s) is used for both listening and outgoing queries. Selecting none listens on all with a wildcard; selecting all listens only on the explicit addresses. The selection should include a WAN-type interface so normal routing works. LAN-only often works thanks to source NAT but can cause asymmetric routing on secondary nodes under CARP. The recommended default is all interfaces, with firewall rules constraining access.

Other options: Time servers with Prefer and Do not use toggles; Orphan mode (stratum reported when no other clock is available, set high so other servers win); NTP graphs (RRD in Reporting > Health); Syslog logging; Statistics logging to /var/log/ntp; Access restrictions; manual Leap seconds file. A GPS receiver supporting NMEA can be a reference clock (some brands preconfigured), and PPS signals are configured with a serial port.

Status table: Status, Server, Ref ID (IP or kiss code), Stratum (lower is closer to source), Type (u unicast, b broadcast, p pool, l local, s symmetric, A/B/M servers), When, Poll, Reach, Delay, Offset and Jitter. Reach is an octal shift register: 377 means no losses; 257 is binary 10101111, so two of the last eight polls failed and the most recent four succeeded.

## Checked

2026-11-03. Read the Network Time manual page (ntpd.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
