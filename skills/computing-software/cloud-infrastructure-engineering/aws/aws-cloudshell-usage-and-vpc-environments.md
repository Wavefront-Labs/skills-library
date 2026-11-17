---
id: computing-software.cloud-infrastructure-engineering.aws.aws-cloudshell-usage-and-vpc-environments
name: aws-cloudshell-usage-and-vpc-environments
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudshell, vpc, iam, persistent-storage, file-transfer]
level: practitioner
status: docs-checked
description: "Use AWS CloudShell effectively: the per-region persistent home directory and its expiry, session limits, VPC environments and IAM controls."
sources: ["https://docs.aws.amazon.com/cloudshell/latest/userguide/limits.html", "https://docs.aws.amazon.com/cloudshell/latest/userguide/using-cshell-in-vpc.html", "https://docs.aws.amazon.com/cloudshell/latest/userguide/sec-auth-with-identities.html", "https://docs.aws.amazon.com/cloudshell/latest/userguide/aws-cloudshell-vpc-permissions-1.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS CloudShell

**Goal:** an authenticated shell in the browser for quick operations without local credentials.

## Limits that matter
- **Persistent storage:** 1 GB in `$HOME` per Region at no cost; other resources are recycled after each session.
- If you stop using CloudShell in a Region, its home directory is deleted 120 days after your last session there. Launching CloudShell again in that Region prevents removal.
- **Idle timeout:** a session ends after 20-30 minutes without keyboard or pointer interaction (10 minutes in GovCloud); running processes do not count as interaction.
- Up to 10 concurrent shells per Region per account; there is also a monthly usage quota per Region (both raisable through Service Quotas).
- A command cannot exceed 65412 characters.
- Large file uploads and downloads can be slow; the docs suggest copying from an S3 bucket with the CLI instead.

## VPC environments
- Create an environment in a VPC subnet with up to five security groups to reach private resources.
- Maximum two VPC environments per IAM principal.
- No persistent storage: the home directory is deleted when the session ends, times out or the environment is deleted.
- The Actions menu upload and download options are not available in VPC environments.
- Internet access works only from a private subnet with NAT; public subnets with an internet gateway route do not get it. The default VPC DNS zone is not configured automatically.
- To create them, the role needs these EC2 permissions: `ec2:DescribeVpcs`, `ec2:DescribeSubnets`, `ec2:DescribeSecurityGroups`, `ec2:DescribeDhcpOptions`, `ec2:DescribeNetworkInterfaces`, `ec2:CreateTags`, `ec2:CreateNetworkInterface`, `ec2:CreateNetworkInterfacePermission`; add `ec2:DeleteNetworkInterface` so CloudShell can clean up the network interfaces (tagged `ManagedByCloudShell`).

## IAM controls
- Managed policy `AWSCloudShellFullAccess` grants full access to CloudShell.
- To launch from the console a user needs `cloudshell:CreateEnvironment`, `cloudshell:CreateSession`, `cloudshell:GetEnvironmentStatus` and `cloudshell:StartEnvironment`.
- Restrict file transfer by denying `cloudshell:GetFileUploadUrls` and `cloudshell:GetFileDownloadUrls`; deny `cloudshell:PutCredentials` to stop console credentials being forwarded into the shell.

## Verify
- [ ] `aws sts get-caller-identity` in CloudShell shows the expected role.
- [ ] A role with the file-transfer actions denied cannot use Upload or Download.

## Checked
2026-10-28. Confirmed in the AWS CloudShell User Guide pages in `sources`: service quotas and restrictions, CloudShell in Amazon VPC, managing access with IAM policies, and VPC permissions.
Removed (not confirmed on fetched pages): the preinstalled tool list and `dnf` behaviour, maximum session length, the 1 GB single-file transfer size, tabs and split panes, CloudTrail attribution, the ExpiredToken and region gotchas, and the inbound-connection statement.
Method: documentation only; no commands were run.
