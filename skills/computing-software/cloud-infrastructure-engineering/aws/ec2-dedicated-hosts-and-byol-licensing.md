---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-dedicated-hosts-and-byol-licensing
name: ec2-dedicated-hosts-and-byol-licensing
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, dedicated-hosts, dedicated-instances, byol, license-manager, windows-server, sql-server]
level: practitioner
status: docs-checked
description: "Run licence-bound software on EC2: Dedicated Hosts vs Dedicated Instances, host resource groups, License Manager configurations, BYOL rules for Windows/SQL Server, and costs."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-hosts-overview.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-hosts-BYOL.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-hosts-billing.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-hosts-understanding.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-hosts-allocating.html", "https://docs.aws.amazon.com/license-manager/latest/userguide/host-resource-groups.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dedicated Hosts, Dedicated Instances and BYOL

## 1. Which tenancy
| | Dedicated Instance | Dedicated Host |
|---|---|---|
| Isolation | hardware not shared with other accounts | a whole physical server allocated to you |
| Visibility of sockets/cores | no | **yes** (needed for per-socket/per-core licences) |
| Instance placement control | no | yes (affinity, host recovery) |
| Billing | per instance | per host |
| BYOL (per-socket, per-core or per-VM licences) | partial (SQL Server with License Mobility through Software Assurance, and Windows VDA) | yes |
| On-Demand Capacity Reservations | supported | not supported |
Choose Dedicated Hosts when licence terms are bound to sockets, physical cores or VMs, or you need
visibility and control of placement. If you only need dedicated hardware, Dedicated Instances may do.
Check the terms of your own licence agreement; BYOL is subject to the software vendor's terms.

## 2. Allocate and use a host
```bash
aws ec2 allocate-hosts --instance-family m5 --availability-zone eu-west-1a --quantity 1 \
  --auto-placement off --host-recovery on
aws ec2 run-instances --image-id ami-byol --instance-type m5.4xlarge \
  --placement 'Tenancy=host,HostId=h-0abc,Affinity=host'
```
`Affinity=host` makes the instance restart on the same host if stopped. Auto-placement (host level, off by default) lets untargeted `Tenancy=host` launches land on any matching host. Host recovery restarts instances on a replacement host after a host failure. Import your own machine image with VM Import/Export and activate Windows against your own KMS server; you cannot activate an imported Windows AMI against the Amazon KMS server.

## 3. Automate with License Manager
1. Create a **license configuration** (counting type `vCPU`, `Instance`, `Core` or `Socket`, with a hard or
   soft limit): `aws license-manager create-license-configuration --name sql-ent-byol --license-counting-type Core --license-count 64 --license-count-hard-limit`.
2. Associate it with the BYOL AMI.
3. Create a **host resource group** that uses the configuration; launch into the group (no host
   ID needed). The group can allocate hosts, release unused hosts and recover failed hosts automatically,
   if you enable those settings. Once a host is in a group you launch through the group, not onto the host.
4. License Manager tracks usage per configuration; AWS Config host recording can also feed licence reporting.

## 4. Cost levers
- Fill hosts (mixed sizes in the family where the host supports it); billing is per host.
- Dedicated Host Reservations (they need an active allocated host) and Savings Plans apply, except for the u-*.metal high-memory hosts for Savings Plans.
- Compare BYOL plus host cost with licence-included options for your footprint.

## Gotchas
- Whether a Windows Server or SQL Server licence may be brought to Dedicated Hosts depends on Microsoft's licensing terms; AWS pages point to the Microsoft licensing guidance.
- To run RHEL or SUSE Linux on a Dedicated Host you must bring your own AMI (except for the u-*.metal high-memory hosts).
- A host allocated for a virtualised type cannot later be changed to a `.metal` type, or the reverse.
- Changing an instance between tenancies uses `modify-instance-placement`.

## Verify
- [ ] `aws ec2 describe-hosts` shows utilisation and the expected instances.
- [ ] License Manager shows consumed vs available licences and blocks launches over a hard limit.
- [ ] Licence terms documented and matched to the chosen tenancy.

## Checked

Checked 2026-10-27 against the Amazon EC2 User Guide (Dedicated Hosts overview, billing, BYOL, auto-placement and affinity, allocate, launch, host recovery), the AWS License Manager guide (host resource groups) and the botocore EC2 and License Manager models.
- The Dedicated Host versus Dedicated Instance comparison (billing basis, socket and core visibility, affinity, BYOL, Capacity Reservations) taken from the overview table; the earlier "BYOL generally no" and "regional dedicated fee" wording was corrected.
- `allocate-hosts` (`--instance-family`, `--auto-placement`, `--host-recovery`), `--placement Tenancy=host,HostId=...,Affinity=host`, `ModifyInstancePlacement` tenancy and affinity values and the License Manager counting types and `--license-count-hard-limit` confirmed.
- Host resource group settings, Dedicated Host Reservations, Savings Plans exclusion for u-*.metal hosts, RHEL and SUSE AMI restriction, KMS activation note and `.metal` change restriction confirmed.
- Removed the Windows Server "after Oct 2019" claim, which no AWS page read states; it defers to Microsoft's terms.

Method: documentation only; no commands were run.
