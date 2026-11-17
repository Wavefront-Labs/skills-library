---
id: computing-software.devops-ci-cd.argo-cd.multi-cluster-management
name: multi-cluster-management
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd, multi-cluster, cluster-secrets, cluster-registration, argocd-cluster-add, hub-spoke, hub-and-spoke, cluster-labels, cluster-generator, in-cluster, kubernetes-default-svc, bearer-token, exec-provider, eks-iam, gke-workload-identity, aks-azure-workload-identity, cluster-cache, cluster-sharding, argocd-manager, service-account-token, cluster-namespaces, private-cluster-access, agent-based-gitops, argocd-agent, gitops, kubernetes]
level: advanced
status: docs-checked
description: "Run one Argo CD for many clusters: declarative cluster Secrets, auth options (token, EKS IAM, exec provider), namespaced access, controller sharding, hub vs agent."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#clusters", "https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_cluster_add/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/high_availability/", "https://argocd-agent.readthedocs.io/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-cluster management

**Goal:** a hub Argo CD that deploys to N clusters with rotatable credentials, labels you can select on, and a blast radius you have thought about.

## 1. Clusters are Secrets
Cluster credentials are stored as Secrets with the label `argocd.argoproj.io/secret-type: cluster`, in the Argo CD namespace. Data fields:
- `name` and `server` (the API server URL);
- `namespaces` (optional comma-separated list; setting it makes Argo CD ignore cluster-level resources unless `clusterResources` is `"true"`; `clusterResources` only applies when `namespaces` is set);
- `project` (optional, makes the cluster project-scoped);
- `config`, a JSON document with `bearerToken`, `username` / `password`, `awsAuthConfig` (`clusterName`, `roleARN`, `profile`), `execProviderConfig` (`command`, `args`, `env`, `apiVersion`, `installHint`), `proxyUrl`, `tlsClientConfig` (`caData`, `certData`, `keyData`, `insecure`, `serverName`) and `disableCompression`.
Writing the Secret yourself (kept in Git through your secret-management tool) is the declarative route. Further labels on the Secret are ordinary metadata you can use for selection.

`argocd cluster add CONTEXT` is the CLI route. Documented flags include `--name`, `--label`, `--annotation`, `--project`, `--namespace`, `--cluster-resources`, `--in-cluster` (Argo CD lives in that cluster and connects through `kubernetes.default.svc`), `--service-account` (if unset, a default `argocd-manager` service account is created), `--system-namespace` (default `kube-system`), `--shard`, `--exec-command*`, `--aws-cluster-name`, `--aws-role-arn`, `--aws-profile`, `--proxy-url` and `--upsert`.

## 2. Credentials
- Static: `bearerToken` in `config`.
- EKS: `awsAuthConfig` with `clusterName` and `roleARN`. The declarative-setup page covers IRSA, adding the role to the target cluster's `aws-auth` config map, an assume-role policy for the Argo CD pod role, and alternatives where IRSA is not possible (`execProviderConfig` with environment variables, or the AWS profile option from Argo CD 2.10).
- Exec providers: `execProviderConfig` runs a command to supply credentials; that command must exist in the Argo CD image (build your own image). For Azure, the page shows an `argocd-k8s-auth` example, and the `AAD_LOGIN_METHOD` environment variable selects the kubelogin flow (devicecode, spn, ropc, msi, azurecli, workloadidentity).
- Namespaced access: with `namespaces` set, Argo CD performs a separate list/watch per namespace, which can exhaust the Kubernetes client's idle connections; raise `ARGOCD_K8S_CLIENT_MAX_IDLE_CONNECTIONS` on the application controller.

## 3. Scale: sharding
The controller keeps a Kubernetes watch cache per cluster. If it manages too many clusters and uses too much memory, shard clusters across controller replicas: raise `replicas` of the `argocd-application-controller` StatefulSet and set `ARGOCD_CONTROLLER_REPLICAS` to the same number. The `shard` field in a cluster Secret (or `--shard` on add) pins a cluster; otherwise it is calculated. The algorithm is set with `--sharding-method` or, preferably, the `controller.sharding.algorithm` key in `argocd-cmd-params-cm` (also `ARGOCD_CONTROLLER_SHARDING_ALGORITHM`): `legacy` (uid based, non-uniform), `round-robin` (equal distribution) or `consistent-hashing` (bounded-load consistent hashing). The docs mark `round-robin` and `consistent-hashing` as experimental: removing the rank-0 cluster can reshuffle all clusters under round-robin.
The controller polls Git every 3 minutes by default (`timeout.reconciliation` and `timeout.reconciliation.jitter` in `argocd-cm`).

## 4. Topologies
- Hub and spoke: one Argo CD reaches every cluster. Traditional multi-cluster deployments need the control plane to hold connections and credentials for every cluster, which is hard for clusters behind NAT, firewalls or air gaps (the argocd-agent project's description of the problem).
- argocd-agent: agents on workload clusters connect inward to a central control plane, application controllers run where the workloads are, with a single pane of glass. It describes two operational modes and states it is in active development and not yet feature complete; read its feature overview before choosing it.
- One Argo CD per cluster avoids cross-cluster credentials at the price of many instances. These are trade-offs to weigh; the pages read do not rank them.

## Verify
- [ ] Each cluster is a labelled Secret managed from Git, not a one-off `argocd cluster add`.
- [ ] Spoke access is scoped to what the apps need (check the service account's RBAC on the target cluster).
- [ ] Controller replicas and `ARGOCD_CONTROLLER_REPLICAS` match, and clusters spread across shards.

## Checked
2026-11-09. Confirmed against the Argo CD declarative-setup page (cluster Secret label and fields, namespaces/clusterResources, project, config structure, exec command in image, per-namespace watch warning, EKS and Azure notes), the `argocd cluster add` reference (flags), the high-availability page (sharding, algorithms and experimental warning, shard field, Git poll interval) and the argocd-agent landing page (inward connections, status). Removed: the YAML example with placeholder IP, GKE plugin and kubelogin argument values, `kubectl create token` duration advice, ClusterRole least-privilege details, cluster generator and sync-window selection claims, `argocd admin cluster stats`, cluster-cache resync default, `argocd cluster list` status meanings, rotation timing, the hub-vs-per-cluster pros and cons table, the "beta" and 2025 labels for argocd-agent, and the 10-20 cluster threshold.
Method: documentation only; no commands were run.
