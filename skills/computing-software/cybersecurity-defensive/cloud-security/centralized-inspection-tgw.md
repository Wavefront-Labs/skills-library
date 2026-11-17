---
id: computing-software.cybersecurity-defensive.cloud-security.centralized-inspection-tgw
name: centralized-inspection-tgw
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [centralized-inspection, transit-gateway, aws-network-firewall, gateway-load-balancer, appliance-mode, inspection-vpc, cloud-network-security]
level: advanced
status: draft
description: "Build centralised traffic inspection in AWS: inspection VPC with Network Firewall or GWLB appliances, TGW route tables, appliance mode, east-west and egress flows, testing."
sources: ["https://docs.aws.amazon.com/network-firewall/latest/developerguide/arch-two-zone-igw.html", "https://docs.aws.amazon.com/prescriptive-guidance/latest/inline-traffic-inspection-third-party-appliances/welcome.html", "https://docs.aws.amazon.com/vpc/latest/tgw/transit-gateway-appliance-scenario.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Centralised inspection with Transit Gateway

## Topology
- Spoke VPCs attach to the TGW.
- **Inspection VPC** with firewall endpoints (AWS Network Firewall or Gateway Load Balancer endpoints in front of third-party NVAs) in each AZ, TGW attachment subnets, optional NAT gateways for centralised egress.
- Optional egress VPC (or combine with inspection) and ingress VPC with ALB/WAF.

## Routing
| TGW route table | Associated with | Routes |
|---|---|---|
| spoke-rt | spoke attachments | `0.0.0.0/0` -> inspection attachment (no propagation of spokes, so spoke-to-spoke must traverse inspection) |
| firewall-rt | inspection attachment | propagated routes for all spokes (return path) |
In the inspection VPC: TGW subnet route `0.0.0.0/0` -> firewall endpoint in same AZ; firewall subnet routes: spoke CIDRs -> TGW, `0.0.0.0/0` -> NAT.

## Appliance mode
`aws ec2 modify-transit-gateway-vpc-attachment --transit-gateway-attachment-id tgw-attach-insp --options ApplianceModeSupport=enable` - keeps both directions of a flow on the same AZ/firewall (stateful inspection breaks otherwise).

## Policy
Network Firewall: stateful rule groups (Suricata-compatible), domain allow-lists for egress (TLS SNI/HTTP host), strict rule order with default drop; TLS inspection configuration where needed. Log alerts and flows to S3/CloudWatch.

## Gotchas
- Cost: TGW data processing plus firewall endpoint hours and GB processed - inspect what matters (egress, inter-environment) rather than every flow if budget-limited.
- Asymmetric routing when appliance mode is off is the top cause of intermittent drops.
- VPC-to-VPC traffic within the same environment may be left uninspected deliberately; document it.

## Verify
- [ ] Spoke-to-spoke test flow appears in firewall flow logs.
- [ ] Blocked domain from a spoke instance fails at the firewall (alert log).
- [ ] AZ failure test: traffic re-routes to remaining endpoints.
