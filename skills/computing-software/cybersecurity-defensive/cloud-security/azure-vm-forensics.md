---
id: computing-software.cybersecurity-defensive.cloud-security.azure-vm-forensics
name: azure-vm-forensics
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [azure-vm-forensics, disk-snapshot-forensics, azure-incident-response, memory-acquisition, chain-of-custody, cloud-incident-response]
level: advanced
status: draft
description: "Collect forensic evidence from Azure VMs: isolate with NSG, snapshot OS/data disks, copy to a forensic subscription, hash, memory capture options, run command caveats and logs."
sources: ["https://learn.microsoft.com/en-us/azure/security/fundamentals/azure-forensic-computer-arch", "https://learn.microsoft.com/en-us/azure/virtual-machines/snapshot-copy-managed-disk", "https://learn.microsoft.com/en-us/azure/security/fundamentals/incident-response-overview", "https://csrc.nist.gov/pubs/sp/800/86/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Azure VM forensics

## 1. Contain without destroying evidence
- Do not stop/deallocate first (memory lost). Apply an isolation NSG to the NIC (deny all inbound/outbound except the forensic workstation subnet) or move into an isolated subnet.
- Defender for Endpoint "Isolate device" if onboarded (keeps EDR connectivity).
- Lock the resource (`CanNotDelete`) and note the time and actor.

## 2. Memory (if needed and feasible)
Run an acquisition tool inside the VM (e.g. WinPmem / AVML for Linux) via the EDR live response or Run
Command, writing to an attached evidence disk or uploading to a forensic storage account with a
short-lived SAS. Every in-guest action changes state - log it.

## 3. Disk snapshots
```
az snapshot create -g ir-rg -n vm1-os-snap-20261018 --source <os-disk-id> --incremental false
az snapshot grant-access -g ir-rg -n vm1-os-snap-20261018 --duration-in-seconds 3600 --access-level Read
# copy the VHD to the forensic subscription's immutable storage
azcopy copy "<sas-url>" "https://forensics.blob.core.windows.net/evidence/case123/vm1-os.vhd"
```
Snapshot all disks (OS and data) at the same time. Hash the copied VHD (SHA-256) and record in the
chain-of-custody log. Revoke access after copying.

## 4. Analyse in a forensic environment
Separate subscription/tenant segment with no trust to production; create a disk from the snapshot and
attach read-only to an analysis VM (SIFT, Windows forensic workstation), never boot the evidence disk.

## 5. Control-plane evidence
Activity log (who ran Run Command, changed NSGs, added extensions), Entra sign-in logs for those principals,
NSG flow logs, Defender for Cloud alerts, boot diagnostics/serial log.

## Gotchas
- Run Command and VM extensions execute as SYSTEM/root and are also attacker tools - check the activity log for their prior use.
- Encrypted disks (ADE/CMK) need key access in the forensic subscription.
- Snapshots in the same subscription can be deleted by a compromised admin; copy out quickly.

## Verify
- [ ] Evidence copies hashed, stored immutably, custody log complete.
- [ ] IR runbook tested on a sample VM.
