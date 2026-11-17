---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-forensics
name: cloud-forensics
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, detection-and-response, cloud-forensics, evidence-capture, disk-snapshots, memory-acquisition, chain-of-custody, forensic-account, container-forensics]
level: advanced
status: draft
description: "Capture and analyse evidence in the cloud: snapshot and share volumes to a forensics account, memory capture, container evidence, log preservation, hashing and chain of custody."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/forensics.html", "https://learn.microsoft.com/azure/architecture/example-scenario/forensics/", "https://cloud.google.com/architecture/security-foundations/detective-controls"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud forensics and evidence capture

## Principles
Capture volatile evidence first, never analyse in the compromised account, hash everything,
record who did what when (chain of custody).

## Steps (VM)
1. **Isolate** without stopping: swap security group to deny-all (existing tracked connections may
   persist — also use NACLs or detach from subnet routes), remove from LB/ASG (set scale-in protection, detach).
2. **Memory** (volatile): acquire via SSM/Run Command with a memory tool (AVML for Linux, WinPmem
   for Windows) to an evidence bucket — before any reboot.
3. **Disk**: snapshot all volumes; copy/share snapshots to the **forensics account** (re-encrypt
   with a forensics KMS key); create volumes there and mount read-only on an analysis instance.
4. **Metadata**: instance details, IAM role, security groups, user data, tags, console output/screenshot.
5. **Hash** artefacts (SHA-256) and store in an evidence bucket with Object Lock and access logging.

## Containers / Kubernetes
Capture pod spec, logs, `kubectl debug`/ephemeral container for live inspection, node snapshot,
container filesystem diff (`docker export` / `crictl`), k8s audit logs. Cordon the node, don't delete the pod.

## Logs
Preserve relevant CloudTrail/Activity/Audit logs, flow logs, DNS logs, app logs — extend retention
or copy to the evidence store before they age out.

## Verify
- [ ] Forensics account, KMS key, analysis AMI and runbook ready and tested.
- [ ] Evidence bucket has Object Lock in compliance mode.
