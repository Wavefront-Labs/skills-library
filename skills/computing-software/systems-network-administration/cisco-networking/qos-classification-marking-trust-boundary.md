---
id: computing-software.systems-network-administration.cisco-networking.qos-classification-marking-trust-boundary
name: qos-classification-marking-trust-boundary
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, qos, quality-of-service, dscp, qos-marking, classification, trust-boundary, qos-trust, nbar, set-dscp, cos, ip-phone-trust, conditional-trust, trust-device-cisco-phone, ingress-marking]
level: practitioner
status: draft
description: "Classify and mark traffic at the edge: where the trust boundary sits, trusting phones conditionally, re-marking untrusted hosts, NBAR-based classification, DSCP vs CoS on Catalyst."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/qos/b_179_qos_9300_cg/configuring_qos.html
  - https://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/WAN_and_MAN/QoS_SRND/QoS-SRND-Book/QoSIntro.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Classification, marking and the trust boundary

## Principles
- Classify and mark **as close to the source as possible**, once; everything upstream queues
  on DSCP.
- The **trust boundary** is the point where you start believing markings. Hosts can set any
  DSCP they like, so a user PC marking all traffic EF would get priority treatment unless the
  access switch re-marks it.
- Layer 2 CoS (3 bits in 802.1Q) exists only on trunks; DSCP (6 bits in IP header) survives
  routing. Use DSCP.

## Catalyst 9000 behaviour
On C9K, ports **trust DSCP by default** (unlike older Catalysts where `mls qos` made everything
untrusted). So you must explicitly re-mark untrusted ports.

## Access port with a Cisco phone (conditional trust)
```
interface Gi1/0/10
 switchport access vlan 10
 switchport voice vlan 110
 trust device cisco-phone           ! trust markings only while CDP sees a Cisco phone
 service-policy input MARK-ACCESS
```

## Re-mark untrusted endpoints with an ingress policy
```
class-map match-any VOICE-MEDIA
 match protocol rtp audio                ! NBAR; or ACL matching softphone ports
class-map match-any COLLAB-SIGNALING
 match protocol sip
policy-map MARK-ACCESS
 class VOICE-MEDIA
  set dscp ef
 class COLLAB-SIGNALING
  set dscp cs3
 class class-default
  set dscp default                       ! everything else to 0
```
NBAR (`match protocol`) costs CPU/ASIC resources and is platform-dependent; ACLs on
known ports (e.g. Teams media UDP 50000-50059) are cheaper and predictable.

## Servers and WAN
- Trust DSCP from known servers (call managers, media servers) on server ports.
- At the WAN edge, re-mark or trust per the provider's class model (often 4-6 classes mapped
  from your DSCP plan).
- Internet traffic arrives with arbitrary DSCP: reset to 0 at the edge.

## Verify
```
show policy-map interface Gi1/0/10 input
show platform software fed switch active qos interface Gi1/0/10    ! C9K: trust state
```
Wireshark on an uplink SPAN: `ip.dsfield.dscp == 46` should only show voice RTP.
- [ ] Phone ports trust only with phone present; PC traffic remarked to 0.
- [ ] Uplinks trust DSCP; WAN edge marking matches provider classes.
