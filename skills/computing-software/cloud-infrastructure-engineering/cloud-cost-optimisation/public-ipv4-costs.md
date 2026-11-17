---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.public-ipv4-costs
name: public-ipv4-costs
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, workload-optimization, public-ipv4-costs, ipv4-charges, elastic-ip, ipv6, vpc-ipam, network-cost]
level: practitioner
status: docs-checked
description: "Reduce public IPv4 address charges: find in-use and idle addresses with IPAM and billing data, remove unneeded ones, adopt private admin access and IPv6."
sources: ["https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/", "https://docs.aws.amazon.com/vpc/latest/ipam/view-public-ip-insights.html", "https://azure.microsoft.com/pricing/details/ip-addresses/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Public IPv4 address cost reduction

Since 1 February 2024 AWS charges per hour for every public IPv4 address, whether attached to a
service or not (see the Amazon VPC pricing page for the current rate). The charge applies across AWS
services such as EC2, RDS and EKS nodes, in all Regions. Azure also bills public IPs by SKU and by
static or dynamic allocation. Large estates with public IPs on every instance pay a lot for
addresses alone.

## Find them
- Billing: AWS Cost and Usage Reports include public IPv4 address usage; filter on that usage per
  account and Region.
- **VPC IPAM Public IP insights** (no cost) lists the public IPv4 addresses used by services across
  all Regions of an account or, with an organization integration, of the whole AWS Organization.
  It splits them by type (Elastic IP, EC2 public IP, BYOIP, service-managed) and shows the
  service (load balancer, NAT gateway, RDS, Redshift, Site-to-Site VPN, Global Accelerator and
  others), and whether the address is associated. Unassociated Elastic IPs trigger a banner telling
  you to release them. CLI: `aws ec2 get-ipam-discovered-public-addresses`.
- CLI:
  ```bash
  aws ec2 describe-addresses --query 'Addresses[?AssociationId==null].[PublicIp,AllocationId]'
  aws ec2 describe-network-interfaces --query 'NetworkInterfaces[?Association.PublicIp].[NetworkInterfaceId,Association.PublicIp,Description]'
  ```

## Reduce
1. **Release idle Elastic IPs** (unassociated) unless allow-listed by a partner.
2. **Stop auto-assigning public IPv4**: EC2 public IPs are assigned when an instance is launched
   into a default subnet or a subnet configured to auto-assign one. Put instances in private
   subnets behind load balancers and NAT.
3. **Admin access without public IPs**: EC2 Instance Connect can reach instances over private IPv4
   addresses, so SSH or RDP administration does not need a public address.
4. **IPv6**: AWS positions IPv6 adoption as the way to avoid the charge; use ELB and NAT gateways
   for ingress and egress rather than a public IPv4 per instance. Test dependencies first.
5. **BYOIP** where you own address space: AWS does not charge for IP addresses you bring with BYOIP.
   On Azure, public IPv4 prefixes derived from custom (BYOIP) prefixes are not charged.

## Azure notes
- In the ARM model a dynamic public IP is not charged while its VM is stopped-deallocated; a static
  public IP is charged regardless of what it is attached to.
- A public IPv4 prefix is charged per address per hour from the moment it is created.

## Gotchas
- NAT gateways and load balancers also hold public IPs that are charged; Public IP insights shows
  them by service.
- Some partners allow-list fixed IPs; check before releasing Elastic IPs.

## Verify
- [ ] Idle (unassociated) address count is zero or allow-listed.
- [ ] New subnets do not auto-assign public IPv4 unless needed.
- [ ] Public IPv4 usage in the cost report trends down.

## Checked

Method: docs-checked 2026-11-09 against the AWS public IPv4 charge blog post, VPC IPAM view-public-ip-insights page, Azure IP addresses pricing page, and botocore ec2 model (DescribeAddresses, DescribeNetworkInterfaces fields in the --query examples). Removed unconfirmed: price figures, usage type names, ALB per-AZ address note, egress-only internet gateway, SSM/IAP/Bastion admin options, Google Cloud claim.
