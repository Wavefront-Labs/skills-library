---
id: computing-software.systems-network-administration.network-design.qos-across-the-internet-dscp-bleaching
name: qos-across-the-internet-dscp-bleaching
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, qos-design, dscp-bleaching, internet-qos, dscp-remarking, sd-wan-qos]
level: practitioner
status: docs-checked
description: "Plan QoS when traffic crosses the internet: DSCP is often re-marked or ignored, so control the edge (shaping, egress queuing), carry markings inside tunnels, and remark on entry."
sources:
  - https://www.rfc-editor.org/rfc/rfc8100
  - https://www.rfc-editor.org/rfc/rfc2983
  - https://datatracker.ietf.org/doc/html/draft-ietf-tsvwg-dscp-considerations
  - https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/qos/ios-xe-17/qos-book-xe.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# QoS across the internet and DSCP bleaching

## Reality
- DSCP is often re-marked along internet paths (the IETF tsvwg DSCP-considerations draft
  describes commonly observed re-marking), so do not rely on it end to end. RFC 8100 describes
  Diffserv classes and practice at provider interconnects.
- So QoS over the internet only works where **you** control the queue: your edge egress, and the
  remote edge for the other direction.

## What to do
1. **Shape egress** slightly below the circuit's real upstream rate so the queue forms in
   your router with your priority policy, not in the ISP's CPE.
2. **Ingress**: you cannot queue what has already crossed the bottleneck; options are shaping on the
   inbound interface to induce TCP back-off (approximate), or SD-WAN/remote edge shaping toward you.
3. Inside **IPsec/GRE/SD-WAN tunnels**, decide how the inner DSCP maps to the outer header
   (RFC 2983 describes the tunnel models) so your own devices queue correctly; the outer marking
   may be changed in transit, but the inner header is preserved to the far end.
4. **Remark on entry** (trust boundary) for traffic from the internet: do not trust external DSCP;
   classify by app/port/IP and set your own values.
5. SD-WAN: per-path SLA measurement and steering plus FEC/duplication for real-time traffic do more
   than markings.

## Diagnosing bleaching
Send traffic with a known DSCP value, capture at both ends and compare the DSCP received.

## Verify
- [ ] Egress shaper and priority queue active on internet edges; captures confirm inner DSCP preserved across tunnels; inbound traffic remarked per policy.

## Checked

- Date: 2026-10-28
- Confirmed: the tsvwg draft covers commonly observed DSCP re-marking along internet paths; RFC 8100 is Diffserv interconnection classes and practice; RFC 2983 covers Diffserv and tunnels.
- Removed: the claim that ISPs reset DSCP to 0, the 95 percent shaping figure, qos pre-classify and the IPsec ToS-copy default, ping -Q, iperf3 --dscp and the Wireshark field name.

Method: documentation only; no commands were run.
