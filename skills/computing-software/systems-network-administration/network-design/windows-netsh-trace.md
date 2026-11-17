---
id: computing-software.systems-network-administration.network-design.windows-netsh-trace
name: windows-netsh-trace
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-tools, netsh-trace, pktmon, windows-packet-capture, etl]
level: practitioner
status: draft
description: "Capture network traffic on Windows without installing Wireshark: netsh trace scenarios and filters, pktmon, converting ETL to pcapng, and capturing across reboots."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/pktmon/pktmon
  - https://github.com/microsoft/etl2pcapng
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows netsh trace

Built into Windows; useful on servers where installing Npcap/Wireshark is not allowed.

## netsh trace
```
netsh trace start capture=yes tracefile=<CAPTURE_DIR>\cap.etl maxsize=1024 filemode=circular overwrite=yes
netsh trace start capture=yes IPv4.Address=10.0.0.5 Protocol=TCP tracefile=<CAPTURE_DIR>\cap.etl
netsh trace start scenario=NetConnection capture=yes report=disabled tracefile=<CAPTURE_DIR>\cap.etl
netsh trace start capture=yes persistent=yes tracefile=<CAPTURE_DIR>\boot.etl   # survives reboot
# reproduce the problem
netsh trace stop
netsh trace show scenarios
```
Scenarios add ETW providers (e.g. `NetConnection`, `InternetClient`, `LAN`, `WLAN`, `DirectAccess`)
so the ETL contains component logs (Winsock, TCP/IP, DNS client) alongside packets. Run as admin;
the `.cab` beside the ETL holds system info.

## pktmon (Windows 10 1809+ / Server 2019+)
```
pktmon filter add -i 10.0.0.5 -p 443
pktmon start --capture --pkt-size 0 -f <CAPTURE_DIR>\pm.etl
pktmon stop
pktmon etl2pcap <CAPTURE_DIR>\pm.etl -o <CAPTURE_DIR>\pm.pcapng
pktmon counters            # where packets are dropped in the stack (drop reasons)
```
pktmon shows packets at each component (NIC, vSwitch, filter drivers): good for Hyper-V and drops
inside the host.

## Converting netsh ETL
`etl2pcapng.exe cap.etl cap.pcapng` (Microsoft GitHub) then open in Wireshark. Microsoft Network
Monitor and Message Analyzer are retired.

## Tips
- Use `maxsize` and circular mode for long waits; filters reduce file size.
- Capture both ends when possible; time-sync hosts (w32tm).

## Verify
- [ ] Converted pcapng opens in Wireshark and contains the traffic of interest with correct timestamps.
