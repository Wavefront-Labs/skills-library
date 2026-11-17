---
id: computing-software.digital-forensics-incident-response.evidence-handling.capturing-memory-from-cloud-vms
name: capturing-memory-from-cloud-vms
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [cloud-memory-acquisition, memory-acquisition, cloud-forensics, avml, dfir]
level: advanced
status: draft
description: "Capture memory from AWS, Azure and GCP instances: in-guest tools via SSM/Run Command, hibernation-based capture, upload paths and integrity records."
sources: ["https://github.com/microsoft/avml", "https://docs.aws.amazon.com/systems-manager/latest/userguide/run-command.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Hibernate.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capturing memory from cloud VMs

**Goal:** cloud providers do not hand you a hypervisor memory dump, so capture is done in-guest
(or via hibernation) and shipped to an evidence bucket.

## Linux instances (AVML)
```bash
# via AWS SSM Run Command / Azure Run Command / GCP OS Login session
curl -sLO https://github.com/microsoft/avml/releases/download/<ver>/avml && chmod +x avml   # better: pre-staged, hashed binary
./avml --compress /mnt/scratch/mem.lime
./avml --sas-url "<azure-sas-url>" --delete /mnt/scratch/mem.lime   # direct upload to Azure blob
sha256sum mem.lime
```
- AVML needs no kernel module and works on most distributions; LiME requires a module built for the exact kernel.
- Write to an attached scratch volume, not the root disk you also want to snapshot.

## Windows instances
- WinPmem or vendor EDR memory capture via SSM `AWS-RunPowerShellScript` / Azure Run Command; upload with `aws s3 cp` using a write-only role.

## Hibernation-based capture (AWS)
- Instances launched with hibernation enabled can be hibernated (`aws ec2 stop-instances --hibernate`);
  RAM is written to the encrypted root EBS volume. Snapshot that volume and extract the hibernation
  file / swap. Only works if hibernation was configured at launch.

## Records
- Instance ID, account, region, command invocation ID (SSM CommandId), tool hash, output hash,
  upload object key/version ID, UTC times.

## Gotchas
- SSM agent must be running and the instance role must allow it; a compromised instance may have SSM disabled.
- Memory capture can take minutes and CPU; autoscaling health checks may terminate the instance mid-capture - suspend scaling processes first.
- Do not stop the instance before capture: memory is lost (and instance store volumes are wiped).

## Verify
Image hash recorded at source and in the bucket match; `vol banners.Banners` / `windows.info` succeeds.
