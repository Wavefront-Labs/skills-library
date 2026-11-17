---
id: computing-software.cloud-infrastructure-engineering.kubernetes.terraform-cluster-provisioning
name: terraform-cluster-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, terraform, terraform-eks, terraform-kubernetes, infrastructure-as-code, opentofu, gke, aks]
level: practitioner
status: draft
description: "Provision Kubernetes clusters with Terraform modules (terraform-aws-modules/eks, GKE, AKS): state layout, separating cluster from in-cluster resources, and upgrade-safe patterns."
sources: ["https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest", "https://registry.terraform.io/modules/terraform-google-modules/kubernetes-engine/google/latest", "https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs#stacking-with-managed-kubernetes-cluster-resources"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Provisioning clusters with Terraform

## Layering (the rule that saves you)
Do **not** create a cluster and configure the `kubernetes`/`helm` provider from it in the same
root module. The provider is configured at plan time; on first apply or after a cluster
replacement it gets an unknown endpoint and fails or targets the wrong cluster (the provider
docs warn explicitly). Use separate states:
1. `network/` — VPC, subnets, NAT.
2. `cluster/` — control plane, node groups, IAM, add-ons offered by the cloud.
3. `platform/` — bootstrap GitOps (Argo CD/Flux) only; everything else from git.

## EKS example
```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.31"
  cluster_name    = "prod"
  cluster_version = "1.31"
  vpc_id     = data.terraform_remote_state.network.outputs.vpc_id
  subnet_ids = data.terraform_remote_state.network.outputs.private_subnets
  cluster_endpoint_public_access = false
  authentication_mode = "API"
  enable_cluster_creator_admin_permissions = false
  access_entries = { admins = { principal_arn = var.admin_role_arn,
    policy_associations = { admin = { policy_arn = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy", access_scope = { type = "cluster" } } } } }
  cluster_addons = { coredns = {}, kube-proxy = {}, vpc-cni = { before_compute = true }, eks-pod-identity-agent = {} }
  eks_managed_node_groups = {
    system = { instance_types = ["m6i.large"], min_size = 2, max_size = 5, desired_size = 3,
               labels = { pool = "system" } }
  }
}
```
Pin module **and** provider versions; major module bumps (v19→v20) rename resources — read the
UPGRADE doc and use `moved {}` blocks / `terraform state mv`.

## Upgrade pattern
1. Bump `cluster_version` alone, plan (should show only the control plane in-place update),
   apply.
2. Bump add-on versions.
3. Node groups: managed groups roll in place with `update_config`; for risky changes add a new
   group, migrate, remove old.
Ignore `desired_size` drift (`lifecycle { ignore_changes = [scaling_config[0].desired_size] }`)
when the cluster autoscaler owns it — the module does this.

## Gotchas
- `terraform destroy` with LoadBalancer Services/PVCs still in the cluster leaves orphaned
  ELBs/volumes that block VPC deletion. Delete in-cluster LB/PVC first.
- Anything that forces replacement of the cluster (subnet change, name, encryption config on
  some providers) is a new cluster — review plans for `-/+` on the cluster resource; add
  `prevent_destroy`.
- GKE: `remove_default_node_pool = true` + separate `google_container_node_pool`.

## Verify
- [ ] `terraform plan` on a clean checkout is empty.
- [ ] Cluster state has no kubernetes/helm provider resources beyond the GitOps bootstrap.
