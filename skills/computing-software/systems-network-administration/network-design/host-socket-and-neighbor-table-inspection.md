---
id: computing-software.systems-network-administration.network-design.host-socket-and-neighbor-table-inspection
name: host-socket-and-neighbor-table-inspection
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-tools, ss, netstat, arp-table, ip-neigh, get-nettcpconnection, lsof, listening-ports, connection-states, tcpdump, host-troubleshooting]
level: practitioner
status: draft
description: "Inspect host networking state on Linux, Windows and macOS: listening ports and owning processes (ss/netstat), connection states, ARP/neighbour tables and quick tcpdump checks."
sources:
  - https://man7.org/linux/man-pages/man8/ss.8.html
  - https://man7.org/linux/man-pages/man8/ip-neighbour.8.html
  - https://learn.microsoft.com/en-us/powershell/module/nettcpip/get-nettcpconnection
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Host socket and neighbour table inspection

## Is the service listening, and on what address?
```
Linux:   ss -tulpn                    # TCP/UDP listeners with process (root for -p)
         ss -tlpn 'sport = :443'
Windows: Get-NetTCPConnection -State Listen | Sort LocalPort
         netstat -ano | findstr :443   # PID, then Get-Process -Id <PID>
macOS:   lsof -nP -iTCP -sTCP:LISTEN
```
`127.0.0.1:8080` = only local clients can connect; `0.0.0.0` / `[::]` = all interfaces. A service
bound to localhost is the classic "works on the server, not from my PC".

## Connection states
```
ss -tan state established '( dport = :5432 )'
ss -s                                   # summary: estab, timewait, orphaned
ss -tin dst 10.20.5.10                  # per-socket TCP info: rtt, cwnd, retrans
```
| State pile-up | Meaning |
|---|---|
| SYN-SENT on client | no reply: firewall drop or host down |
| SYN-RECV on server | SYN flood or replies not reaching the client (asymmetric path) |
| CLOSE-WAIT on server | application not closing sockets (app bug) |
| TIME-WAIT many | normal for busy clients; watch for port exhaustion |

## Neighbour (ARP/ND) tables
```
Linux:   ip neigh show                   # REACHABLE/STALE/FAILED/INCOMPLETE
         ip neigh flush dev eth0
Windows: Get-NetNeighbor -AddressFamily IPv4 ; arp -a ; arp -d *
macOS:   arp -an ; ndp -an
```
FAILED/INCOMPLETE for the gateway = Layer 2 problem (VLAN, port, gateway down). Two IPs with
the same MAC on a LAN = proxy ARP, a router, or spoofing.

## Quick capture to confirm traffic arrives
```
sudo tcpdump -ni eth0 'tcp port 443 and host 10.20.30.40' -c 20
sudo tcpdump -ni any -w /tmp/cap.pcap 'port 53'
```
SYNs arriving with no SYN/ACK = host firewall or no listener; nothing arriving = network path.
Windows: `pktmon start --capture --comp nics --pkt-size 0`, `pktmon stop`, `pktmon etl2pcap`.

## Verify
- [ ] Service listener, bind address and owning process identified.
- [ ] Neighbour entry for the gateway is REACHABLE/STALE.
- [ ] tcpdump shows whether packets reach the host.
