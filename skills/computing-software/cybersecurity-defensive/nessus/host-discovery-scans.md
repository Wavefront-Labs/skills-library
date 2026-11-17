---
id: computing-software.cybersecurity-defensive.nessus.host-discovery-scans
name: host-discovery-scans
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, scan-policy, host-discovery-scan, ping-sweep, asset-discovery, scan-templates, tenable]
level: practitioner
status: draft
description: "Configure Nessus host discovery scans: ping methods, fragile device handling, ARP and TCP probes, and turning discovery results into scan targets and inventory."
sources: ["https://docs.tenable.com/nessus/Content/SettingsDiscovery.htm", "https://docs.tenable.com/nessus/Content/HostDiscovery.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Host discovery scans

**Goal:** find what is alive in a range quickly and safely, before running full
vulnerability scans, and catch assets nobody told you about.

## Template
New Scan > **Host Discovery**. Discovery types: *Host enumeration* (ping only),
*OS identification*, *Port scan (common ports)*, *Port scan (all ports)*, or *Custom*.
Run weekly across all owned ranges; run full vulnerability scans only against live hosts.

## Ping settings (Discovery > Host Discovery)
- **ARP** on local subnets: most reliable; hosts that block ICMP still answer ARP.
- **TCP** ping to common ports (`built-in` list or e.g. `22,80,443,445,3389`): finds
  hosts behind ICMP-dropping firewalls.
- **ICMP** (echo) with retries 2.
- **UDP** ping is slow and unreliable; leave off unless needed.
- *Test the local Nessus host*: off unless you want the scanner in results.
- *Use fast network discovery*: on for speed, off when firewalls spoof responses (some
  firewalls answer TCP for every IP, making every address look alive).

## Fragile devices
*Scan network printers*, *Novell Netware*, *Operational Technology devices* default to off:
keep them off on general scans; printers print garbage on raw port 9100 probes and OT
devices can fault. Scan OT with passive tools (Tenable OT/Nessus Network Monitor) instead.

## Wake-on-LAN
Optional: send WoL to MAC lists before the scan for sleeping workstations.

## Using the results
- Export live hosts (CSV) and feed the asset inventory; diff against CMDB to spot unknown
  hosts (see unauthorised asset detection).
- Create target groups from discovered ranges for authenticated scans.
- Unknown live hosts in server ranges are investigation tickets, not just scan targets.

## Gotchas
- Hosts that do not respond to any ping method are marked dead and not scanned; a strict
  host firewall can hide a server. Check firewall rules or enable *consider unscanned hosts*
  in platform reporting.
- Proxy ARP or load balancers can answer for ranges and inflate counts.
- Scanning across NAT gives the NAT device, not hosts behind it.

## Verify
Compare discovery output against DHCP leases and the EDR console for the same ranges;
explain every host present in one source but not the other.
