---
id: computing-software.cloud-infrastructure-engineering.aws.global-accelerator-dual-stack-accelerators
name: global-accelerator-dual-stack-accelerators
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, global-accelerator, dual-stack-accelerator, ipv6, static-anycast-ips]
level: advanced
status: gated
description: "Create dual-stack Global Accelerators with static IPv4 and IPv6 anycast addresses, and meet the dual-stack endpoint requirements."
sources: ["https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoints.html", "https://docs.aws.amazon.com/global-accelerator/latest/dg/disaster-recovery-resiliency.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dual-stack accelerators

## 1. Create
```bash
aws globalaccelerator create-accelerator --region us-west-2 --name web-ds --ip-address-type DUAL_STACK
aws globalaccelerator describe-accelerator --region us-west-2 --accelerator-arn <ARN> \
  --query 'Accelerator.IpSets[].{family:IpAddressFamily,ips:IpAddresses}'
```
`--region us-west-2` for Global Accelerator calls: (gated: unconfirmed, source is paywalled or blocked).
A dual-stack accelerator gets four static IP addresses: two IPv4 and two IPv6, one per network zone.
Converting an existing IPv4 accelerator: `update-accelerator --ip-address-type DUAL_STACK`.

## 2. Endpoint requirements
- Add only endpoints that support dual-stack. Network Load Balancers, Application Load Balancers and EC2
  instances can be added as dual-stack endpoints.
- A resource must be valid and active when you add it as an endpoint.

## Verify
- [ ] `describe-accelerator` shows IPv4 and IPv6 address families in `IpSets`.
- [ ] Endpoints in each endpoint group report healthy.

## Checked
2026-10-28: Confirmed against the Global Accelerator Developer Guide pages about-endpoints (dual-stack endpoint rule: NLB, ALB and EC2 can be dual-stack) and disaster-recovery-resiliency (two IPv4 plus two IPv6 addresses for dual-stack, one per network zone), and botocore (IpAddressType IPV4/DUAL_STACK, IpAddressFamily). The original sources were empty stubs and were replaced. Read end to end. Gated: the us-west-2 control-plane Region. Removed as unconfirmed: DualStackDnsName, IPv6 CIDR subnet requirement, custom routing IPv4-only claim, DNS A/AAAA advice, client IP and WAF notes, curl checks.

Method: documentation only; no commands were run.
