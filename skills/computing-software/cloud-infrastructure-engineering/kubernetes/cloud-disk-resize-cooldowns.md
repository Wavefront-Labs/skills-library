---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cloud-disk-resize-cooldowns
name: cloud-disk-resize-cooldowns
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, volume-expansion, ebs-modify-cooldown, ebs, pvc-resize, cloud-limits]
level: practitioner
status: gated
description: "Plan PVC expansions around cloud disk modification limits (EBS modification rate limits, no shrinking, size caps) and recover when a resize is rejected."
sources: ["https://docs.aws.amazon.com/ebs/latest/userguide/ebs-modify-volume.html", "https://docs.aws.amazon.com/ebs/latest/userguide/general-purpose.html", "https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/docs/modify-volume.md", "https://learn.microsoft.com/en-us/azure/virtual-machines/linux/expand-disks", "https://kubernetes.io/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims", "https://cloud.google.com/compute/docs/disks/resize-persistent-disk"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud disk resize limits

## AWS EBS
- After a modification (size, type, IOPS or throughput) you must wait for it to reach
  `completed` before starting another on the same volume, and you can modify a volume at most
  four times in a rolling 24-hour period; exceeding that returns an error saying when the next
  modification is allowed. A modification can take minutes to hours, but a size increase takes
  effect once it reaches `optimizing`.
- The EBS CSI driver notes that modifications started during a cooldown do not progress until
  it ends, so a PVC resize or VolumeAttributesClass change can sit pending.
- Sizes only grow (no decrease). gp3 volumes range from 1 GiB to 64 TiB (16 TiB on Outposts);
  gp2 up to 16 TiB.
```bash
aws ec2 describe-volumes-modifications --volume-ids <vol-id> \
  --query 'VolumesModifications[0].[ModificationState,StartTime,Progress]'
```

## GCE PD / Hyperdisk
Size can grow at any time with no cooldown, Hyperdisk performance changes have their own rate
limits, and disks cannot shrink (gated: unconfirmed, source is paywalled or blocked). Google
Compute Engine documentation is not in a readable source repository for this review, so confirm
these limits in the persistent disk resize docs.

## Azure Disk
Data disks can be expanded without deallocating the VM, with exceptions: a Standard HDD,
Standard SSD or Premium SSD of 4 TiB or less must be detached (VM deallocated) to grow beyond
4 TiB, while Premium SSD v2 and Ultra Disks are exempt. Shrinking is not supported.

## Planning
- Grow in generous steps instead of small repeated bumps, so you stay well inside the
  modification rate limit.
- Combine size and performance changes into one window (VolumeAttributesClass for IOPS and
  throughput plus the PVC size), since each counts as a modification.
- Alert well before volumes fill (kubelet volume usage metrics) so there is time to wait out a
  limit.

## Recovering a failed resize
If the requested size cannot be satisfied, Kubernetes keeps retrying. You can lower
`spec.resources.requests.storage` to a smaller value than the failed request, as long as it is
still above `.status.capacity` (`RecoverVolumeExpansionFailure`, stable since 1.34), and watch
`.status.allocatedResourceStatuses` and PVC events. A PVC never shrinks below its current size.

## Verify
`kubectl get pvc <n> -o jsonpath='{.status.capacity.storage}'` equals the request and `df -h`
inside the pod shows the new size.

## Checked
Checked 2026-10-27 against the Amazon EBS User Guide (Elastic Volumes considerations and
limitations: wait for `completed`, four modifications per rolling 24 hours, size effective at
`optimizing`, no decrease; General Purpose volumes: gp3 1 GiB to 64 TiB, 16 TiB on Outposts, gp2
up to 16 TiB), the AWS EBS CSI driver volume modification doc (cooldown behaviour), the Azure
"Expand virtual hard disks on a Linux VM" page and its expand-without-downtime restrictions
(4 TiB boundary, Premium SSD v2/Ultra exempt, no shrinking), and kubernetes/website Persistent
Volumes and the RecoverVolumeExpansionFailure feature-gate page (alpha 1.23, beta 1.32, stable
1.34). Corrected the stale six-hour EBS cooldown (now up to four modifications per rolling
24 hours) and the gp3 size cap (64 TiB, not 16 TiB); removed unconfirmed error strings, metric
names and the 75-80 % alert figure. GCE claims are gated because Google docs were not readable.

Method: documentation only; no commands were run.
