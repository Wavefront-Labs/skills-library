---
id: computing-software.cloud-infrastructure-engineering.terraform.kubernetes-and-helm-provider-exec-auth
name: kubernetes-and-helm-provider-exec-auth
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, exec-plugin, kubeconfig-auth, kubernetes-provider, helm-provider, eks, aks, gke]
level: practitioner
status: docs-checked
description: "Authenticate kubernetes and helm providers with exec plugins (aws eks get-token, gke-gcloud-auth-plugin) instead of static tokens or kubeconfig files."
sources: ["https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs#exec-plugins", "https://registry.terraform.io/providers/hashicorp/helm/latest/docs#exec-plugins", "https://kubernetes.io/docs/reference/access-authn-authz/authentication/#client-go-credential-plugins"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubernetes/helm providers with exec auth

Some cloud providers issue short-lived cluster tokens that expire quickly. The provider
docs recommend an **exec**-based credential plugin, which fetches a new token before each
Terraform operation (kubernetes provider) or before the provider is initialised (helm).

## EKS
```hcl
provider "kubernetes" {
  host                   = data.aws_eks_cluster.this.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.this.certificate_authority[0].data)
  exec {
    api_version = "client.authentication.k8s.io/v1"
    command     = "aws"
    args        = ["eks", "get-token", "--cluster-name", var.cluster_name]
    # env = { AWS_PROFILE = "prod" }     # optional map of environment variables
  }
}

provider "helm" {
  kubernetes = {                # attribute syntax, as in the current helm provider docs
    host                   = data.aws_eks_cluster.this.endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.this.certificate_authority[0].data)
    exec = {
      api_version = "client.authentication.k8s.io/v1beta1"
      command     = "aws"
      args        = ["eks", "get-token", "--cluster-name", var.cluster_name]
    }
  }
}
```

## GKE / AKS
- GKE: `command = "gke-gcloud-auth-plugin"` in the `exec` block (the helm provider docs show it).
- AKS: use whichever credential plugin your cluster's authentication requires; this skill has
  no confirmed `kubelogin` arguments, so copy them from Microsoft's AKS documentation.

## kubeconfig alternative
`config_path = "~/.kube/config"` (or `KUBE_CONFIG_PATH`) + `config_context` (`KUBE_CTX`) — fine
locally, but ties the run to files on the machine. Prefer explicit host/CA + exec in CI.
Do not mix `exec` with other credential attributes such as `token` or `client_certificate`:
the provider docs say the behaviour is undefined.

## Gotchas
- The command must exist on the runner (HCP Terraform agents: custom image).
- The cluster must exist when the provider is configured, so a cluster and its workloads
  in one root module usually need splitting.
- The current helm provider docs use `kubernetes = { ... }` (attribute) where older
  versions used a `kubernetes { }` block; check the docs for your provider version.
- `api_version` is required in `exec` and must match what the plugin emits.

## Verify
- [ ] `aws eks get-token --cluster-name X` returns a credential on the runner.
- [ ] A long apply completes without `Unauthorized` errors.

## Checked
- 2026-10-28. Confirmed against the kubernetes provider docs (`exec` block fetching a new token before each operation, EKS `eks get-token` example with `client.authentication.k8s.io/v1`, `api_version`, `command` required, `args`, `env`, warning not to mix `exec` with `token` or `client_certificate`, `config_path`, `KUBE_CONFIG_PATH`, `config_context`, `KUBE_CTX`) and the helm provider docs (`kubernetes = { exec = { ... } }` attribute syntax, `client.authentication.k8s.io/v1beta1`, `gke-gcloud-auth-plugin` example).
- Removed: the ~15 minute EKS token lifetime, token-stored-in-state claim, the `gcloud components install` command, the AKS `kubelogin` arguments and server ID, Stacks deferral, and the EKS access-entry claim (not in the fetched docs).
Method: documentation only; no commands were run.
