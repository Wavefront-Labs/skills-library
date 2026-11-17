---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-ec2nodeclass-block-devices-and-instance-store
name: karpenter-ec2nodeclass-block-devices-and-instance-store
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [blockdevicemappings, ebs, instancestorepolicy, raid0, gp3, kms, bottlerocket, instance-store]
level: advanced
status: docs-checked
description: "Block device mappings and defaults per AMI family, EBS fields, and instanceStorePolicy RAID0 setup on AL2, AL2023 and Bottlerocket (device /dev/md/0, mount /mnt/k8s-disks/0)."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeclasses.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EC2NodeClass storage: blockDeviceMappings and instanceStorePolicy

`blockDeviceMappings` overrides default EBS volumes. Fields under `ebs`: `volumeSize`, `volumeType`, `iops`, `encrypted`, `kmsKeyID`, `deleteOnTermination`, `throughput`, `snapshotID`, `volumeInitializationRate`.

```yaml
blockDeviceMappings:
  - deviceName: /dev/xvda
    ebs: {volumeSize: 100Gi, volumeType: gp3, iops: 10000, encrypted: true, throughput: 125}
```

Defaults when unset:
- AL2 and AL2023: `/dev/xvda`, 20Gi gp3 encrypted.
- Bottlerocket: `/dev/xvda` 4Gi (OS) plus `/dev/xvdb` 20Gi (images and logs), gp3 encrypted.
- Windows2019/2022/2025: `/dev/sda1`, 50Gi gp3 encrypted.
- Custom: none.

`instanceStorePolicy: RAID0` makes allocatable ephemeral-storage equal the instance-store total. By default instance-store is ignored. The disks must back kubelet and containerd; without the policy, pods requesting ephemeral-storage may deadlock on insufficient storage even if you RAID the disks yourself.
- AL2: bootstrap arg `--local-disks raid0`; device `/dev/md/0`, mount `/mnt/k8s-disks/0`.
- AL2023: configured via the generated NodeConfig; same device and mount.
- Bottlerocket (v1.22.0+): bootstrap commands added automatically; do not set ephemeral storage in userData.
- Others: configure yourself (see amazon-eks-ami setup-local-disks).

## Checked

2026-11-04. Confirmed against the NodeClasses concept page (v1.13) (identifiers, defaults, limits and prose). Removed the unconfirmed root volume advice.

Method: documentation only; no commands were run.
