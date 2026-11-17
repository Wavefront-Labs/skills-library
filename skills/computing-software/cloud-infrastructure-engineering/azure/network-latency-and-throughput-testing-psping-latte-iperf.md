---
id: computing-software.cloud-infrastructure-engineering.azure.network-latency-and-throughput-testing-psping-latte-iperf
name: network-latency-and-throughput-testing-psping-latte-iperf
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, network-troubleshooting, psping, latte, iperf, latency-testing, throughput, accelerated-networking]
level: advanced
status: docs-checked
description: "Measure Azure VM-to-VM latency with latte or sockperf and throughput with NTttcp, use psping and AzureCT on hybrid links, and avoid misleading ICMP results."
sources: ["https://learn.microsoft.com/azure/virtual-network/virtual-network-test-latency", "https://learn.microsoft.com/azure/virtual-network/virtual-network-bandwidth-testing", "https://learn.microsoft.com/sysinternals/downloads/psping", "https://learn.microsoft.com/azure/expressroute/expressroute-troubleshooting-network-performance"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Latency and throughput testing in Azure

**Goal:** get trustworthy numbers when someone says "the network is slow".

## Rules first
- ICMP is not representative of TCP/UDP traffic, so do not base a latency verdict on ping alone.
- Test VM to VM with the same sizes as production. Each VM SKU has a bandwidth limit, so a small SKU caps the test; the ExpressRoute page suggests a DS5v2 for testing.
- Tips from the latency page: Accelerated Networking, proximity placement groups, larger VMs, and a baseline to compare against.
- Open the test ports in NSGs (the ExpressRoute page names 5201 for iPerf, 3389 for RDP, 22 for SSH).

## Latency
Windows (latte), run from the Windows command line, not PowerShell:
```
latte -a 10.0.0.4:5005 -i 65100          # receiver
latte -c -a 10.0.0.4:5005 -i 65100       # sender
```
Linux (sockperf, built from the mellanox/sockperf repo on the page):
```bash
sudo sockperf sr --tcp -i 10.0.0.4 -p 12345                                 # server
sockperf ping-pong -i 10.0.0.4 --tcp -m 350 -t 101 -p 12345 --full-rtt     # client
```
The receiver needs a firewall allow rule for latte.exe (the page uses `netsh advfirewall firewall add rule program=<path>latte.exe ...`).

psping (Sysinternals) can run a TCP connect test and a latency/bandwidth test against a `-s` server:
```
psping -n 100 -i 0 -q host:80            # TCP connect test
psping -l 8k -n 10000 -h 100 host:port   # latency with histogram
psping -b -l 8k -n 10000 -h 100 host:port   # bandwidth; add -u for UDP
```
`-h` takes a bucket count. The psping page notes the histogram needs at least one second of data after warmup.

## Throughput (NTttcp)
```
ntttcp -r -m 4,*,10.0.0.5 -t 300     # receiver: -m is [VM cores x 2],*,<receiver IP>
ntttcp -s -m 4,*,10.0.0.5 -t 300     # sender
```
- The page recommends 300 s runs; the Linux default is 60 s. Use same-size VMs in the same proximity placement group or availability set.
- Windows and Linux pairs: the page's mixed-OS examples add `-ns` or `-N` to the sender command; follow its examples for the direction you test.

## ExpressRoute and VPN links (AzureCT)
One host must be Windows, the other Windows or Linux. On Windows: install the AzureCT module, run `Install-LinkPerformance` (installs iPerf and PSPing in a new ACTTools directory on the system drive and opens ICMP and port 5201), start iPerf in server mode on the remote host, then:
```
Get-LinkPerformance -RemoteHost 10.0.0.1 -TestSeconds 10
```
Results are saved as text files in the ACTTools directory. The page warns that expecting a full 1 Gbps over a 1 Gbps circuit at 100 ms latency is unrealistic because of TCP behaviour on high-latency links. To isolate the problem domain, test from the edges (Azure, WAN, corporate network) inward, and check NSGs, UDRs and VM SKU limits.

## Verify
- [ ] Recorded test matrix: tool, direction, VM sizes, placement, run length, results, date.

## Checked

2026-11-07. Read in full: Test VM network latency, Test VM network throughput, Sysinternals PsPing. ExpressRoute network performance article: read the summary, components, tools/AzureCT and the start of troubleshooting (assumptions); the later troubleshooting steps and references were not read in full.
- Removed (not on the pages): iperf3 commands and "always use multiple streams", the same-zone/cross-zone latency figures, the Accelerated Networking `az network nic show` check, "Azure load balancers drop ICMP", and the `psping -n 1000 -h 20` form.
- Corrected: latte iteration count (65100 on the page), NTttcp run time (300 s) and `-ns`/`-N` flags, psping `-h` meaning.
- Commands are shown as the pages give them; nothing was executed.

Method: documentation only; no commands were run.
