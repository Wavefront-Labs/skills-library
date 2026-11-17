---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.cleaning-orphaned-resources-and-scheduled-non-prod-shutdown
name: cleaning-orphaned-resources-and-scheduled-non-prod-shutdown
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac-cost, orphaned-resources, scheduled-shutdown, finops]
level: practitioner
status: draft
description: "Find and remove idle or orphaned cloud resources (unattached volumes, old snapshots, idle IPs) and schedule non-production shutdowns with tags and automation."
sources: ["AWS Instance Scheduler (https://docs.aws.amazon.com/solutions/latest/instance-scheduler-on-aws/solution-overview.html)", "Azure automation start/stop VMs (https://learn.microsoft.com/en-us/azure/azure-functions/start-stop-vms/overview)", "AWS Well-Architected Cost Optimization (https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Orphaned resources and scheduled shutdown

## Find orphans
```bash
# AWS
aws ec2 describe-volumes --filters Name=status,Values=available --query 'Volumes[].{id:VolumeId,gb:Size,created:CreateTime}'
aws ec2 describe-addresses --query 'Addresses[?AssociationId==null].PublicIp'
aws ec2 describe-snapshots --owner-ids self --query "Snapshots[?StartTime<='2026-01-01'].[SnapshotId,VolumeSize]"
aws elbv2 describe-target-groups --query 'TargetGroups[?length(LoadBalancerArns)==`0`].TargetGroupName'
# Azure
az disk list --query "[?diskState=='Unattached'].{name:name,rg:resourceGroup}"
az network public-ip list --query "[?ipConfiguration==null].name"
```
Also: resources not in any Terraform state (compare `terraform state list` across stacks vs cloud inventory), and resources without an `Owner` tag.

## Safe cleanup process
1. Report (owner from tags, age, cost).
2. Tag `cleanup-candidate=<date>` and notify the owner.
3. Snapshot/backup if data-bearing.
4. Delete after the grace period — through IaC where the resource is managed (remove from code), via automation otherwise:
```yaml
- amazon.aws.ec2_vol:
    id: "{{ item }}"
    state: absent
  loop: "{{ approved_orphan_volume_ids }}"
```

## Scheduled shutdown of non-prod
- Tag-driven: `Schedule=office-hours` on dev/test instances.
- AWS Instance Scheduler / Azure Start-Stop VMs, or an AAP schedule running:
```yaml
- amazon.aws.ec2_instance:
    filters: {"tag:Schedule": office-hours, instance-state-name: running}
    state: stopped
```
at 19:00 and `state: running` at 07:00 on weekdays (controller RRULE schedules).
- Scale ASGs/node pools to zero instead of stopping members (they would be replaced).

## Gotchas
- Stopped instances still bill for volumes and IPs.
- Shutdown breaks long-running tests and batch jobs; provide an opt-out tag with expiry.

## Verify
- [ ] Monthly report shows orphan count and non-prod off-hours runtime trending down.
