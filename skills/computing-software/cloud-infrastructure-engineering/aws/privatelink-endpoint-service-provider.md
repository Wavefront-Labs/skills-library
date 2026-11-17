---
id: computing-software.cloud-infrastructure-engineering.aws.privatelink-endpoint-service-provider
name: privatelink-endpoint-service-provider
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, privatelink, endpoint-service, service-provider, acceptance-required, nlb, private-dns-verification, saas, allowed-principals, connection-notifications]
level: practitioner
status: docs-checked
description: "Publish a service over PrivateLink as a provider: NLB/GWLB-backed endpoint services, allowed principals, acceptance, private DNS names, AZ coverage and proxy protocol."
sources: ["https://docs.aws.amazon.com/vpc/latest/privatelink/create-endpoint-service.html", "https://docs.aws.amazon.com/vpc/latest/privatelink/configure-endpoint-service.html", "https://docs.aws.amazon.com/vpc/latest/privatelink/manage-dns-names.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Providing a PrivateLink endpoint service

**Goal:** customers or other teams reach your service from their VPCs through an interface
endpoint — one-way, no routing, overlapping CIDRs irrelevant.

## 1. Create
```bash
SVC=$(aws ec2 create-vpc-endpoint-service-configuration \
  --network-load-balancer-arns "$NLB_ARN" --acceptance-required \
  --private-dns-name api.example.com --supported-ip-address-types ipv4 \
  --query ServiceConfiguration.ServiceId --output text)
aws ec2 modify-vpc-endpoint-service-permissions --service-id $SVC \
  --add-allowed-principals arn:aws:iam::<CONSUMER_ACCOUNT>:root
```
- Backed by a **Network Load Balancer** or a **Gateway Load Balancer** (appliances). An NLB can be
  associated with one endpoint service; a service can use several NLBs.
- By default nobody can connect. Allowed principals are ARNs: account root
  (`arn:aws:iam::<ACCOUNT_ID>:root`), role, user, or `*` (all principals; with automatic acceptance
  the service is effectively public, so rely on acceptance).
- Consumers create an interface endpoint with service name `com.amazonaws.vpce.<REGION>.vpce-svc-...`.
- The service exists in the Region where you create it; enable cross-Region access to serve others.
- For IPv6 requests the NLB must use the dualstack IP address type and the VPC and subnets need IPv6 CIDR blocks.

## 2. Accept connections
```bash
aws ec2 describe-vpc-endpoint-connections --filters Name=service-id,Values=$SVC
aws ec2 accept-vpc-endpoint-connections --service-id $SVC --vpc-endpoint-ids vpce-0123
```
Without `--acceptance-required`, requests are accepted automatically. To be told about accepted or
rejected connections, configure `create-vpc-endpoint-connection-notification`.

## 3. Private DNS name verification
To let consumers use `api.example.com` with private DNS you must prove domain ownership: add the
TXT record (Name and Value from `describe-vpc-endpoint-service-configurations --query
ServiceConfigurations[*].PrivateDnsNameConfiguration`) to your public domain's DNS, then run
`start-vpc-endpoint-service-private-dns-verification` if you do not want to wait. State
(`pendingVerification`, `verified`, `failed`) must reach `verified`; if it later changes, new
connection requests are denied but existing connections are unaffected.

## 4. AZ coverage
The service is available in the Availability Zones enabled on its load balancer. Give consumers
the service name and supported AZs, and make the service available in at least two AZs for latency
and fault tolerance. If you enable another AZ on the load balancer, then enable the endpoint
service for it too (allow a few minutes first); consumers can then add a subnet from that AZ.

## 5. Knowing who is calling
The source IPs your application sees are the private IPs of the load balancer nodes, not the
consumers. Enable **proxy protocol** on the load balancer: the header carries the consumer's address
and the interface endpoint ID, which you can map to a tenant.

## Gotchas
- Removing a principal does not affect connections already accepted.
- If the NLB has a security group it must allow inbound traffic from the clients' IP addresses, or you can turn off inbound security group rule evaluation for PrivateLink traffic.
- If you parse proxy protocol v2 source addresses, make sure you can handle IPv6.

## Verify
- [ ] Consumer endpoint reaches `Available` after acceptance; `curl https://api.example.com` from the consumer VPC succeeds with private DNS.
- [ ] Private DNS verification state `verified`.
- [ ] Target logs show the proxy-protocol endpoint ID for each consumer.

## Checked
2026-10-28. Confirmed against the PrivateLink guide pages "Create an endpoint service" (NLB or GWLB, one service per NLB, Region scope, cross-Region access, acceptance, private DNS name, IPv6 requirements, proxy protocol, security groups, at least two AZs), "Configure an endpoint service" (principal ARN forms, default no access, removal does not affect connections, enabling new AZs, verification) and "Manage DNS names" (public TXT record, name/value from describe-vpc-endpoint-service-configurations, verification states), plus botocore ec2 (PrivateDnsNameConfiguration states; CLI flags verified by check_commands.py). Removed unconfirmed claims: ALB behind NLB, AZ-ID wording, cross-zone advice, Proxy Protocol v2 TLV detail, EventBridge-based acceptance automation.
Method: documentation only; no commands were run.
