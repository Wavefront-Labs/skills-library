---
id: computing-software.systems-network-administration.windows-server.network-connectivity-testing
name: network-connectivity-testing
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, netadapter, server-networking, test-netconnection, pathping, tracert, portqry, resolve-dnsname, pktmon, netsh-trace, get-nettcpconnection, troubleshooting]
level: practitioner
status: docs-checked
description: "Troubleshoot server connectivity: Test-NetConnection, pathping, Resolve-DnsName, Get-NetTCPConnection, PortQry for UDP and RPC, pktmon and netsh trace."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/pktmon/pktmon
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/pktmon-start
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/pktmon-etl2pcap
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/pathping
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/portqry-command-line-port-scanner-v2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network connectivity testing on Windows Server

Work up the stack: name resolution, route, port, application.

```powershell
Resolve-DnsName app02.ad.example.com                 # which IP, from which server (-Server dc01)
Test-NetConnection app02 -TraceRoute                 # ICMP + route
Test-NetConnection app02 -Port 443 -InformationLevel Detailed   # TCP handshake, source IP/interface used
Test-NetConnection -ComputerName app02 -CommonTCPPort SMB
Find-NetRoute -RemoteIPAddress 10.50.1.20            # which local route/interface would be used
pathping /n app02                                    # per-hop loss statistics (skips name resolution)
```
- ICMP blocked does not mean the port is closed; always test the actual port.
- `TcpTestSucceeded : False` with `PingSucceeded : True` points to a firewall or no listener on that port.

## On the target
```powershell
Get-NetTCPConnection -LocalPort 443 -State Listen
Get-NetTCPConnection -RemoteAddress 10.0.10.25 | Select LocalPort,RemotePort,State,OwningProcess
Get-Process -Id (Get-NetTCPConnection -LocalPort 443 -State Listen).OwningProcess
Get-NetFirewallRule -Enabled True -Direction Inbound | Get-NetFirewallPortFilter | ? LocalPort -eq 443
```

## UDP and RPC
`Test-NetConnection` tests TCP ports. **PortQry** (a separate Microsoft download) reports TCP and UDP port status,
distinguishing LISTENING, NOT LISTENING and FILTERED, and querying port 135 returns the endpoints registered with the
RPC endpoint mapper:
```cmd
portqry -n dc01 -e 389 -p udp
portqry -n dc01 -e 135      (lists endpoints registered with the RPC endpoint mapper)
```

## Capture packets without installing anything
```cmd
pktmon start --capture --pkt-size 0 -f <LOG_DIR>\cap.etl
pktmon stop
pktmon etl2pcap <LOG_DIR>\cap.etl -o <LOG_DIR>\cap.pcapng      :: dropped packets are excluded unless you ask for them
:: or
netsh trace start capture=yes tracefile=<LOG_DIR>\trace.etl maxsize=512
netsh trace stop
```
The pcapng can be analysed in Wireshark (or any pcapng analyser). `--pkt-size 0` logs whole packets (default 128
bytes). Add filters before starting (`pktmon filter add -i 10.0.10.25 -p 445`; up to 32 filters) to keep captures
small; `pktmon counters` gives a quick per-component view of traffic and drops.

## Verify
- [ ] Root cause identified at the right layer (DNS, route, firewall, listener, app).
- [ ] Capture files deleted after analysis (they may contain credentials/data).

## Checked

2026-10-27. Documentation release: Windows Server networking pktmon pages and command references for pktmon start, etl2pcap, netsh trace, pathping and ping, the PortQry documentation, and the Test-NetConnection and NetTCPIP cmdlet references (Windows Server 2022 docset). Confirmed: -TraceRoute, -Port, -InformationLevel Detailed, -CommonTCPPort values (HTTP, RDP, SMB, WINRM), pathping /n, PortQry -n/-e/-p and RPC endpoint mapper behaviour, pktmon --pkt-size 0, -f, filter syntax and 32-filter limit, etl2pcap -o and dropped-packet behaviour, netsh trace start capture=yes tracefile= maxSize=. Removed the absolute TCP-only wording and the 5-minute pathping figure, which no fetched page covers.

Method: documentation only; no commands were run.
