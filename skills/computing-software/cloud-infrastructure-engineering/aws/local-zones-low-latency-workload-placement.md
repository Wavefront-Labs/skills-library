---
id: computing-software.cloud-infrastructure-engineering.aws.local-zones-low-latency-workload-placement
name: local-zones-low-latency-workload-placement
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, local-zones, low-latency-placement, edge-compute, latency-testing, hybrid-architecture]
level: advanced
status: docs-checked
description: "Place latency-sensitive workloads in AWS Local Zones: what to put there, how to opt in and create a subnet, latency testing, and failover design."
sources:
  - https://docs.aws.amazon.com/local-zones/latest/ug/what-is-aws-local-zones.html
  - https://docs.aws.amazon.com/local-zones/latest/ug/getting-started.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local Zones: low-latency workload placement

## 1. What a Local Zone gives you
AWS Local Zones place compute, storage, database and other select AWS resources close to
large population and industry centres, for low-latency access to your applications. AWS
lists these reasons to use them: low-latency applications at the edge (real-time gaming,
live streaming, AR/VR, virtual workstations), simpler hybrid cloud migrations that keep
low latency, and meeting local data residency requirements. There is no additional charge
for enabling a Local Zone; you pay for the resources you deploy, at prices that differ from
the parent Region. The set of services in a Local Zone is a subset of the parent Region's
and varies by zone: check the Local Zones features and per-zone availability before design.

## 2. Decide the split (practitioner guidance)
Put in the Local Zone only what needs the latency (real-time media, game servers, AR/VR
rendering, virtual workstations, hybrid apps near an on-prem site). Keep databases of record,
object storage, control planes and batch work in the parent Region unless the zone supports
the service you need. Every call back to the Region adds latency and may add data transfer
charges, so measure the link between zone and Region.

## 3. Enable and create resources
The getting-started guide sequence: opt in to the Local Zone, create a subnet in a VPC of the
parent Region specifying the Local Zone, then create resources in that subnet.
```bash
aws ec2 describe-availability-zones --region us-west-2 \
  --filters Name=zone-type,Values=local-zone --all-availability-zones
aws ec2 modify-availability-zone-group --region us-west-2 \
  --group-name us-west-2-lax-1 --opt-in-status opted-in
aws ec2 create-subnet --region us-west-2 --availability-zone us-west-2-lax-1a \
  --vpc-id <vpc-id> --cidr-block <cidr-in-vpc-range>
aws ec2 describe-instance-type-offerings --location-type availability-zone \
  --filters Name=location,Values=us-west-2-lax-1a
```
Opting in via the console also asks you to enable the parent Region. To disable a zone
group you must open an AWS Support case titled "Disable zone group" naming the group. When
you finish, delete the resources in the Local Zone.

## 4. Measure latency before committing (practitioner guidance)
- Test from representative client networks to an instance in the Local Zone and one in the
  parent Region (`mtr`, `ping`, application-level RTT).
- Include last-mile variability (mobile, Wi-Fi); a Local Zone helps the network part only.

## 5. Resilience (practitioner guidance)
Design failover to the parent Region (for example Route 53 failover routing) and accept
higher latency during failover. Check capacity in your zone for the instance types you need
and test scaling.

## Verify
- [ ] Measured RTT improvement documented for target user populations.
- [ ] Only latency-critical tiers in the Local Zone; dependencies on the parent Region quantified.
- [ ] Failover to the parent Region tested.

## Checked
Method: docs-checked 2026-11-09 against the Local Zones "What is" and "Getting started" pages, read via summarising fetch. The services page returned only a title, so it was dropped as a source along with the service-by-service list, EBS types, single-digit-millisecond and 5-20 ms figures, NAT/IGW notes, "most zones are single zone" and capacity reservation claims. Sections 2, 4 and 5 are practitioner guidance.
