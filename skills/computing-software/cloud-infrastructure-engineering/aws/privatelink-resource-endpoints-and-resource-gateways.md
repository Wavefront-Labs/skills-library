---
id: computing-software.cloud-infrastructure-engineering.aws.privatelink-resource-endpoints-and-resource-gateways
name: privatelink-resource-endpoints-and-resource-gateways
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, privatelink, resource-endpoint, resource-gateway, resource-configuration, vpc-lattice, cross-account-database-access]
level: advanced
status: docs-checked
description: "Share a specific resource (RDS DB, IP or DNS target) privately across VPCs and accounts with resource gateways, resource configurations and resource VPC endpoints, no NLB needed."
sources: ["https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-access-resources.html", "https://docs.aws.amazon.com/vpc/latest/privatelink/resource-configuration.html", "https://docs.aws.amazon.com/vpc-lattice/latest/ug/resource-gateway.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PrivateLink for resources: resource gateways and resource endpoints

**Problem it solves:** classic PrivateLink exposes a *service* behind an NLB. To share one
database or an on-prem IP with another account you used to build an NLB with IP targets
and keep it in sync. VPC Lattice resource gateways and resource
configurations let a consumer create a **resource endpoint** straight to the resource.

## 1. Provider side
1. **Resource gateway**: ingress point into the provider VPC, ENIs in chosen subnets.
```bash
aws vpc-lattice create-resource-gateway --name db-gw --vpc-identifier vpc-0prov \
  --subnet-ids subnet-a subnet-b --security-group-ids sg-0gw --ip-address-type IPV4
```
   The gateway SG must be allowed in the database SG on the DB port.
2. **Resource configuration**: what is shared and on which ports.
```bash
aws vpc-lattice create-resource-configuration --name orders-db \
  --type ARN --resource-gateway-identifier rgw-... \
  --resource-configuration-definition 'arnResource={arn=arn:aws:rds:eu-west-1:111122223333:db:orders}' \
  --port-ranges 5432 --protocol TCP
```
   Types: `SINGLE` (one IP address or domain name), `GROUP` with `CHILD` configurations
   (several IPs or domain names behind one share; a child cannot be shared on its own),
   `ARN` for a supported AWS-provisioned resource (only RDS databases are supported, and not a
   publicly accessible cluster), and `CIDR` (reached through a tunnel endpoint). Only TCP is
   supported for the protocol (CIDR configurations use `TCP_UDP`); clients can only use the
   ports you list. IPv4 targets must be private IPs from 10.0.0.0/8, 100.64.0.0/10,
   172.16.0.0/12 or 192.168.0.0/16.
3. **Share** with consumer accounts or the org via RAM:
   `aws ram create-resource-share --name orders-db --resource-arns <rescfg-arn>
   --principals 444455556666`.

## 2. Consumer side
Option A, resource endpoint in a VPC:
```bash
aws ec2 create-vpc-endpoint --vpc-endpoint-type Resource --vpc-id vpc-0cons \
  --resource-configuration-arn <shared-rescfg-arn> --subnet-ids subnet-x subnet-y \
  --security-group-ids sg-0client --private-dns-enabled
```
Clients connect to the endpoint's DNS name (or the resource's own DNS name if private DNS
is enabled and the provider set a custom domain). Option B: associate the resource
configuration with a **VPC Lattice service network** and give consumer VPCs a
service-network endpoint or association, which scales to many resources and VPCs.

## 3. When to choose which
| Need | Use |
|---|---|
| Expose an HTTP/TCP application to many consumers, consumer-initiated | Endpoint service (NLB/GWLB) |
| Share one DB/cache/on-prem host to a few accounts | Resource configuration + resource endpoint |
| Many services and resources across many VPCs with auth policies | VPC Lattice service network |
| Full network connectivity both ways | TGW/peering, not PrivateLink |

## 4. Operations
- Traffic is one-way (consumer to provider).
- Resource gateway security group rules control outbound traffic from the gateway to the resources.
- Pricing: see the PrivateLink pricing page.

## Gotchas
- The provider's DB SG must allow the **resource gateway** SG, not the consumer CIDRs.
- ARN configurations support only RDS databases; other resources use IP or domain-name configurations.
- A domain-name target in a private hosted zone or on a private DNS server needs the resource
  gateway's DNS resolution set to `IN_VPC`; a target outside your VPC needs a NAT gateway in the VPC.

## Verify
- [ ] From a consumer instance, `nc -vz <endpoint-dns> 5432` succeeds; `psql` connects with TLS.
- [ ] After an RDS failover, the consumer reconnects without changes.
- [ ] RAM share shows the consumer account associated; unshared accounts cannot create endpoints.

## Checked
2026-10-31. Confirmed in the PrivateLink resource configuration page, the VPC Lattice resource gateway page and the botocore vpc-lattice and ec2 models: configuration types SINGLE/GROUP/CHILD/ARN/CIDR and what each holds, RDS as the only ARN type, TCP only (TCP_UDP for CIDR), port ranges, private IPv4 ranges, IN_VPC DNS resolution, gateway security groups controlling outbound traffic, create-resource-gateway/create-resource-configuration parameters, and `Resource` as a VPC endpoint type. Corrected the example from `--type SINGLE` to `--type ARN` for an RDS ARN. Removed as unconfirmed: launch date, CloudWatch namespace, pricing description, overlapping-CIDR and RDS TLS statements.
Method: documentation only; no commands were run.
