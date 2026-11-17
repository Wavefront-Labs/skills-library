---
id: computing-software.cloud-infrastructure-engineering.metallb.ip-sharing
name: ip-sharing
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, allow-shared-ip, sharing-key, loadbalancerip, ip-sharing, tcp-udp, dns]
level: practitioner
status: docs-checked
description: "Let several LoadBalancer Services share one IP with the metallb.io/allow-shared-ip annotation: sharing key, distinct ports, traffic policy rules and L2 serviceSelectors conflict."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/usage/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IP address sharing

By default Services never share IPs. Opt in with the annotation `metallb.io/allow-shared-ip`; its value is the sharing key.

Services can share an IP when:
- they have the same sharing key,
- they request different ports (e.g. tcp/80 and tcp/443),
- both use the `Cluster` external traffic policy, or both point to the exact same set of pods (identical selectors).

MetalLB may colocate them but need not. To force a specific shared address, also set `spec.loadBalancerIP`.

Example (TCP and UDP DNS on one IP):
```yaml
metadata:
  name: dns-service-tcp
  annotations:
    metallb.io/allow-shared-ip: "key-to-share-1.2.3.4"
spec:
  type: LoadBalancer
  loadBalancerIP: 1.2.3.4
  ports:
    - name: dnstcp
      protocol: TCP
      port: 53
      targetPort: 53
  selector:
    app: dns
```
The second Service (`dns-service-udp`) is identical except for name, `protocol: UDP` and port name `dnsudp`.

Reasons: work around a Kubernetes limitation (the page does not name it; the TCP and UDP DNS example illustrates it) or work with limited IP addresses.

Warning: in L2 mode `allow-shared-ip` is incompatible with `serviceSelectors` on L2Advertisements; such Services are not announced (`computing-software.cloud-infrastructure-engineering.metallb.l2-service-selectors`).

If a Service that asks for an IP used by other services does not get it, recheck these sharing conditions (`computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-ip-assignment`).

## Checked

2026-11-04. Confirmed against the MetalLB Usage page (IP address sharing section: annotation, three sharing conditions, may-colocate wording, DNS example, L2 serviceSelectors warning) and the Troubleshooting page (sharing properties). Replaced an unsupported "mixed protocols" explanation of the Kubernetes limitation.

Method: documentation only; no commands were run.
