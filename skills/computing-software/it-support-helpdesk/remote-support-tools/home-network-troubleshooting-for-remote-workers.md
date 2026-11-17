---
id: computing-software.it-support-helpdesk.remote-support-tools.home-network-troubleshooting-for-remote-workers
name: home-network-troubleshooting-for-remote-workers
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, home-network-troubleshooting, remote-work, wifi, double-nat, subnet-overlap, isp]
level: practitioner
status: draft
description: "Diagnose a remote worker's home network: Wi-Fi vs ISP vs corporate side, signal and band checks, double NAT, subnet overlap with corporate ranges, and where support stops."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netsh-wlan"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/pathping"
  - "https://www.ncsc.gov.uk/guidance/home-working"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# home-network-troubleshooting-for-remote-workers

## Split the path
1. Router: `ping -n 20 <default gateway>` (find with `ipconfig`). Loss or over 10 ms here
   = Wi-Fi problem in the house.
2. Internet: `ping -n 20 1.1.1.1` and `pathping 1.1.1.1`. Loss starting at hop 2-3 = ISP.
3. Corporate: VPN/ZTNA up and an internal resource reachable. Only this part is yours.

## Wi-Fi checks
- `netsh wlan show interfaces`: signal %, radio type, band/channel, receive rate. Below
  ~60% or a 2.4 GHz link at 72 Mbps explains video freezes.
- Move closer, use 5/6 GHz, or plug in Ethernet as a test. A wired test that works ends
  the debate.
- Powerline adapters and old repeaters halve throughput and add jitter.

## Classic home problems
| Symptom | Cause |
|---|---|
| Fine until evening, then calls break | Household streaming/gaming saturating upload |
| VPN connects but some internal subnets unreachable | Home LAN uses the same range as an office subnet (e.g. 192.168.1.0/24) |
| VPN or games break, others fine | Double NAT (ISP router plus own router) or carrier-grade NAT |
| Random DNS failures | ISP router DNS proxy; test with `Resolve-DnsName example.com -Server 1.1.1.1` |

## Where support stops
Give guidance (reboot router, move it, wire up, call ISP with the pathping output) but do
not log in to personal routers or change home devices unless policy covers it. Offer a
company hotspot or office desk if the home link cannot support the job.

## Gotchas
- Speed tests measure peak download; video calls need stable upload and low jitter.
- Corporate laptops with outdated Wi-Fi drivers drop on mesh networks; update the driver.

## Verify
With the fix in place, 20-ping tests to router and internet show no loss, and a 10-minute
test call stays clean.
