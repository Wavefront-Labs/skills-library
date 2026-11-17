---
id: computing-software.cloud-infrastructure-engineering.aws.snow-family-and-transfer-family
name: snow-family-and-transfer-family
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, snowball, snow-family, snowball-edge, snowcone, snowmobile, transfer-family, bulk-transfer, sftp, ftps, as2, offline-transfer, opshub, nfs-interface, s3-adapter, datasync, managed-sftp, custom-identity-provider, transfer-workflows]
level: practitioner
status: draft
description: "Move bulk data into AWS with Snowball Edge (order, unlock, NFS/S3 adapter copy, return) and run managed SFTP/FTPS/AS2 endpoints with AWS Transfer Family backed by S3 or EFS."
sources: ["AWS Snowball Edge Developer Guide - Getting started and transferring data", "AWS Snow Family - Device specifications and when to use which device", "AWS Transfer Family User Guide - Creating servers and managing users", "AWS Transfer Family User Guide - Managed workflows and custom identity providers"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Snow Family and Transfer Family — when the network is too slow, and when partners still speak SFTP

**Goal:** tens of terabytes to petabytes arrive in S3 via shipped devices without data loss,
and external parties push/pull files over SFTP/FTPS/AS2 against S3 or EFS with no servers to patch.

## 1. Do you need a Snow device at all?
Transfer time ≈ data ÷ (bandwidth × ~0.8). 100 TB at 1 Gbps ≈ 12 days; at 10 Gbps ≈ 1.2 days.
If it fits in the window with DataSync over Direct Connect, skip hardware. Snow wins above
~10 TB per 100 Mbps-class link, or where the site has no usable uplink.

| Device | Capacity (approx.) | Use |
|---|---|---|
| **Snowball Edge Storage Optimized** | ~80 TB usable HDD (210 TB NVMe variant) | Bulk import/export |
| **Snowball Edge Compute Optimized** | less storage, vCPUs/GPU option, EC2-compatible instances | Edge processing then import |
| **Snowcone** (small, 8–14 TB) | Rugged, battery-capable | Small sites, DataSync agent on device (check current availability) |
| **Snowmobile** | Exabyte truck | Data-centre exit (engagement with AWS) |
Order several in parallel (cluster for compute) for petabyte-scale.

## 2. Snowball Edge import workflow
1. **Job** in the Snow console: import to S3, pick bucket(s), KMS key, IAM role, shipping
   address, device type. Devices ship with an E Ink label pre-addressed for return.
2. On arrival: connect power + network (RJ45/SFP+, 10/25/40/100 Gbps depending on model),
   get the device IP from the E Ink screen or DHCP.
3. **Unlock** with the manifest + unlock code from the console (both needed; keep them separate — chain of custody):
   ```bash
   snowballEdge unlock-device --endpoint https://<device-ip> --manifest-file ./manifest.bin --unlock-code 12345-abcde-...
   snowballEdge list-access-keys / get-secret-access-key   # local S3-compatible creds
   ```
   Or use **OpsHub** (GUI) for unlock, copy and monitoring.
4. Copy data with the **S3 adapter** (`aws s3 cp --endpoint https://<ip>:8443 --profile snow`)
   or mount the **NFS interface** (`snowballEdge start-service --service-id nfs …`) and `rsync`.
   Parallelise: many concurrent `s3 cp` streams, several workstations; one stream is slow.
   Small files kill throughput — tar/zip them first (>1 MB objects ideal); use `aws s3 sync`
   with `--only-show-errors` and keep a manifest of what was copied.
5. Validate: compare local checksums with the device's object list; the device verifies
   integrity on ingest. **Power off**, label updates automatically, ship back.
6. AWS imports into the bucket (days); job status → `Completed`; review the import report
   for any failed objects and recopy those via network. Data on the device is NIST-wiped.
- Encryption: 256-bit server-side with your KMS key; the device is useless without the unlock code.
- Export jobs: specify S3 key ranges; device arrives loaded; download via adapter.

## 3. Transfer Family
```bash
aws transfer create-server --protocols SFTP --identity-provider-type SERVICE_MANAGED \
  --endpoint-type VPC --endpoint-details SubnetIds=subnet-…,VpcId=vpc-…,AddressAllocationIds=eipalloc-… \
  --security-policy-name TransferSecurityPolicy-2024-01 --logging-role arn:aws:iam::…:role/TransferLogs
aws transfer create-user --server-id s-… --user-name partner1 --role arn:aws:iam::…:role/PartnerS3 \
  --home-directory-type LOGICAL --home-directory-mappings Entry=/,Target=/my-bucket/partner1 \
  --ssh-public-key-body "ssh-ed25519 AAAA…"
```
- Protocols: **SFTP** (most partners), **FTPS**, **FTP** (VPC-only, do not expose), **AS2**
  (EDI trading partners with MDN receipts), plus a **web app** for browser uploads to S3.
- Endpoints: **public** (AWS-managed IPs, no allow-listing possible) vs **VPC** with EIPs
  (static IPs partners can allow-list; SG-controlled); internal VPC for private only.
- Identity: `SERVICE_MANAGED` (keys stored in Transfer), **Directory Service** (AD),
  or **custom** (Lambda/API Gateway returning role, policy, home dir — for passwords in Secrets
  Manager or any IdP).
- Per-user **session policy** with `${transfer:UserName}` locks users to their prefix:
  `"Resource": "arn:aws:s3:::my-bucket/${transfer:HomeDirectory}/*"`. Logical home
  directory mappings hide the bucket name and let you chroot across buckets.
- Storage: S3 (object per file, no partial writes, `s3:PutObject` only when upload completes)
  or **EFS** (POSIX; set POSIX uid/gid per user).
- **Managed workflows**: on upload complete → steps (copy, tag, decrypt PGP, custom Lambda,
  delete); exception handler workflow for failures. Or just S3 event notifications.
- Host key: import your existing server's key (`--host-key`) when migrating so partners' known_hosts do not break; rotate with multiple host keys.
- Cost: per protocol-hour per server (~$0.30/h ≈ $216/month) + per GB. Stop (`stop-server`)
  servers used only in windows; one server can hold thousands of users.

## 4. Operations
- CloudWatch: `BytesIn/Out`, `FilesIn/Out`, `OnUploadExecutionsStarted`; **structured JSON
  logs** to a log group with `session-id`, `user`, `file path`, `status`.
- Security policy name pins ciphers/MACs/key exchange (FIPS variants exist); partners on
  ancient clients need an older policy — isolate them on their own server.
- Alarm on `FilesIn` dropping to 0 during an expected partner feed window.
- Test as a partner: `sftp -i key partner1@s-….server.transfer.<region>.amazonaws.com` then `ls`, `put`, verify the S3 object.

## Gotchas
- Snowball: a job sits "Preparing" if the KMS key policy does not allow the Snow service role; check before shipping delays.
- Snowball Edge devices time out and lock after a reboot; the manifest/unlock code are needed again on site.
- Copying with `aws s3 cp` from a Windows laptop over 1 GbE gives ~100 MB/s; use a server with 10 GbE and 8+ parallel streams for 1 GB/s-class.
- Transfer Family SFTP has no `chmod`/symlinks on S3-backed servers; some clients' "resume" fails — tell partners.
- Public endpoints change IPs; partners who allow-list must use a VPC endpoint with EIPs.
- A user's IAM role trust must allow `transfer.amazonaws.com` or logins fail with a generic auth error.
- Unconfirmed: current Snow device models/capacities and Snowcone availability by region — check the console at order time.

## Verify
- [ ] Transfer-time arithmetic documented and Snow justified (or DataSync chosen).
- [ ] Snowball: object count and total bytes on device match the local manifest before shipping; import report has 0 failures.
- [ ] Transfer Family: a test user can only list/put under their own prefix; another user's path returns permission denied.
- [ ] Partner connects with the published host key fingerprint; structured log shows the session and file.
- [ ] Workflow (or S3 event) fires on upload and the post-processing step completes.
