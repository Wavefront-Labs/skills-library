---
id: computing-software.cloud-infrastructure-engineering.kubespray.aws-iam-tags-and-dynamic-inventory
name: aws-iam-tags-and-dynamic-inventory
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [aws, iam, tags, dynamic-inventory, cloud-provider, elb]
level: advanced
status: docs-checked
description: "Prepare AWS for Kubespray: IAM roles, cluster tags, VPC DNS, hostname matching, the tag-driven dynamic inventory script and aws_* variables (in-tree provider removed)."
sources:
  - https://kubespray.io/docs/cloud_providers/aws.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Removed note.** The page states that since Kubernetes v1.31 (Kubespray v2.27) the in-tree `cloud_provider` is no longer supported, except the external cloud provider. Treat the `cloud_provider: aws` steps below as applying to older releases.

**Preparation.**
- Before creating instances, create IAM roles and policies for "kubernetes-master" and "kubernetes-node" (policies live under `contrib/aws_iam/`) and associate each instance with its role.
- Tag subnets, route tables and all instances with key `kubernetes.io/cluster/$cluster_name` (unique per cluster). Tag subnets for external ELBs with `kubernetes.io/role/elb` and internal ELBs with `kubernetes.io/role/internal-elb`.
- Enable both DNS Hostnames support and Private DNS on the VPC.
- Make inventory hostnames identical to AWS internal hostnames (like `ip-...us-west-2.compute.internal`) and set `ansible_ssh_host` and `ansible_ssh_user`.

**Dynamic inventory.** Tag instances with `kubespray-role` set to `kube_control_plane`, `etcd` or `kube_node` (roles can be shared, such as `kube_control_plane, etcd`). Copy `kubespray-aws-inventory.py` from `contrib/aws_inventory` into `inventory`, export `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_REGION`, and run with `-i inventory/kubespray-aws-inventory.py`. For public instances prefix `VPC_VISIBILITY="public"`. Node labels and taints come from tags `kubespray-node-labels` (for example `node-role.kubernetes.io/ingress=`) and `kubespray-node-taints` (`node-role.kubernetes.io/ingress=:NoSchedule`).

**Config variables** (all optional): `aws_zone`, `aws_vpc`, `aws_subnet_id`, `aws_route_table_id`, `aws_role_arn`, `aws_kubernetes_cluster_tag`, `aws_kubernetes_cluster_id`, `aws_disable_security_group_ingress` (avoids the 50-rule security group limit), `aws_elb_security_group`, `aws_disable_strict_zone_check` (experimental).

## Checked

Preparation steps, inventory script usage, tags and variable names were confirmed on the AWS page; variable descriptions are condensed.

Method: docs-checked 2026-11-09 against the Kubespray docs/cloud_providers/aws.md page (full file read).
