---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-instance-type-discovery-and-offerings
name: ec2-instance-type-discovery-and-offerings
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, describe-instance-types, instance-type-offerings, attribute-based-instance-selection]
level: practitioner
status: docs-checked
description: "Find EC2 instance types that meet requirements and check which AZs offer them with describe-instance-types, instance-requirements queries and type offerings."
sources: ["https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instance-types.html", "https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instance-type-offerings.html", "https://docs.aws.amazon.com/cli/latest/reference/ec2/get-instance-types-from-instance-requirements.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-fleet-attribute-based-instance-type-selection.html", "https://docs.aws.amazon.com/ec2/latest/instancetypes/ec2-instance-quotas.html", "https://docs.aws.amazon.com/ram/latest/userguide/working-with-az-ids.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Discovering instance types and offerings

## 1. Filter by attributes
```bash
aws ec2 describe-instance-types \
  --filters Name=processor-info.supported-architecture,Values=arm64 \
            Name=vcpu-info.default-vcpus,Values=4 \
            Name=current-generation,Values=true \
  --query 'InstanceTypes[].{t:InstanceType,mem:MemoryInfo.SizeInMiB,net:NetworkInfo.NetworkPerformance,ebs:EbsInfo.EbsOptimizedInfo.BaselineBandwidthInMbps}' \
  --output table
```
Useful filter names: `instance-storage-supported`, `network-info.ena-support`, `network-info.efa-supported`,
`hypervisor` (nitro or xen), `burstable-performance-supported`, `hibernation-supported`,
`supported-usage-class` (on-demand, spot, capacity-block), `vcpu-info.valid-threads-per-core`.

## 2. Ask by requirements (same engine as attribute-based fleets)
```bash
aws ec2 get-instance-types-from-instance-requirements \
  --architecture-types x86_64 arm64 --virtualization-types hvm \
  --instance-requirements 'VCpuCount={Min=4,Max=8},MemoryMiB={Min=16384},BurstablePerformance=excluded,InstanceGenerations=[current]' \
  --query 'InstanceTypes[].InstanceType'
```
The same requirement attributes are used by attribute-based instance type selection in EC2 Fleet and Auto Scaling
mixed instances policies, so this call previews which types a requirement set matches.

## 3. Where is it offered?
```bash
aws ec2 describe-instance-type-offerings --location-type availability-zone-id \
  --filters Name=instance-type,Values=g6.xlarge --query 'InstanceTypeOfferings[].Location'
```
Use AZ **IDs** (`use1-az4`), not names: `us-east-1a` maps to different physical AZs per account.
`--location-type` accepts `region` (default), `availability-zone`, `availability-zone-id` and `outpost`; a location filter
must then be an AZ ID or an Outpost ARN for the current Region.

## 4. Gotchas
- Offered does not mean capacity available right now; use capacity reservations or diversify.
- On-Demand and Spot quotas are counted in vCPUs per instance family group, for example `Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) instances`.

## Verify
- [ ] Every subnet the ASG uses is in an AZ ID that offers each chosen type.

## Checked

Date: 2026-10-27. Sources: AWS CLI 2.38.6 references for describe-instance-types (filter list) and describe-instance-type-offerings (location types); botocore EC2 model (GetInstanceTypesFromInstanceRequirements request, InstanceRequirementsRequest members, BurstablePerformance and InstanceGeneration enums); EC2 Instance Types Guide quotas page; RAM user guide page on AZ IDs.
Confirmed: filter names processor-info.supported-architecture, vcpu-info.default-vcpus, current-generation, instance-storage-supported, network-info.ena-support, network-info.efa-supported, hypervisor, burstable-performance-supported, supported-usage-class; requirement keys VCpuCount, MemoryMiB, BurstablePerformance=excluded, InstanceGenerations=current; AZ IDs are consistent across accounts while AZ names map differently; quota name format.
Removed: the processor-info.manufacturer filter (not in the documented filter list) and the "new generations join automatically" claim.

Method: documentation only; no commands were run.
