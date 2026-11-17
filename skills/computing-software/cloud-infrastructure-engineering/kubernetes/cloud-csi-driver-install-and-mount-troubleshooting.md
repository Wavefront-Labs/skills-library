---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cloud-csi-driver-install-and-mount-troubleshooting
name: cloud-csi-driver-install-and-mount-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, csi, csi-driver-install, ebs-csi-install, csi-troubleshooting, failedmount, mount-failure, failedattachvolume, workload-identity]
level: practitioner
status: docs-checked
description: "Install a cloud block CSI driver (EBS, PD, Azure Disk) with workload identity and troubleshoot FailedAttachVolume/FailedMount via controller and node plugin logs."
sources: ["https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/docs/install.md", "https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/docs/parameters.md", "https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/docs/faq.md", "https://kubernetes-csi.github.io/docs/troubleshooting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud CSI driver install and mount/attach troubleshooting

## Install (EBS example; other cloud drivers are analogous)
The EBS CSI driver can be installed with Kustomize, Helm or as an Amazon EKS managed add-on. IAM: the project's example policy and the AWS-managed policy `AmazonEBSCSIDriverPolicyV2` (ARN `arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicyV2`) scope permissions to volumes and snapshots tagged `ebs.csi.aws.com/cluster: true`, a tag the driver applies to dynamically provisioned resources; statically imported volumes must be tagged manually. EKS Pod Identity is the recommended way to give the controller credentials: assign the role to the `ebs-csi-controller-sa` service account (IRSA via `controller.serviceAccount.annotations` is the alternative).
```bash
helm repo add aws-ebs-csi-driver https://kubernetes-sigs.github.io/aws-ebs-csi-driver
helm repo update
helm upgrade --install aws-ebs-csi-driver aws-ebs-csi-driver/aws-ebs-csi-driver --namespace kube-system
# EKS managed add-on with Pod Identity (shorthand serviceAccount, roleArn):
aws eks create-addon --cluster-name <cluster> --addon-name aws-ebs-csi-driver \
  --pod-identity-associations serviceAccount=ebs-csi-controller-sa,roleArn=<role-arn>
```
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata: {name: gp3}
provisioner: ebs.csi.aws.com
parameters: {type: gp3, encrypted: "true"}
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```
`type` accepts io1, io2, gp2, gp3, sc1, st1, standard and defaults to gp3; `iops`, `iopsPerGB` and `throughput` (gp3 only, default 125 MiB/s) are optional. For GKE and AKS use their current docs for the built-in driver names and settings.

## Components to check
- **Controller** Deployment `ebs-csi-controller`: containers `ebs-plugin`, `csi-provisioner`, `csi-attacher`, `csi-resizer`, `csi-snapshotter`.
- **Node** DaemonSet `ebs-csi-node`, which stages and mounts volumes on each node.
```bash
kubectl get csidriver
kubectl get csinode <node> -o yaml
kubectl -n kube-system logs deploy/ebs-csi-controller -c csi-provisioner --tail=50
kubectl -n kube-system logs deploy/ebs-csi-controller -c csi-attacher --tail=50
kubectl -n kube-system logs deploy/ebs-csi-controller -c ebs-plugin --tail=50
kubectl -n kube-system logs ds/ebs-csi-node -c ebs-plugin --tail=50
kubectl get volumeattachment
```
`csinode` shows whether the driver registered on the node and its allocatable volume count. On Kubernetes 1.34 and later the beta `MutableCSINodeAllocatableCount` feature lets the kubelet re-query the node plugin for the limit (the EBS FAQ explains its requirements).

## Symptoms and likely causes
| Event | Likely cause |
|---|---|
| PVC Pending, waiting for external provisioner | controller not running or lacking permission; read `csi-provisioner` and `ebs-plugin` logs |
| `FailedAttachVolume` ... in use | still attached to another node (see `multi-attach-and-stuck-volumeattachment`) |
| `FailedAttachVolume` timeout or limit errors | attacher cannot reach the API, or the node's volume attach limit is reached (`csinode`) |
| `FailedMount ... not found in the list of registered CSI drivers` | node plugin not running or not registered on that node (taints, crash loop) |
| mount failures | read the node plugin logs on the affected node |

## Verify
- [ ] A test PVC and Pod bind, write, and survive rescheduling.
- [ ] `csinode` shows the driver on every node.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) plus the named upstream project docs and Kubernetes source. Confirmed: EBS CSI install options, AmazonEBSCSIDriverPolicyV2, Pod Identity service account, StorageClass parameters and defaults, chart deployment and container names, EKS create-addon podIdentityAssociations shape in botocore.

Method: documentation only; no commands were run.
