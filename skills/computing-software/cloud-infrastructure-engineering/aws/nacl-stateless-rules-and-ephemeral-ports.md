---
id: computing-software.cloud-infrastructure-engineering.aws.nacl-stateless-rules-and-ephemeral-ports
name: nacl-stateless-rules-and-ephemeral-ports
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, nacl, network-acl, stateless-rules, stateful-rules, ephemeral-ports, security-groups, subnet-security]
level: practitioner
status: docs-checked
description: "Write network ACLs that do not break return traffic: stateless vs stateful filtering, ephemeral port ranges per client OS, rule numbering, and when NACLs are worth using."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html", "https://docs.aws.amazon.com/vpc/latest/userguide/custom-network-acl.html", "https://docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html", "https://docs.aws.amazon.com/vpc/latest/userguide/path_mtu_discovery.html", "https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NACLs: stateless rules and ephemeral ports

## 1. Stateful vs stateless
| | Security group | Network ACL |
|---|---|---|
| Level | instance (network interface) | subnet |
| State | **stateful**: return traffic allowed automatically | **stateless**: return traffic needs its own rule |
| Rules | allow only; all rules evaluated before deciding | allow and deny, evaluated in ascending rule number, first match wins |
| Default | n/a | default NACL allows all; a custom NACL denies everything until you add rules |

Use SGs for application access control. Use NACLs for coarse subnet guardrails: explicit
**deny** of a malicious CIDR, blocking a whole subnet tier from another, compliance
"defence in depth".

## 2. Ephemeral ports — the classic outage
A client connects from a random high port; the server's reply goes back to that port. With a
custom NACL you must allow the reply direction:
- Many Linux kernels (including Amazon Linux): 32768–61000; Windows Server 2008 and later: 49152–65535; NAT gateways,
  Lambda and Elastic Load Balancing: 1024–65535. For public-facing instances AWS says you can open **1024–65535** and add deny rules for malicious ports, placed earlier in the table.

Public web subnet NACL:
```
Inbound
 100 TCP 443        0.0.0.0/0      ALLOW   # clients to ALB
 110 TCP 1024-65535 0.0.0.0/0      ALLOW   # replies to outbound calls (e.g. ALB->targets, NAT)
 *   ALL            0.0.0.0/0      DENY
Outbound
 100 TCP 1024-65535 0.0.0.0/0      ALLOW   # replies to clients
 110 TCP 8080       10.0.16.0/20   ALLOW   # ALB to app subnets
 *   ALL            0.0.0.0/0      DENY
```
```bash
aws ec2 create-network-acl-entry --network-acl-id acl-123 --ingress --rule-number 110 \
  --protocol tcp --port-range From=1024,To=65535 --cidr-block 0.0.0.0/0 --rule-action allow
```

## 3. Rule numbering
Leave gaps (100, 110, 120) and put specific **deny** rules at low numbers (e.g. 50) so they
evaluate before broad allows. Quota: 20 rules per network ACL for each direction by default, adjustable up to 40 (VPC quotas page, read 2026-10-27).

## Gotchas
- Path MTU Discovery needs an inbound rule for ICMP type 3, code 4 (Destination Unreachable, fragmentation needed); without it large transfers can hang.
- NACL rules are evaluated when traffic enters or leaves the subnet, not for traffic routed within a subnet.
- NACLs do not filter traffic to and from the Amazon DNS resolver, DHCP, instance metadata, Windows license activation or Amazon Time Sync.
- A deny rule for 0.0.0.0/0 or the subnet CIDR on a backend subnet stops a load balancer's health checks.

## Verify
- [ ] Reachability Analyzer shows the path allowed and names the NACL rules evaluated.
- [ ] Flow logs show no `REJECT` on return traffic (destination port in 1024–65535) after the change.
- [ ] A blocked CIDR is rejected at the NACL (`REJECT` in flow logs) while others pass.

## Checked

Checked 2026-10-27 against the Amazon VPC User Guide (Network ACLs, rules, custom NACLs and ephemeral ports, Path MTU Discovery, infrastructure security comparison table, VPC quotas) and the botocore EC2 model.
- The security group versus NACL table (level, rule type, evaluation, return traffic) and the default NACL behaviour confirmed.
- Ephemeral ranges confirmed on the custom NACL page; the Linux range is 32768-61000. The ICMP type 3 code 4 requirement confirmed on the Path MTU Discovery page.
- Rule quota (20, adjustable to 40) confirmed on the quotas page. The not-filtered traffic list and the load balancer health check warning confirmed.
- Removed the security group "default deny in, allow out" row (not on a page read). The sources entry for ephemeral ports now points to the custom NACL page, replacing a page name that does not exist.

Method: documentation only; no commands were run.
