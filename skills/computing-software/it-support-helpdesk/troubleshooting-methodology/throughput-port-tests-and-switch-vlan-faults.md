---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.throughput-port-tests-and-switch-vlan-faults
name: throughput-port-tests-and-switch-vlan-faults
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, iperf, test-netconnection, switch-port-vlan, throughput-testing, port-reachability, vlan]
level: practitioner
status: draft
description: "Measure network throughput with iperf3, test TCP port reachability with Test-NetConnection and nc, and recognise switch port, speed/duplex and VLAN faults from the client side."
sources:
  - "https://iperf.fr/iperf-doc.php"
  - "https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection"
  - "https://www.cisco.com/c/en/us/support/docs/lan-switching/ethernet/10561-3.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# throughput-port-tests-and-switch-vlan-faults

## Throughput with iperf3
```
iperf3 -s                                   # on the server/peer (TCP 5201)
iperf3 -c 10.0.0.20                         # client, 10 s test upload
iperf3 -c 10.0.0.20 -R                      # reverse: download
iperf3 -c 10.0.0.20 -P 4 -t 30              # 4 parallel streams, 30 s
iperf3 -c 10.0.0.20 -u -b 50M               # UDP at 50 Mbit/s: jitter and loss
```
- Test segment by segment: client to local switch-side server, then across the WAN.
  Internet speed tests measure the ISP path, not the LAN.
- Expect ~940 Mbit/s on clean gigabit wired; Wi-Fi depends on signal and band.
- Single stream much lower than parallel: TCP window / latency limits (long-distance or
  VPN), not bandwidth.

## Port reachability
```powershell
Test-NetConnection fileserver -Port 445            # TcpTestSucceeded True/False
Test-NetConnection smtp.example.com -Port 587 -InformationLevel Detailed
Test-NetConnection 8.8.8.8 -TraceRoute
```
- macOS/Linux: `nc -vz host 443`; `curl -v telnet://host:25` as a quick test.
- False with ping working: firewall (host or network) or service not listening
  (`netstat -ano | findstr :445` on the server).
- TCP success doesn't prove the app works (TLS, auth); test with the client too.

## Switch port and VLAN faults (seen from the client)
| Client symptom | Likely switch-side cause |
|---|---|
| Link up, 169.254 address | Port in wrong VLAN, DHCP not relayed there, 802.1X failed and port in guest/blocked VLAN |
| 100 Mbit/s instead of 1 Gbit | Bad cable pair, damaged port, forced speed |
| Slow with errors, worse under load | Duplex mismatch (one side forced full, other auto) |
| Works for a minute after plug-in then drops | Port security (MAC limit), spanning tree, NAC |
| Phone works, PC behind it doesn't | Voice/data VLAN config on the port |
- Client checks: `Get-NetAdapter | Select Name, LinkSpeed, FullDuplex`,
  `Get-NetAdapterStatistics` (errors), LLDP/CDP info (vendor tools or switch side) to
  identify the exact switch port.
- Give the network team: switch/port (from patch labels or LLDP), MAC address, VLAN
  expected, time of failure.

## Verify
Throughput is within expected range on each segment, required ports test True from the
client subnet, and port/VLAN issues are fixed with link at the right speed.
