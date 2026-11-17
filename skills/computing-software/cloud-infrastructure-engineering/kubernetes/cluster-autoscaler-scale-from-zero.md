---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cluster-autoscaler-scale-from-zero
name: cluster-autoscaler-scale-from-zero
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cluster-autoscaler, scale-from-zero, node-groups, asg-tags]
level: practitioner
status: docs-checked
description: "Make Cluster Autoscaler scale node groups up from zero: node template labels, taints and resources via ASG tags or provider APIs, and GPU caveats."
sources: ["https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/README.md", "https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/clusterapi/README.md", "https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/azure/README.md", "https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster Autoscaler: scale from zero

With nodes present, CA learns a group's labels, taints and allocatable from a real node. At
zero nodes it must build a template from provider metadata. If the template lacks the label a
pending pod selects on, CA decides the group cannot help (`NotTriggerScaleUp`).

## AWS ASG tags
```
k8s.io/cluster-autoscaler/enabled = true
k8s.io/cluster-autoscaler/<cluster> = owned
k8s.io/cluster-autoscaler/node-template/label/workload = batch
k8s.io/cluster-autoscaler/node-template/label/nvidia.com/gpu.present = true
k8s.io/cluster-autoscaler/node-template/taint/nvidia.com/gpu = true:NoSchedule
k8s.io/cluster-autoscaler/node-template/resources/nvidia.com/gpu = 1
k8s.io/cluster-autoscaler/node-template/resources/ephemeral-storage = 100G
```
CPU, memory and GPU resources are derived from the instance type in the launch configuration or
template (for mixed instances policies, only the first instance type is used). The label, taint
and resource tags are only needed when scaling up from 0 nodes. EKS managed node groups: with the
`eks:DescribeNodegroup` permission CA can pull labels and taints from the EKS API, but only for a
managed node group created with 0 nodes that has never had nodes; an EKS label wins over an ASG
tag with the same key.

## Other providers
- Azure VMSS: tags `k8s.io_cluster-autoscaler_node-template_label_<name>`,
  `k8s.io_cluster-autoscaler_node-template_taint_<name>` and
  `k8s.io_cluster-autoscaler_node-template_resources_<resource>` (a slash in a label key is written as
  an underscore in the tag name).
- Cluster API: if the infrastructure provider does not support scale from zero, annotate the
  MachineDeployment (or MachineSet) with `capacity.cluster-autoscaler.kubernetes.io/memory` and
  `.../cpu` (both required), optionally `.../ephemeral-disk`, `.../maxPods` (default 110),
  `.../gpu-type` or `.../dra-driver`, `.../gpu-count`, `.../labels` and `.../taints`.

## GPU caveat
On AWS the GPU resources come from the instance type; other extended resources can be declared
with a `node-template/resources/<name>` tag. With Cluster API use the `gpu-type` (device plugin)
or `dra-driver` annotation together with `gpu-count`.

## Verify
```bash
kubectl -n kube-system logs deploy/cluster-autoscaler
kubectl get events --field-selector reason=TriggeredScaleUp
```
Test by scaling the group to 0 and creating a pod that selects only it.

## Checked

Checked 2026-10-24. The documentation checked is the Cluster Autoscaler FAQ and provider READMEs in kubernetes/autoscaler (master, 2026-10-24); the autoscaler binary source now lives in kubernetes-sigs/cluster-autoscaler.
- AWS ASG tag formats for `node-template/label/`, `taint/` (`<value>:<effect>`) and `resources/` (for example `ephemeral-storage`), auto-discovery tags `k8s.io/cluster-autoscaler/enabled` and `k8s.io/cluster-autoscaler/<cluster-name>`, resources derived from the instance type, the EKS DescribeNodegroup behaviour and precedence: AWS README.
- Azure VMSS tag names: Azure README ("Scaling a VMSS node group to and from 0"). Cluster API annotations and the default `maxPods` of 110: Cluster API README.

Method: documentation only; no commands were run.
