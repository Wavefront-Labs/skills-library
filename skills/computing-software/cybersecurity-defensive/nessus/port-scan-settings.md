---
id: computing-software.cybersecurity-defensive.nessus.port-scan-settings
name: port-scan-settings
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, scan-policy, port-scan-settings, syn-scan, netstat-scanner, port-range, scan-performance]
level: practitioner
status: draft
description: "Tune Nessus port scanning: SYN vs TCP connect, credentialed netstat enumeration, port ranges, UDP trade-offs, and firewall detection settings."
sources: ["https://docs.tenable.com/nessus/Content/SettingsDiscovery.htm", "https://docs.tenable.com/nessus/Content/PortScanning.htm", "https://docs.tenable.com/nessus/Content/SettingsPerformance.htm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Port scanning settings

**Goal:** find every listening service without wasting hours or knocking over hosts.

## Settings (Discovery > Port Scanning)
- **Port scan range:** `default` (about 4,790 common ports) or `1-65535`. Use all ports
  for internet-facing and server ranges; default is acceptable for workstation sweeps.
- **Local port enumerators (credentialed):** SSH (netstat), WMI (netstat), SNMP. With
  valid credentials, Nessus reads listening ports from the host itself, faster and complete.
  *Only run network port scanners if local port enumeration failed*: keep on to save time.
- **Network port scanners:**
  - **SYN:** default, fast, half-open. Firewall detection setting
    (*Automatic (normal)*, *Disabled*, *Do not detect RST rate limitation*, *Ignore closed ports*)
    handles hosts that rate limit RSTs.
  - **TCP (connect):** full handshake; use when SYN is blocked or you scan through some
    stateful devices; noisier in logs.
  - **UDP:** very slow (ICMP rate limiting) and unreliable; limit to a short list
    (53, 69, 123, 161, 500, 1900) in a custom range like `T:1-65535,U:53,69,123,161,500`.
- **Verify open TCP ports found by local port enumerators:** off normally; on to see what is
  actually reachable through host firewalls.

## Performance (Advanced)
- *Max simultaneous checks per host* and *Max simultaneous hosts per scan*: lower for
  fragile networks or VPN links (e.g. 2 checks, 10 hosts); defaults are tuned for LANs.
- *Network timeout*: raise for high-latency links.
- *Slow down the scan when network congestion is detected*: on for WAN.

## Gotchas
- IPS and host firewalls may block the scanner partway through; results show hosts with
  only a few ports. Allowlist scanner IPs on IPS (and document it) for authenticated scans.
- Netstat-based results show ports listening on localhost too; those are not exposed.
- Scanning through a load balancer or proxy shows its ports, not the backends.

## Verify
For a sample host compare Nessus plugin 34252/14272 (netstat) results with `ss -tulpn` or
`netstat -ano` on the host, and plugin 11219 (SYN) results with an external nmap run.
