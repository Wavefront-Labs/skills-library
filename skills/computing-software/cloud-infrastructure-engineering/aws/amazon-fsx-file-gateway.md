---
id: computing-software.cloud-infrastructure-engineering.aws.amazon-fsx-file-gateway
name: amazon-fsx-file-gateway
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, storage-gateway, amazon-fsx-file-gateway, fsx-windows, smb-cache]
level: advanced
status: docs-checked
description: "Give branch offices low-latency SMB access to FSx for Windows File Server through Amazon FSx File Gateway: AD join, file system association and cache settings."
sources: ["https://docs.aws.amazon.com/filegateway/latest/filefsxw/what-is-file-fsxw.html", "https://docs.aws.amazon.com/storagegateway/latest/APIReference/API_AssociateFileSystem.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Amazon FSx File Gateway

**What:** an on-prem Storage Gateway that caches an FSx for Windows File Server share locally, so branch
users get LAN-speed SMB while data lives in AWS. Before a new design, check the current Storage Gateway
documentation for the product's availability status.

## 1. Prerequisites
- FSx for Windows file system joined to AD; the gateway must join the same domain.
- Network: Direct Connect or VPN so the gateway can reach the FSx file share over SMB and FSx can join your
  on-premises AD domain.
- A service account in AD allowed to join computers and access the shares.

## 2. Activate and join
Activate the gateway as an FSx File Gateway, then join the domain after it can reach FSx (the Storage Gateway
console or API), then associate the file system:
```bash
aws storagegateway join-domain --gateway-arn <GW_ARN> --domain-name corp.example.com \
  --user-name svc-sgw --password '<PASSWORD>' --organizational-unit "OU=Gateways,DC=corp,DC=example,DC=com"
aws storagegateway associate-file-system --gateway-arn <GW_ARN> \
  --location-arn arn:aws:fsx:<REGION>:<ACCOUNT_ID>:file-system/fs-0abc \
  --user-name svc-sgw --password '<PASSWORD>' --client-token assoc-1 \
  --cache-attributes CacheStaleTimeoutInSeconds=300 --audit-destination-arn <LOG_GROUP_ARN>
```

## 3. Behaviour
- `CacheStaleTimeoutInSeconds` (an `--cache-attributes` field of AssociateFileSystem) controls how often the
  gateway refreshes its cache against FSx; multi-site writers to the same files risk conflicts.
- Size the cache disk for the working set.

## Verify
- [ ] Users map `\\gateway\share`; a file written there is visible on the FSx file system.

## Checked

2026-10-28. Confirmed against the FSx File Gateway what-is page (Direct Connect or VPN needed for SMB access and AD join; join domain after activation) and the Storage Gateway API reference page for AssociateFileSystem (CacheStaleTimeoutInSeconds), plus the botocore storagegateway model (ActivateGateway, JoinDomain).
Removed: the claim that AWS stopped offering the gateway to new customers (not on any fetched page), the FILE_FSX_SMB gateway-type value, SMB port 445 and HTTPS 443 specifics, the CacheHitPercent and CachePercentDirty metrics, and the async-upload behaviour wording.
Method: documentation only; no commands were run.
