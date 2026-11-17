---
id: computing-software.systems-network-administration.cisco-networking.wireless-client-radioactive-trace
name: wireless-client-radioactive-trace
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst-9800, wlc, radioactive-trace, wireless-client-troubleshooting, client-delete-reason, always-on-tracing]
level: practitioner
status: draft
description: "Troubleshoot a wireless client on a Catalyst 9800 WLC: client state and delete reasons, always-on traces, RadioActive tracing by MAC, and decoding the join phases."
sources:
  - https://www.cisco.com/c/en/us/support/docs/wireless/catalyst-9800-series-wireless-controllers/213949-wireless-debugging-and-log-collection-on.html
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/17-9/config-guide/b_wl_17_9_cg.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wireless client troubleshooting with RadioActive tracing

## Where is the client now?
```
show wireless client mac-address aaaa.bbbb.cccc detail
!  Client State: Associated / L2 auth / Webauth pending / IP learn / Run
!  Policy Manager State: RUN
!  AP Name, WLAN, VLAN, Session timeout, RSSI, SNR
show wireless client summary
show wireless stats client delete reasons
```
States progress: Associated -> L2 Authentication (802.1X/PSK) -> Mobility -> IP Learn -> Webauth
(if any) -> Run. The state where it stalls tells you what to look at.

| Stalls at | Look at |
|---|---|
| L2 auth | RADIUS reachability, cert trust on client, wrong PSK (EAPOL key timeout) |
| IP learn | DHCP scope, VLAN on the policy profile, trunk to WLC/AP (FlexConnect local switching) |
| Webauth pending | redirect ACL, DNS for the portal, HTTPS interception on client |
| Deletes with `CO_CLIENT_DELETE_REASON_*` | idle timeout, session timeout, roam, AP disassoc |

## Always-on traces (already running)
```
show logging profile wireless filter mac aaaa.bbbb.cccc to-file bootflash:client.txt
show logging profile wireless start last 30 minutes filter mac aaaa.bbbb.cccc
```
Good for "it failed ten minutes ago": the controller keeps notice-level logs per client.

## RadioActive trace (debug-level for one MAC)
GUI: Troubleshooting > RadioActive Trace > add MAC > Start, reproduce, Generate (last 10 min),
download. CLI:
```
debug wireless mac aaaa.bbbb.cccc monitor-time 600
! reproduce
no debug wireless mac aaaa.bbbb.cccc
dir bootflash: | include ra_trace
more bootflash:ra_trace_MAC_aaaabbbbcccc_*.log
```
Only that client's events are logged at debug level, so it is safe on a production controller.
Add `internal` keyword only when TAC asks; it is far more verbose.

## Reading it
Search for `S_CO_` state transitions, `EAP`, `DOT1X`, `DHCP`, `IP-LEARN` and `delete reason`.
Pair with an over-the-air capture or the AP's client trace if the controller never sees the
association (problem is RF or the client).

## Gotchas
- Randomised MAC addresses (iOS/Android private address per SSID) mean the MAC you are tracing
  may change; ask the user to disable private address for the SSID while testing.
- FlexConnect local switching: DHCP happens at the AP; check the AP's VLAN trunk, not the WLC.
- Clock must be right (NTP) to correlate with RADIUS logs.

## Verify
- [ ] Client reaches Run with the expected VLAN and policy.
- [ ] Trace files attached to the ticket with the reproduce time noted.
