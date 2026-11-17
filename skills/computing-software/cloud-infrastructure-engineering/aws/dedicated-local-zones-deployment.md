---
id: computing-software.cloud-infrastructure-engineering.aws.dedicated-local-zones-deployment
name: dedicated-local-zones-deployment
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, local-zones, dedicated-local-zone-deployment, dedicated-local-zones, data-residency, sovereignty, edge-infrastructure]
level: practitioner
status: draft
description: "AWS Dedicated Local Zones: AWS-managed infrastructure dedicated to one customer at a chosen location, how it differs from Outposts and Local Zones, and enabling it."
sources: ["AWS Local Zones User Guide - Dedicated Local Zones", "AWS Local Zones User Guide - Getting started (opt in to zone groups)", "AWS Outposts User Guide - What is AWS Outposts (comparison)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dedicated Local Zones

**What:** a Local Zone built for exclusive use by one customer or community (often public sector or
regulated industries), placed at a location the customer specifies (including the customer's own
data centre), and operated by AWS as part of a parent Region.

## Compared with alternatives
| | Local Zone | Dedicated Local Zone | Outposts |
|---|---|---|---|
| Tenancy | shared, public | dedicated to one customer/community | your site, your capacity |
| Location | AWS-chosen metros | customer-specified | your facility |
| Operated by | AWS | AWS (with customer-specific operating controls) | AWS (hardware), you (site, power, network) |
| Scale and services | subset of Region services | subset tailored to the deployment | subset, smaller scale |
| Engagement | opt in | contract with AWS | order from catalog |
Choose Dedicated Local Zones for sovereignty, residency or isolation requirements at larger scale
than Outposts where you want AWS to run the infrastructure.

## Engagement and enablement
- Engaged through the AWS account team: requirements (location, capacity, services, security and operational controls such as staff vetting) become part of the agreement.
- Once delivered, the zone appears as a zone group for the allowed accounts:
```bash
aws ec2 describe-availability-zones --all-availability-zones \
  --filters Name=zone-type,Values=local-zone --query 'AvailabilityZones[].[ZoneName,GroupName,OptInStatus]'
aws ec2 modify-availability-zone-group --group-name <zone-group> --opt-in-status opted-in
aws ec2 create-subnet --vpc-id vpc-0abc --cidr-block 10.0.50.0/24 --availability-zone <dedicated-zone-name>
```
- Extend VPCs with subnets in the zone; workloads use the same APIs, IAM and tooling as the Region.
- Connectivity to on-premises via local network interfaces; parent Region for control plane and other services.

## Design notes
- Control plane operations go to the parent Region; plan for behaviour if the link is impaired.
- Service availability is a subset; verify every dependency (managed databases, load balancers, container services) against the zone's list.
- Combine with data residency controls (SCP region and zone restrictions, KMS with external key store) for sovereignty cases.

## Verify
- [ ] Required services confirmed available in the dedicated zone before migration planning.
- [ ] Subnets in the zone launch the workload; residency controls block use outside approved zones.
