---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-placement-groups
name: ec2-placement-groups
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, placement-group, cluster-placement, spread-placement, partition-placement, hpc, kafka]
level: practitioner
status: docs-checked
description: "Use EC2 cluster, spread and partition placement groups: when each fits, limits, insufficient-capacity errors, partition metadata for Kafka/HDFS, and moving instances in."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-strategies.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-placement-group.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/change-instance-placement-group.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EC2 placement groups

| Strategy | Places instances | Use for | Limits |
|---|---|---|---|
| **cluster** | close together in one AZ (same high-bisection network segment) | HPC, tightly coupled MPI, low-latency trading; with enhanced networking up to 10 Gbps single-flow inside the group (5 Gbps outside) | single AZ; current-generation types only (no burstable such as T2, no Mac1 or M7i-flex); mixing types or adding later raises capacity-error odds |
| **spread** | each on distinct hardware racks | a handful of critical instances (quorum nodes) | **7 running instances per AZ** per group; can span AZs in a Region |
| **partition** | groups of racks ("partitions"), no shared hardware between partitions | Kafka, HDFS, Cassandra — rack awareness | 7 partitions per AZ; instance count limited only by account limits; Dedicated Instances: max 2 partitions |

## 1. Create and launch
```bash
aws ec2 create-placement-group --group-name mpi-pg --strategy cluster
aws ec2 create-placement-group --group-name kafka-pg --strategy partition --partition-count 3
aws ec2 run-instances --launch-template LaunchTemplateName=kafka --count 3 \
  --placement 'GroupName=kafka-pg,PartitionNumber=1'
```
Spread can also be **host-level**, but host-level spread is supported only on Outposts. You can create at most 500 placement groups per Region.

## 2. Cluster tips
- Launch all instances in **one request** with the same instance type; adding later
  increases `InsufficientInstanceCapacity` odds. On failure: stop and start all, or retry later.
- Reserve capacity explicitly with an **On-Demand Capacity Reservation created in the cluster placement
  group**. Zonal Reserved Instances cannot reserve capacity in a placement group, Capacity Blocks do not
  support placement groups, and Capacity Reservations do not reserve capacity in partition or spread groups.
- Pick an instance type that supports enhanced networking for the lowest latency and highest packets per second.
- Traffic to the internet or over Direct Connect from a cluster group is limited to 5 Gbps.

## 3. Partition awareness
Each instance can read its partition from IMDS:
```bash
TOKEN=$(curl -sX PUT http://169.254.169.254/latest/api/token -H 'X-aws-ec2-metadata-token-ttl-seconds: 60')
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/placement/partition-number
```
Feed it to Kafka `broker.rack` / HDFS rack topology so replicas land on different partitions.

## 4. Moving an existing instance
Instance must be **stopped**:
```bash
aws ec2 modify-instance-placement --instance-id i-123 --group-name kafka-pg --partition-number 2
aws ec2 modify-instance-placement --instance-id i-123 --group-name ""   # remove from its group
```

## Gotchas
- Spread's 7-per-AZ cap is per group; use several groups or a partition group for more.
- Cluster placement doesn't protect against hardware failure — the opposite: shared fate.
- Placement groups can't be merged; an instance belongs to one group.
- Dedicated Hosts cannot be launched in placement groups, and Spot Instances set to stop or hibernate on interruption cannot be placed in one.

## Verify
- [ ] `aws ec2 describe-instances --query 'Reservations[].Instances[].Placement'` shows GroupName/PartitionNumber as intended.
- [ ] Kafka brokers' `broker.rack` matches their partition number; replica sets span ≥ 2 partitions.
- [ ] Cluster group latency test (e.g. `sockperf`) meets the target.

## Checked

Date: 2026-10-27. Source: AWS EC2 User Guide pages Placement groups, Placement strategies, Create a placement group and Change the placement for an EC2 instance; EC2 API model in botocore (CreatePlacementGroup PartitionCount, ModifyInstancePlacement PartitionNumber, Placement PartitionNumber).
Confirmed: 7 running instances per AZ for rack-level spread; 7 partitions per AZ; 10 Gbps vs 5 Gbps single-flow with enhanced networking; one group per instance and no merging; Capacity Reservation and Capacity Block rules per strategy; 500 groups per Region; stopped-instance requirement and empty group name to remove; IMDS category placement/partition-number.
Removed: the unsupported claims about "hundreds of instances" per partition group and EFA/ENA Express as a placement benefit.

Method: documentation only; no commands were run.
