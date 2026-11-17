---
id: computing-software.cloud-infrastructure-engineering.aws.vpc-lattice-service-networks
name: vpc-lattice-service-networks
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc-lattice, lattice, service-network, service-to-service, auth-policy, sigv4, cross-account]
level: practitioner
status: docs-checked
description: "Connect services across VPCs and accounts with VPC Lattice: service networks, listeners, target groups, SigV4 auth policies, and when to pick it over PrivateLink or TGW."
sources: ["https://docs.aws.amazon.com/vpc-lattice/latest/ug/what-is-vpc-lattice.html", "https://docs.aws.amazon.com/vpc-lattice/latest/ug/auth-policies.html", "https://docs.aws.amazon.com/vpc-lattice/latest/ug/service-networks.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC Lattice service networks

**Goal:** service-to-service HTTP/gRPC/TCP connectivity across VPCs and accounts with
IAM-based auth, without peering, TGW routes or overlapping-CIDR worries.

## 1. Building blocks
- **Service**: DNS name + listeners (HTTP/HTTPS/TLS passthrough) + rules → **target groups**
  (instances, IPs, Lambda, ALB, ECS/EKS via controller).
- **Service network**: logical grouping; services are *associated*, VPCs are *associated*
  (consumers). Any client in an associated VPC can reach any associated service, subject to
  auth policy and security groups.
- **Resource configurations** (TCP to databases etc.) can also be shared through a service network.
- Services and service networks can be shared with other accounts (AWS RAM).

```bash
SN=$(aws vpc-lattice create-service-network --name prod --auth-type AWS_IAM --query id --output text)
SVC=$(aws vpc-lattice create-service --name orders --auth-type AWS_IAM --query id --output text)
aws vpc-lattice create-service-network-service-association --service-network-identifier $SN --service-identifier $SVC
aws vpc-lattice create-service-network-vpc-association --service-network-identifier $SN \
  --vpc-identifier vpc-consumer --security-group-ids sg-allow-lattice
```

## 2. Auth policies (IAM, both levels)
```json
{"Version": "2012-10-17", "Statement": [{
  "Effect": "Allow",
  "Principal": {"AWS": "arn:aws:iam::<ACCOUNT_ID>:role/checkout-task"},
  "Action": "vpc-lattice-svcs:Invoke",
  "Resource": "arn:aws:vpc-lattice:<REGION>:<ACCOUNT_ID>:service/svc-123/*",
  "Condition": {"StringEquals": {"vpc-lattice-svcs:RequestMethod": "GET"}}}]}
```
Clients must **SigV4-sign** requests (signing service name `vpc-lattice-svcs`) when auth type is
`AWS_IAM`. Auth type `NONE` turns access control off. Policies attach at the service network and at the service.

## 3. Networking details
- Lattice traffic uses link-local and non-routable addresses listed in the managed prefix lists
  `com.amazonaws.<REGION>.vpc-lattice` (IPv4) and `com.amazonaws.<REGION>.ipv6.vpc-lattice` (IPv6);
  reference them in the consumer's outbound rules (if custom) and the target's inbound rules.
- Overlapping CIDRs between consumer and provider VPCs are fine.
- Access logs to CloudWatch Logs/S3/Firehose on the service network and service.

## 4. When to choose
| Need | Choice |
|---|---|
| Many app services, IAM auth, L7 routing, cross-account | VPC Lattice |
| Expose one service to many consumers (incl. other orgs), TCP | PrivateLink endpoint service |
| Full IP routing between networks, on-prem, appliances | Transit Gateway / Cloud WAN |

## Gotchas
- Check the VPC Lattice pricing page before modelling high-volume paths against Transit Gateway.
- A VPC can associate with only one service network directly (use service network endpoints for more).
- Targets' security groups must allow the Lattice prefix list on the listener ports.

## Verify
- [ ] From a consumer task: a SigV4-signed request (service name `vpc-lattice-svcs`) to the service DNS succeeds; an unsigned one is denied.
- [ ] Access logs show the caller principal and target.
- [ ] A VPC not associated with the network cannot resolve/reach the service.

## Checked
2026-10-31. Confirmed against the VPC Lattice User Guide (service networks, auth policies, security groups, SigV4-authenticated requests): one direct VPC-to-service-network association (use service-network endpoints for more), `--auth-type AWS_IAM` or `NONE`, `vpc-lattice-svcs:Invoke`, `vpc-lattice-svcs:RequestMethod`, `vpc-lattice` ARN format, signing name `vpc-lattice-svcs`, managed prefix list names, 169.254.171.0/24 link-local range. Removed: fd00:ec2:80::/64, the 403 status claim, the PrincipalOrgID advice and the per-request charge description (not confirmed). CLI commands passed check_commands.py.
Method: documentation only; no commands were run.
