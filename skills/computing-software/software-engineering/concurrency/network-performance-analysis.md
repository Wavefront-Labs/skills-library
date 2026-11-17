---
id: computing-software.software-engineering.concurrency.network-performance-analysis
name: network-performance-analysis
category: computing-software
field: software-engineering
product: concurrency
tags: [performance, network-performance, tcp-retransmits, ss, sar, nstat, linux-networking]
level: advanced
status: draft
description: "Diagnose network performance on Linux: throughput and latency, TCP retransmits, socket queues and buffers, with sar, nstat, ss, tcpretrans and iperf3."
sources: ["https://man7.org/linux/man-pages/man8/ss.8.html", "https://man7.org/linux/man-pages/man1/sar.1.html", "https://github.com/iovisor/bcc/blob/master/tools/tcpretrans_example.txt", "https://www.brendangregg.com/USEmethod/use-linux.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Network performance analysis (TCP retransmits / ss / sar)

## Interface level
```
sar -n DEV 1             # rxkB/s, txkB/s per interface: compare with link/instance bandwidth limits
sar -n EDEV 1            # errors, drops (rxdrop/s, txdrop/s)
ip -s link show eth0     # counters incl. dropped, overruns
ethtool -S eth0 | grep -iE 'drop|err|discard|exceed'   # NIC/driver drops; ENA "bw_*_allowance_exceeded" on AWS
```
Cloud instances have bandwidth and packets-per-second caps; exceeding them shows as drops in
`ethtool -S` (AWS ENA `pps_allowance_exceeded`, `conntrack_allowance_exceeded`).

## TCP health
```
sar -n TCP,ETCP 1        # active/passive opens, retrans/s, errors
nstat -az | grep -iE 'Retrans|ListenOverflows|ListenDrops|TCPTimeouts|SynRetrans'
sudo tcpretrans          # BCC: each retransmit with addresses and state
ss -tni dst 10.0.3.7     # per-connection: rtt, rttvar, cwnd, retrans, delivery rate
```
- Retransmits > ~1% of segments = loss somewhere (congestion, bad link, overloaded middlebox, NIC drops).
- `ListenOverflows`/`ListenDrops` = accept queue full: app not calling `accept()` fast enough or
  `somaxconn`/backlog too small.
- `SynRetrans` = connection attempts failing (firewall, SYN backlog, remote overload).
- Many `TIME-WAIT` from short-lived outbound connections: use connection pooling/keepalive; ephemeral
  port exhaustion shows as `EADDRNOTAVAIL` connect errors.

## Socket queues
`ss -tn`: `Recv-Q` growing = application not reading; `Send-Q` growing = peer/network not draining
(receiver window, congestion). Buffer tuning (`net.ipv4.tcp_rmem/wmem`) matters for high
bandwidth-delay paths (cross-region): throughput <= window / RTT.

## Measure capacity and latency
```
iperf3 -s                       # on server
iperf3 -c server -P 4 -t 30     # throughput with 4 streams; -R reverse; -u UDP loss/jitter
mtr -rwc 100 host               # per-hop loss and latency
ping -c 100 host                # RTT distribution
```

## Typical root causes
Instance bandwidth caps, cross-AZ/region RTT in chatty protocols (N+1 calls), MTU/fragmentation
mismatches (PMTU blackholes with VPNs/tunnels: test `ping -M do -s 1472`), conntrack table full
(`nf_conntrack: table full` in dmesg), DNS resolution latency, Nagle + delayed ACK (40 ms stalls:
`TCP_NODELAY`).
