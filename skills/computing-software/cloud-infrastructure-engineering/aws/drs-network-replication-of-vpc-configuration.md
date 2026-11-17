---
id: computing-software.cloud-infrastructure-engineering.aws.drs-network-replication-of-vpc-configuration
name: drs-network-replication-of-vpc-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elastic-disaster-recovery, network-replication, source-network, vpc-recovery, drs-cross-region]
level: practitioner
status: docs-checked
description: "Keep the recovery-region network in sync with DRS network replication: source networks, replicated VPC configuration as CloudFormation, and recovery deployment."
sources: ["https://docs.aws.amazon.com/drs/latest/userguide/replicating-network-configurations.html", "https://docs.aws.amazon.com/drs/latest/userguide/source-networks.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DRS network replication of VPC configuration

**Problem:** servers replicate to the recovery region, but on the day the VPC there is out of
date: missing subnets, old security group rules, wrong routes. Recovery instances launch into the wrong network or fail.

## Source networks
DRS can replicate a source **VPC** configuration and save it as a CloudFormation stack template.
In the console, choose the network on the Source networks page, then Actions > Start replication,
and select an S3 bucket for the CloudFormation template. The bucket must be set before you start
network recovery, and S3 versioning must be enabled.
```bash
aws drs create-source-network --vpc-id vpc-0abc --origin-region <REGION> --origin-account-id <ACCOUNT_ID>
aws drs start-source-network-replication --source-network-id sn-0123
aws drs describe-source-networks
aws drs export-source-network-cfn-template --source-network-id sn-0123   # inspect what will be built
```

## Recovery
```bash
aws drs start-source-network-recovery \
  --source-networks sourceNetworkID=sn-0123,cfnStackName=dr-network-orders --deploy-as-new
```
- `cfnStackName` is a member of each `--source-networks` entry, not a separate flag.
- In the console you can update the recommended stack (the last one used), create a new stack,
  or use a previously created stack (this only updates the launch templates).
- When the recovery job is Successful, the VPC is launched in the target Region and the EC2 launch
  templates of the source servers in that network are updated, so recovered servers launch into the new
  network and subnet.

## Design notes
- CIDRs: decide whether the recovery VPC reuses the source CIDR or a different range, and plan DNS and
  routing accordingly.
- Check what the replicated template covers before relying on it for hybrid connectivity or DNS.

## Verify
- [ ] Source network replication started and the template bucket has versioning enabled.
- [ ] Drill: recovered network stack deploys; recovery instances launch into it and reach dependencies.

## Checked

2026-10-28. Confirmed against AWS documentation: console flow for network replication (S3 bucket, versioning required, update/new/previous stack options, launch templates updated after successful recovery); CreateSourceNetwork, ExportSourceNetworkCfnTemplate and StartSourceNetworkRecovery shapes via botocore drs model.
Removed: wrong --cfn-stack-name flag (cfnStackName is a member of --source-networks entries; check_commands flagged it), list of VPC resource types replicated, periodic-check claim, CIDR/connectivity and pre-deploy advice, out-of-VPC resource gotcha; account id placeholders.
Method: documentation only; no commands were run.
