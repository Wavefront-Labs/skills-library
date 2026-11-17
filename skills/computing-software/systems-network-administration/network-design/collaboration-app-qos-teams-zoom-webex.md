---
id: computing-software.systems-network-administration.network-design.collaboration-app-qos-teams-zoom-webex
name: collaboration-app-qos-teams-zoom-webex
category: computing-software
field: systems-network-administration
product: network-design
tags: [qos-design, teams-qos, collaboration-qos, zoom, webex, dscp, gpo-qos, media-ports]
level: practitioner
status: docs-checked
description: "Prioritise Teams, Zoom and Webex media: vendor port ranges, marking at the endpoint via GPO/Intune or by port ACLs at the access edge, network requirements, and verification."
sources:
  - https://learn.microsoft.com/en-us/microsoftteams/qos-in-teams
  - https://learn.microsoft.com/en-us/microsoftteams/prepare-network
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# QoS for Teams, Zoom and Webex

## Network targets (Microsoft guidance, client to Microsoft edge)
Take the current latency, jitter and packet-loss targets from Microsoft's Teams network
preparation page. QoS helps on congested LAN/WAN links you control; it cannot fix the internet.

## Teams
Media source ports (client-side) and DSCP values from Microsoft's QoS-in-Teams page:
| Media | Source ports | DSCP |
|---|---|---|
| Audio | 50000-50019 | EF (46) |
| Video | 50020-50039 | AF41 (34) |
| App/screen sharing | 50040-50059 | AF21 (18) |
Mark on Windows with a GPO policy-based QoS rule per media type (application name `ms-teams.exe`
for new Teams, source port range, DSCP value). Mac and mobile clients use hard-coded DSCP values
for audio (EF) and video and sharing (AF41), not configurable.

## Zoom
Take Zoom and Webex media port ranges and DSCP defaults from each vendor's current network
requirements page; they change between releases and are not reproduced here.

## Network side
- Trust DSCP from managed endpoints on access ports (or re-mark by port/ACL if endpoints are not
  trusted):
```
ip access-list extended TEAMS-AUDIO
 permit udp any range 50000 50019 any
class-map match-any TEAMS-AUDIO
 match access-group name TEAMS-AUDIO
policy-map ACCESS-IN
 class TEAMS-AUDIO
  set dscp ef
```
- Queue EF in LLQ and AF41 in a video queue on congested links (WAN edge, Wi-Fi WMM mapping).
- Keep media off VPN tunnels (split tunnel the vendor media ranges).

## Verify
- [ ] Wireshark on a client shows DSCP 46 on Teams audio packets leaving and still marked at the WAN
  edge; Teams call analytics show low jitter/loss.

## Checked

- Date: 2026-10-28
- Confirmed: the Teams audio, video and sharing source port ranges with DSCP EF, AF41, AF21 and the ms-teams.exe name (qos-in-teams); Mac and mobile hard-coded DSCP.
- Removed: latency, jitter and loss figures and the 15 s window (not on the fetched page), UDP 3478-3481 and the Teams admin center toggle, Windows/Intune marking claims, all Zoom and Webex ports and DSCP defaults (Zoom page unreadable).

Method: documentation only; no commands were run.
