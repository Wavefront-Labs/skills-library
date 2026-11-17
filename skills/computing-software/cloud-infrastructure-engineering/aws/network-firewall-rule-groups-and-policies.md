---
id: computing-software.cloud-infrastructure-engineering.aws.network-firewall-rule-groups-and-policies
name: network-firewall-rule-groups-and-policies
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, network-firewall, firewall-policy, suricata-rules, stateful-inspection, ips]
level: practitioner
status: draft
description: "Deploy AWS Network Firewall: endpoints and symmetric routing, stateless vs stateful rule groups, strict rule order, Suricata rules, domain lists, managed threat rules and logging."
sources: ["https://docs.aws.amazon.com/network-firewall/latest/developerguide/what-is-aws-network-firewall.html", "https://docs.aws.amazon.com/network-firewall/latest/developerguide/suricata-examples.html", "https://docs.aws.amazon.com/network-firewall/latest/developerguide/rule-evaluation-order.html", "https://docs.aws.amazon.com/network-firewall/latest/developerguide/firewall-logging.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AWS Network Firewall rule groups and policies

## 1. Architecture
- Firewall = one endpoint per AZ in dedicated firewall subnets (a GWLB endpoint under the hood).
- Traffic must be routed **through** the endpoint in both directions (symmetric):
  - Distributed: IGW ingress route table sends public subnet CIDRs → firewall endpoint; public
    subnet routes `0.0.0.0/0` → firewall endpoint; firewall subnet routes `0.0.0.0/0` → IGW.
  - Centralised: inspection VPC behind Transit Gateway with **appliance mode** enabled on the
    inspection VPC attachment.
- Route each AZ to its own AZ's endpoint, or flows break on AZ asymmetry.

## 2. Policy and rule groups
- **Stateless** groups (5-tuple, priority ordered) → actions `pass`, `drop`, `forward to
  stateful`. Default stateless action: **forward to stateful** (`aws:forward_to_sfe`) for
  both full packets and fragments, otherwise stateful rules never see traffic.
- **Stateful** groups: Suricata-compatible rules, domain lists, 5-tuple. Use **strict
  order** with default actions `aws:drop_established` + `aws:alert_established` for
  default-deny egress.

Suricata examples:
```
pass tls $HOME_NET any -> $EXTERNAL_NET 443 (tls.sni; content:".amazonaws.com"; endswith; nocase; flow:to_server; sid:100;)
pass http $HOME_NET any -> $EXTERNAL_NET 80 (http.host; content:"packages.example.org"; endswith; flow:to_server; sid:101;)
drop tcp $HOME_NET any -> $EXTERNAL_NET 22 (msg:"no outbound ssh"; flow:to_server; sid:102;)
```
Set `HOME_NET` rule variable to all VPC CIDRs for centralised deployments (default is only the
inspection VPC CIDR).

## 3. Managed rule groups
AWS managed threat signatures (malware domains, botnet C2, emerging threats) in alert mode
first; switch to drop after a week of reviewing alerts.

## 4. Logging
```bash
aws network-firewall update-logging-configuration --firewall-name egress-fw --logging-configuration \
 '{"LogDestinationConfigs":[{"LogType":"ALERT","LogDestinationType":"CloudWatchLogs","LogDestination":{"logGroup":"/nfw/alert"}},{"LogType":"FLOW","LogDestinationType":"S3","LogDestination":{"bucketName":"nfw-flow-logs"}}]}'
```
Alert logs include `sid` and SNI/host — the evidence for tuning.

## Gotchas
- Capacity of a rule group is fixed at creation; size for growth.
- TLS SNI rules see the hostname, not the URL path; ECH/encrypted SNI defeats them —
  enable TLS inspection configuration if you must inspect content.
- Rule changes are eventually applied (seconds to minutes); test before relying on them.
- Cost: hourly per endpoint per AZ + per GB processed; centralise to share endpoints.

## Verify
- [ ] From a workload: `curl https://s3.<REGION>.amazonaws.com` succeeds, `curl https://example.com` is dropped and appears in alert logs with the default-drop action.
- [ ] Flow logs show traffic traversing the firewall in both directions (no asymmetric drops).
- [ ] `describe-firewall` shows endpoints `READY` in every AZ used.
