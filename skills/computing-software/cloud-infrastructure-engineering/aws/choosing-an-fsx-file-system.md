---
id: computing-software.cloud-infrastructure-engineering.aws.choosing-an-fsx-file-system
name: choosing-an-fsx-file-system
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, fsx, fsx-selection, efs-vs-fsx, smb, nfs, iscsi, storage-architecture]
level: practitioner
status: docs-checked
description: "Pick the right AWS file service: EFS or FSx for Lustre, NetApp ONTAP, OpenZFS or Windows File Server, by current storage, protocol, performance, availability and features."
sources: ["https://docs.aws.amazon.com/fsx/latest/WindowsGuide/what-is.html", "https://aws.amazon.com/fsx/when-to-choose-fsx/", "https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a file system on AWS

## 1. Start from what you run today
AWS's "Choosing an Amazon FSx File System" page recommends matching your current storage technology to keep application compatibility:
| Current storage | FSx choice |
|---|---|
| Lustre or other parallel file systems | FSx for Lustre |
| NetApp ONTAP or other NAS appliances | FSx for NetApp ONTAP |
| ZFS or other Linux-based file servers | FSx for OpenZFS |
| Microsoft Windows Server | FSx for Windows File Server |

Amazon EFS is the separate, serverless NFS option: fully elastic, no capacity or performance provisioning, NFSv4.1 and NFSv4.0, reachable from EC2, ECS, EKS, Lambda and Fargate. It is not supported on Windows EC2 instances.

## 2. Comparison (from the FSx page; some figures are ranges)
| | ONTAP | OpenZFS | Windows | Lustre |
|---|---|---|---|---|
| Latency | <1 ms | <0.5 ms | <1 ms | <1 ms |
| Max throughput per file system | 72-80 GB/s | 10-21 GB/s | 12-20 GB/s | 1000 GB/s |
| Max throughput, single client | 18 GB/s | 10 GB/s | 20 GB/s | 150 GB/s |
| Max IOPS | Millions | 1-2 million | Hundreds of thousands | Millions |
| Max size | Virtually unlimited (10s of PBs) | 512 TiB | 64 TiB | Multiple PBs |
| Clients | Windows, Linux, macOS | Windows, Linux, macOS | Windows, Linux, macOS | Linux |
| Protocols | SMB 2.0-3.1.1, NFS 3/4.0/4.1/4.2, iSCSI | NFS 3/4.0/4.1/4.2 | SMB 2.0-3.1.1 | POSIX-compliant custom protocol |
| Deployment | Single-AZ and Multi-AZ | Single-AZ and Multi-AZ | Single-AZ and Multi-AZ | Single-AZ, Persistent or Scratch |
| Availability SLA | Multi-AZ 99.99%, Single-AZ 99.9% | Multi-AZ 99.99%, Single-AZ 99.5% | Multi-AZ 99.99%, Single-AZ 99.5% | Single-AZ 99.5% |
The lower figure in a throughput range is baseline; the upper includes caching, bursting and compression. All four run on EC2, ECS and EKS, and all offer user/group quotas, and crash-consistent incremental backups.
- Only Lustre has automatic import/export of S3 data sets.
- Cold-data cost options: ONTAP low-cost tier with automatic cycling of cold data; HDD storage for Windows and Lustre.
- Hybrid: NetApp ONTAP gives on-premises caching (Global File Cache, FlexCache), SnapMirror backup/DR from on-premises, and FlexCache compute bursting.
- Cross-region replication: ONTAP via SnapMirror; Lustre via S3 cross-region replication.

## 3. FSx for Windows File Server specifics
Fully managed Windows file servers on native Windows; SMB 2.0 to 3.1.1; joins Microsoft Active Directory at creation; Windows ACLs; data in transit encrypted with SMB Kerberos session keys, at rest with KMS. You set storage (GiB), SSD IOPS and throughput (MBps) independently and can change them later. HDD suits home directories, shares and content management; SSD suits databases, media processing and analytics. Automatic daily backups are on by default (VSS-consistent). Multi-AZ keeps a standby server in another AZ. Accessible from other VPCs, accounts and Regions via VPC peering or transit gateway, and from on-premises via Direct Connect or Site-to-Site VPN.

## 4. Questions before choosing
1. Which clients and OS, and which protocol do they already speak?
2. Throughput, IOPS and latency at peak; parallelism?
3. Capacity now and later; how much is cold?
4. Features needed: AD, ACL type, quotas, backups, replication?
5. Availability target (Multi-AZ?) and DR.
6. For prices, see the Amazon EFS and Amazon FSx pricing pages (not covered here).

## Method
Rewritten from the three cited pages. Cost figures, EFS-vs-FSx latency claims, Amazon File Cache and Mountpoint for S3 advice, and feature rows whose table cells could not be mapped to a column were removed.

## Checked
Checked 2026-11-08 against the three cited pages (FSx for Windows overview, Choosing an Amazon FSx File System, What is Amazon EFS).
Method: docs-only read of cited pages, 2026-11-08
