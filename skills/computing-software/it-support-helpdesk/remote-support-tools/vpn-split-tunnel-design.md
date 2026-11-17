---
id: computing-software.it-support-helpdesk.remote-support-tools.vpn-split-tunnel-design
name: vpn-split-tunnel-design
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, split-tunnel-design, split-tunneling, force-tunnel, m365-optimize-endpoints, vpn, route-print]
level: advanced
status: draft
description: "Understand and troubleshoot VPN split vs full tunnel: Microsoft 365 optimize exclusions, route tables, symptoms of each mode, and checking which path traffic takes."
sources:
  - "https://learn.microsoft.com/en-us/microsoft-365/enterprise/microsoft-365-vpn-split-tunnel"
  - "https://learn.microsoft.com/en-us/microsoft-365/enterprise/microsoft-365-ip-web-service"
  - "https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/vpn/vpn-routing"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vpn-split-tunnel-design

- **Full (force) tunnel**: all traffic goes through the VPN, including internet. Central
  inspection, but Teams/Zoom media hairpins through the datacentre and congests the VPN.
- **Split tunnel**: only corporate subnets go through the VPN; everything else goes
  direct from the home network.
- **Force tunnel with exclusions** (Microsoft's recommended model for M365): tunnel
  everything except the Microsoft 365 **Optimize** category endpoints (Exchange Online,
  SharePoint, Teams media IP ranges), which go direct.

## Microsoft 365 exclusions
- Endpoint list from the M365 IP/URL web service
  (`https://endpoints.office.com/endpoints/worldwide?clientrequestid=<guid>`), filter
  `category = Optimize`. Exclude by IP range in the VPN client config (most clients
  support IP exclusions; FQDN exclusions vary by vendor).
- Teams media also uses UDP 3478-3481 to the Teams IP ranges.

## Symptoms that point to tunnel mode
| Symptom | Likely |
|---|---|
| Teams calls choppy only on VPN | Full tunnel without media exclusions |
| Internal app by FQDN fails, works by IP | DNS: split tunnel without internal DNS over VPN (see NRPT) |
| Internal subnet unreachable on split tunnel | That route isn't in the split include list; home LAN uses the same subnet (e.g. 192.168.1.0/24 overlap) |
| Websites blocked/slow on VPN | Full tunnel through the corporate proxy/SWG |

## Check what the client actually does
- Windows: `route print` (VPN interface routes; `0.0.0.0/0` via VPN = full tunnel),
  `Get-NetRoute -InterfaceAlias "<VPN adapter>"`; `Find-NetRoute -RemoteIPAddress 10.20.30.40`
  shows the interface chosen for a destination.
- `tracert -d <host>`: first hop the VPN gateway vs home router.
- macOS: `netstat -rn`, `route get 10.20.30.40`.
- Always On VPN profile: `Get-VpnConnection` (SplitTunneling True/False) or the ProfileXML
  routes.

## Overlapping subnets
Home routers on 10.0.0.0/24 or 192.168.0.0/24 clash with corporate ranges. Split tunnel
routes more specific than the home LAN win, but resources in the overlapping range on
the local side become unreachable. Long term: avoid common home ranges in corporate
addressing; short term: user changes the home router LAN range.

## Gotchas
- Security teams may require full tunnel for compliance; changes go through security.
- Excluding by FQDN on clients that only support IPs silently does nothing.

## Verify
`Find-NetRoute` for an internal IP returns the VPN interface and for a Teams media IP returns
the physical interface (in force-tunnel-with-exclusions), and Teams call quality improves.
