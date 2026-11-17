---
id: computing-software.cybersecurity-defensive.security-operations.fakenet-inetsim-network-simulation
name: fakenet-inetsim-network-simulation
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [fakenet, inetsim, malware-analysis, network-simulation, dynamic-analysis, c2-analysis, remnux, flare-vm]
level: practitioner
status: draft
description: "Simulate network services for malware analysis with FakeNet-NG and INetSim: DNS and HTTP responses, capturing C2 traffic and configuring safe isolated labs."
sources: ["https://github.com/mandiant/flare-fakenet-ng", "https://www.inetsim.org/documentation.html", "https://docs.remnux.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Network simulation with FakeNet-NG and INetSim

Malware often refuses to run fully without network. Simulators answer its requests safely so you
can observe C2 protocols, URLs and downloads.

## FakeNet-NG (on the Windows analysis VM, FLARE-VM)
- Run as admin: `fakenet.exe`. It redirects all traffic to local listeners (DNS, HTTP/S, SMTP, FTP,
  raw TCP/UDP) via WinDivert, logs requests and writes a PCAP.
- Config `configs/default.ini`: set `RedirectAllTraffic`, per-listener options, custom responses
  (serve a specific file for a URL pattern), process blacklist to ignore noisy system processes.
- HTTPS listener uses a generated CA; malware with certificate pinning will fail (record that).

## INetSim (on a Linux gateway VM, REMnux)
- Analysis VM uses REMnux as default gateway and DNS. Configure `/etc/inetsim/inetsim.conf`:
  `service_bind_address <remnux_ip>`, `dns_default_ip <remnux_ip>`, enable services.
- `inetsim` serves fake HTTP/HTTPS/DNS/SMTP/IRC etc., with fake files by extension (`.exe` returns
  a benign executable).
- Combine with `iptables` redirect for non-standard ports, and capture with `tcpdump`/Wireshark on
  the gateway.

## Analysis
- From logs: DNS names, HTTP request URIs, user agents, POST bodies (beacon format), SNI.
- Iterate: serve plausible responses (e.g. expected config file) to coax further behaviour.
- Extract indicators and protocol details for detections (URI patterns, headers, JA3/JA4).

## Safety
- Host-only network; no route to real internet unless you deliberately do controlled live
  analysis through a separate, monitored egress.
- Snapshot before each run; malware may attack the gateway too.

## Gotchas
- Samples checking connectivity to well-known sites with specific content may detect simulation.
- DGA samples resolve many domains; FakeNet answers all, which may differ from real-world behaviour.

## Verify
PCAP and simulator logs show the sample's outbound requests; indicators match those seen in sandbox
or production telemetry.
