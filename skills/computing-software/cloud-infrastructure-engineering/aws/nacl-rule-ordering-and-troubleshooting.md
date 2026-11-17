---
id: computing-software.cloud-infrastructure-engineering.aws.nacl-rule-ordering-and-troubleshooting
name: nacl-rule-ordering-and-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, network-acl, nacl-rule-number, nacl-ordering, nacl-troubleshooting, ephemeral-ports, flow-logs]
level: practitioner
status: docs-checked
description: "Write network ACLs that work: rule numbering and first-match order, ephemeral return ports, deny-lists, subnet association, and diagnosing NACL drops with flow logs."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html", "https://docs.aws.amazon.com/vpc/latest/userguide/nacl-rules.html", "https://docs.aws.amazon.com/vpc/latest/userguide/custom-network-acl.html", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-records-examples.html", "https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network ACLs: ordering and troubleshooting

## 1. Evaluation
- Stateless, per subnet, evaluated when traffic enters and leaves the subnet (not as it is routed within a subnet).
- Rules are numbered 1 to 32766 and evaluated in **ascending rule number**; the first match wins (allow or deny);
  the `*` rule (a final deny) catches the rest.
- Each subnet is associated with exactly one NACL (the default NACL if you do not choose one), and one NACL can serve several subnets. The default NACL allows all traffic in and out; a custom NACL
  has only the `*` deny rules until you add rules.
- Quotas (VPC quotas page, read 2026-10-27): 200 network ACLs per VPC and 20 rules per network ACL as the default for each direction,
  adjustable up to 40 inbound and 40 outbound rules, with a documented risk of reduced network performance.

## 2. Numbering scheme
Leave gaps so you can insert rules later:
```
Inbound
  90   DENY  tcp 22     198.51.100.0/24   (known-bad, block before allows)
  100  ALLOW tcp 443    0.0.0.0/0
  110  ALLOW tcp 80     0.0.0.0/0
  200  ALLOW tcp 1024-65535  0.0.0.0/0     (return traffic for outbound connections)
  300  ALLOW all        10.20.0.0/16       (intra-VPC)
  *    DENY  all
Outbound
  100  ALLOW tcp 443    0.0.0.0/0
  200  ALLOW tcp 1024-65535  0.0.0.0/0     (responses to inbound clients)
  300  ALLOW all        10.20.0.0/16
  *    DENY  all
```
Deny rules must have **lower numbers** than the allows they override.

## 3. Ephemeral ports
Responses go to the client's ephemeral port. Ranges per AWS: many Linux kernels (including Amazon Linux) 32768-61000, Windows Server 2008 and later
49152-65535, NAT gateway 1024-65535, Elastic Load Balancing 1024-65535, Lambda 1024-65535. Safe default:
allow `1024-65535` for return traffic in both directions. Forgetting the outbound
ephemeral rule on a web subnet is the classic "SG allows 443 but connections hang".

## 4. Commands
```bash
aws ec2 create-network-acl-entry --network-acl-id acl-0abc --ingress --rule-number 90 \
  --protocol tcp --port-range From=22,To=22 --cidr-block 198.51.100.0/24 --rule-action deny
aws ec2 replace-network-acl-entry ...   # change a rule in place (same number)
aws ec2 replace-network-acl-association --association-id aclassoc-... --network-acl-id acl-0new
aws ec2 describe-network-acls --filters Name=association.subnet-id,Values=subnet-0abc
```
Protocol numbers: `-1` all, `6` TCP, `17` UDP, `1` ICMP (needs `--icmp-type-code`).
IPv6 rules are separate entries (`--ipv6-cidr-block`).

## 5. Troubleshooting with flow logs
Both NACL and security group drops show as `REJECT` in flow logs. Distinguish them:
- A security group that denies the inbound request gives a single `REJECT` record.
- NACL problem signature: the request is `ACCEPT` (allowed by both) but the response is `REJECT`, because the
  NACL is stateless and has no rule for the reply (AWS's ping example: NACL allows inbound ICMP but not outbound).
Logs Insights:
```
fields @timestamp, srcAddr, srcPort, dstAddr, dstPort, action
| filter interfaceId = "eni-0abc" and action = "REJECT"
| sort @timestamp desc | limit 50
```
Reachability Analyzer is a static configuration analysis tool that identifies the blocking component, for example missing or misconfigured NACL rules.

## 6. When to use NACLs at all
- Subnet-wide **deny** of specific CIDRs (attack sources) quickly; SGs cannot deny.
- Coarse tier isolation (isolated data subnets accept only from app subnets).
Do not replicate SG logic in NACLs; it doubles the debugging surface.

## Gotchas
- Default NACL associations: new subnets join the default NACL. If the default is
  locked down, new subnets break; if it is open, custom intent is lost. Associate explicitly
  in IaC.
- NACLs do not filter traffic to and from the Route 53 Resolver (VPC+2), DHCP, instance metadata, ECS task metadata endpoints, Windows license activation, Amazon Time Sync or the reserved router addresses; you cannot block those with NACLs.
- Rule changes apply after a short period and are easy to typo; peer review numbers. If you delete rules and add more new entries than the quota allows in one request, the deletions happen and the additions do not.

## Verify
- [ ] Each subnet's NACL association is explicit in IaC.
- [ ] Ephemeral return ranges allowed in both directions where clients/servers live.
- [ ] Reachability Analyzer path from ALB to app instance on the app port shows reachable.
- [ ] Flow logs show no unexpected REJECT pairs after changes.

## Checked

Checked 2026-10-27 against the Amazon VPC User Guide (Network ACLs, rules, default and custom NACLs, flow log examples, VPC quotas) and the botocore EC2 model.
- Rule numbering (1 to 32766), ascending first-match, statelessness, one NACL per subnet, default NACL behaviour and the not-filtered traffic list confirmed.
- Quotas: 200 NACLs per VPC, 20 rules per NACL adjustable to 40 inbound and 40 outbound with a performance warning, read on the quotas page.
- Ephemeral ranges confirmed on the custom NACL page (Linux range is 32768-61000, not 60999). The flow log request/response REJECT pattern and single REJECT for a security group denial confirmed on the flow log examples page.
- `create-network-acl-entry`, `replace-network-acl-association` options confirmed in the service model.
- Removed the claim that SG rule removal does not kill tracked flows (not on a page read).

Method: documentation only; no commands were run.
