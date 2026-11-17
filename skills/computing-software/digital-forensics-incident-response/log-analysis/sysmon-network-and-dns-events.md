---
id: computing-software.digital-forensics-incident-response.log-analysis.sysmon-network-and-dns-events
name: sysmon-network-and-dns-events
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [sysmon-network-events, sysmon, event-id-3, event-id-22, dns-query-logging, c2-detection, beaconing, dfir]
level: practitioner
status: docs-checked
description: "Investigate with Sysmon Event 3 (network connection) and Event 22 (DNS query): what they log, filter tags and linking to the originating process."
sources: ["https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sysmon network and DNS events (3, 22)

**Goal:** attribute network activity to the exact process, which firewall and proxy logs
cannot do. Events are UTC-stamped, in Applications and Services Logs/Microsoft/Windows/Sysmon/Operational.

## Event 3: network connection
Logs TCP/UDP connections on the machine and is **disabled by default**. Each connection is linked
to a process through the ProcessId and ProcessGuid fields, and the event contains source and
destination host names, IP addresses, port numbers and IPv6 status. Sysmon's installation with
default settings does no network monitoring; enable it through the `NetworkConnect` filter tag.

## Event 22: DNS query
Generated when a process executes a DNS query, whether successful or failed, cached or not.
Filter tag `DnsQuery`. Telemetry was added for Windows 8.1, so it is not available on Windows 7
and earlier.

## Config tuning
Event filtering exists because gathering everything is often not possible. The documented
approach is `NetworkConnect` include rules (for example by `DestinationPort`) combined with
exclude rules (for example `Image` with `end with`); excludes override includes. Rules on the
same field are ORed and rules on different fields ANDed; add `name` attributes to rules so
the event records which rule matched. Decide which processes and ports matter for your case
before enabling Event 3, since volume can be high.

## Pivoting
The ProcessGuid is a unique value for the process across a domain and links events 3 and 22
to the process creation event (Event ID 1: full command line, parent process, hashes).

## Hunting ideas (analyst judgement, not from the page)
- Office or script-host processes making external connections.
- Domains queried by only one host; many failed lookups from one process.
- Regular connection intervals per ProcessGuid and destination.

## Gotchas
- Sysmon does not analyse events for you and does not hide itself from attackers.
- Event 22 records queries made by processes on that host only; traffic that never uses the
  Windows DNS client path will not appear there, so corroborate with network-side logs.

## Self-check
For each suspicious connection you can name the process (with command line via the process
creation event), the domain requested, and the timing pattern.

## Checked
2026-11-09. Confirmed on the Sysmon page (read in full): Event 3 and 22 descriptions, disabled-by-default network event, ProcessGuid linkage, filter tags, include/exclude and AND/OR rules, rule names, Windows 8.1 DNS note, UTC, the statement that Sysmon does no analysis. Removed: field lists with QueryStatus codes, ETW provider claim, DoH/WSL claims, LOLBin and port lists, the KQL hunt, beaconing/DGA/tunnelling specifics, sysmon-modular and SwiftOnSecurity sources (not read).
Method: documentation only; no commands were run.
