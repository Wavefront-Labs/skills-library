---
id: computing-software.cloud-infrastructure-engineering.metallb.bgp-peer-and-advertisement
name: bgp-peer-and-advertisement
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, bgppeer, bgpadvertisement, asn, myasn, peerasn, peeraddress, v1beta2]
level: practitioner
status: docs-checked
description: "Basic MetalLB BGP setup: one BGPPeer per router (myASN, peerASN, peerAddress), a pool, and a BGPAdvertisement; note BGPPeer v1beta1 is deprecated in favour of v1beta2."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGPPeer and BGPAdvertisement

Create one `BGPPeer` for each router. A basic setup needs: router IP, router AS number, the AS number MetalLB uses, and an address range.

```yaml
apiVersion: metallb.io/v1beta2
kind: BGPPeer
metadata:
  name: sample
  namespace: metallb-system
spec:
  myASN: 64500
  peerASN: 64501
  peerAddress: 10.0.0.1
```
BGPPeer `v1beta1` is deprecated; use `v1beta2`.

Then advertise a pool:
```yaml
apiVersion: metallb.io/v1beta1
kind: BGPAdvertisement
metadata:
  name: example
  namespace: metallb-system
spec:
  ipAddressPools:
  - first-pool
```
- No pool selector means all pools. For specialized pools list `ipAddressPools` (or use a label selector).
- MetalLB must be configured through a `BGPAdvertisement` to advertise the IPs of a pool via BGP.
- Default advertisement: a /32 per service IP, localpref 0, no communities (`computing-software.cloud-infrastructure-engineering.metallb.bgp-aggregation-and-communities`).

Session state metric: `metallb_bgp_session_up` (1 is up, 0 is down); in FRR-K8s mode it is `frrk8s_bgp_session_up`. See `computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-bgp-session`.

## Checked
2026-11-04. Confirmed against the MetalLB "Configuration" page (BGP section, v1beta1 deprecation note, pool selector behaviour), the Advanced BGP page (default /32, localpref zero) and the Prometheus Metrics page (session metrics and prefixes). Removed an unsupported definition of advertising.
Method: documentation only; no commands were run.
