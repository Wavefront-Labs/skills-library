---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.nat-gateway-cost-reduction
name: nat-gateway-cost-reduction
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, architecting-for-cost, nat-gateway-cost-reduction, nat-gateway, vpc-endpoints, data-transfer, egress, private-link]
level: practitioner
status: docs-checked
description: "Cut NAT gateway cost: find traffic by destination with flow logs, add free gateway endpoints and interface endpoints, and keep traffic in the same AZ."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-pricing.html", "https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html", "https://cloud.google.com/nat/pricing", "https://learn.microsoft.com/azure/nat-gateway/nat-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NAT gateway cost reduction

An AWS NAT gateway is charged for each hour it is available and each gigabyte it processes. Google
Cloud NAT charges an hourly gateway price (Public NAT: scaled by the number of VMs using it, capped
at 32), a per-GiB processing price, an hourly price per external IP address used, and normal data
transfer out for traffic leaving the network. See each provider's pricing page for rates; heavy
pulls from S3, container registries or APIs through NAT can cost more than the instances.

## Find the traffic
1. Cost: break NAT gateway charges into hours and bytes processed per account and Region in your
   cost data.
2. Enable VPC Flow Logs on the NAT gateway network interface (or its subnet), aggregate bytes by
   destination address, and map destinations to services (for example AWS's published IP ranges)
   to see what is worth moving off NAT.

## Fixes, in order of value
1. **Gateway endpoints for S3 and DynamoDB** (AWS): no additional charge. Traffic to the service
   goes through a route-table entry using the service's prefix list, so private subnets no longer
   need a NAT device to reach them. Each subnet's route table must be associated with the endpoint;
   instances in other subnets keep using the public endpoint. Security groups and network ACLs must
   still allow the traffic.
2. **Interface endpoints** (PrivateLink) for other AWS services that support them: AWS suggests
   them when most NAT traffic goes to such services; compare against AWS PrivateLink pricing.
3. **Same-AZ placement**: AWS advises keeping resources that send heavy traffic in the same
   Availability Zone as the NAT gateway, or creating a NAT gateway in each AZ that has resources,
   to reduce cross-AZ data transfer charges.
4. **Cache and mirror**: pull-through caches for container images and packages inside the VPC;
   avoid pulling images on every start.
5. **Google Cloud**: Public NAT also bills per external IP, so use only the IPs you need; check usage
   with `gcloud compute routers get-nat-ip-info`.

## Gotchas
- A NAT gateway per AZ adds hourly cost; at low volume in non-prod a single gateway can be
  cheaper (accept the AZ risk).
- Gateway endpoint routes cannot be modified or deleted by hand; they are removed when the route
  table is disassociated or the endpoint is deleted.
- A more specific route to the service's IP range in the same Region takes precedence over the
  endpoint route; traffic to the service in a different Region still goes via the internet
  gateway or NAT.

## Verify
- [ ] Top NAT destinations identified and the S3/DynamoDB share moved to gateway endpoints.
- [ ] NAT gateway bytes-processed trend reduced after changes.

## Checked

Method: docs-checked 2026-11-09 against AWS NAT gateway pricing page, AWS gateway endpoints page, Google Cloud NAT pricing page and Azure NAT Gateway overview (pricing section only). Removed unconfirmed: all price figures, usage type names, flow-log SQL, interface endpoint prices and break-even claim, IPv6 egress-only gateway, Azure service/private endpoint remarks.
