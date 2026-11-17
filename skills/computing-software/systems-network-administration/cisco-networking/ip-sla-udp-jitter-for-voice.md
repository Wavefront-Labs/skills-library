---
id: computing-software.systems-network-administration.cisco-networking.ip-sla-udp-jitter-for-voice
name: ip-sla-udp-jitter-for-voice
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, ip-sla, udp-jitter, voip-monitoring, mos, ip-sla-responder, jitter, packet-loss, codec-g711]
level: practitioner
status: draft
description: "Measure voice-path quality with IP SLA udp-jitter: responder setup, codec-based operations with MOS/ICPIF, one-way delay with NTP, thresholds and SNMP."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipsla/configuration/xe-16/sla-xe-16-book/sla-udp-jitter.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipsla/configuration/xe-16/sla-xe-16-book/sla-voip-mos.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IP SLA udp-jitter for voice paths

## Responder (far end)
```
ip sla responder
```
The responder timestamps packets, removing its processing time from results. Permit UDP 1967
(control) and the chosen test port through firewalls.

## Codec-based operation (sender)
```
ip sla 10
 udp-jitter 10.20.0.1 16384 codec g711alaw codec-numpackets 1000 codec-interval 20
 tos 184                                   ! DSCP EF (46 << 2)
 frequency 300
 tag VOICE-SITE20
ip sla schedule 10 life forever start-time now
```
Non-codec form: `udp-jitter 10.20.0.1 16384 num-packets 100 interval 20`.

## Reading results
```
show ip sla statistics 10 details
  Voice Scores: ICPIF: 1  MOS score: 4.34
  RTT Values: Min/Avg/Max 18/21/35 ms
  Packet Loss Values: Loss Source->Destination 0, Destination->Source 0
  Jitter Time: Source to Destination Jitter Min/Avg/Max 0/1/6 ms
  One Way Latency Min/Avg/Max ...         ! needs NTP sync on both ends, else 'Precision' not accurate
```
Voice targets (ITU-T G.114 and common practice): one-way delay < 150 ms, jitter < 30 ms, loss < 1%, MOS > 4.0.

## Alerting
```
ip sla reaction-configuration 10 react jitterAvg threshold-value 30 20 threshold-type consecutive 3 action-type trapOnly
ip sla reaction-configuration 10 react mos threshold-value 380 350 threshold-type immediate action-type trapOnly
ip sla logging traps
snmp-server enable traps ipsla
```
MOS thresholds are in hundredths (380 = 3.80).

## Gotchas
- TOS must be set or you measure best-effort, not the voice queue.
- Source interface (`source-ip`) to test the right path in multi-WAN routers.
- High frequency x many probes loads small routers; stagger start times.
- Results from software-based timestamps on busy CPUs can show false jitter; use hardware
  timestamping platforms or responder on dedicated devices for accuracy.

## Verify
- [ ] `show ip sla summary` OK; MOS/jitter in range; traps arrive when a test link is congested.
