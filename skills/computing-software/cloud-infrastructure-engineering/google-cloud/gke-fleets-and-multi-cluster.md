---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gke-fleets-and-multi-cluster
name: gke-fleets-and-multi-cluster
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, gke-fleet, fleet, multi-cluster, config-sync, policy-controller, cloud-service-mesh, anthos, gke-enterprise, multi-cluster-ingress, multi-cluster-gateway, multi-cluster-services, mcs, serviceexport, fleet-workload-identity, team-scopes, connect-gateway, attached-clusters, gitops]
level: advanced
status: docs-checked
description: "Run many GKE clusters as one fleet: registration, Config Sync, Policy Controller, multi-cluster Services and Gateway, Connect gateway and team scopes."
sources: ["https://cloud.google.com/kubernetes-engine/fleet-management/docs/fleet-concepts", "https://cloud.google.com/kubernetes-engine/enterprise/config-sync/docs/overview", "https://cloud.google.com/kubernetes-engine/enterprise/policy-controller/docs/overview", "https://cloud.google.com/kubernetes-engine/docs/concepts/multi-cluster-services", "https://cloud.google.com/kubernetes-engine/docs/how-to/deploying-multi-cluster-gateways", "https://cloud.google.com/kubernetes-engine/enterprise/multicluster-management/gateway"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GKE fleets and multi-cluster

**Goal:** N clusters (regions, environments, even on-prem) that share identity, configuration,
policy and a single north-south entry point, managed from one project without N kubeconfigs.

## 1. Fleet basics
- A **fleet** is a project-scoped grouping (`gcloud container fleet`), one fleet per project, clusters from other projects can register into it. Pattern: a fleet host project per environment.
- Register: `gcloud container fleet memberships register prod-euw1 --gke-cluster=europe-west1/prod-euw1 --enable-workload-identity`. GKE clusters can also be fleet-registered at creation (`gcloud container clusters create --fleet-project`).
- **Sameness**: the fleet assumes a namespace/service name means the same thing in every cluster. Design namespaces accordingly before you enable multi-cluster features.
- **Fleet Workload Identity**: `<FLEET_PROJECT>.svc.id.goog` pool; services in a fleet share a common identity pool, so IAM policy can be written once for a set of same-named workloads (identity sameness: keep namespaces and service accounts consistent).
- **Connect gateway**: `gcloud container fleet memberships get-credentials prod-euw1` gives kubectl access through Google's control plane via IAM and RBAC (see the Connect gateway page for the required roles), without direct network access to the cluster. Good for CI.

## 2. Config Sync (GitOps across the fleet)
Config Sync reconciles clusters to a central source of truth (a Git repository, OCI image or Helm chart), with configuration defined across the fleet and applied locally in each member cluster. Enable and configure it per the Config Sync documentation; the `gcloud container fleet config-management` group exposes `describe` and `disable`. Use fleet-level defaults so new memberships inherit, and keep team repos separate from the platform repo. Config Sync and Policy Controller can use namespace sameness to select the same namespace across clusters.

## 3. Policy Controller
`gcloud container fleet policycontroller enable --memberships=...`: based on Open Policy Agent Gatekeeper, with prebuilt policy bundles and a constraint template library; supports audit and admission control, so audit before enforcing. `--audit-interval` sets the audit period and `--referential-rules` enables referential constraints.

## 4. Multi-cluster traffic
- **Multi-cluster Services (MCS)**: `gcloud container fleet multi-cluster-services enable`; a `ServiceExport` in cluster A creates a `ServiceImport` in the other clusters of the fleet.
- **Multi-cluster Gateway**: `gcloud container fleet ingress enable --config-membership=<CONFIG_CLUSTER>`; use a `-mc` GatewayClass such as `gke-l7-global-external-managed-mc` in the config cluster; `HTTPRoute` `backendRefs` target `ServiceImport` objects. Traffic goes from the load balancer directly to Pod IPs. Remove a `ServiceExport` to take a cluster out of rotation.
- **Cloud Service Mesh**: forms a service mesh across clusters in the same fleet (see the Cloud Service Mesh docs for enrolment).

## 5. Team scopes (Enterprise)
`gcloud container fleet scopes create payments`, then namespaces and RBAC role bindings under the scope: a team gets the same namespaces across clusters without cluster-admin (see "Manage teams for your fleet").

## Gotchas
- Config Sync needs reachability from the cluster to its source; private nodes need Cloud NAT or a private endpoint.
- Check the multi-cluster Services and multi-cluster Gateway pages for network and firewall prerequisites before enabling them.

## Verify
- [ ] `gcloud container fleet memberships list` shows every cluster; `get-credentials` through Connect gateway works.
- [ ] A commit to the source of truth is applied to the targeted clusters.
- [ ] `ServiceImport` appears in cluster B after `ServiceExport` in A; cross-cluster curl to the imported service succeeds.
- [ ] Removing a `ServiceExport` takes that cluster out of the multi-cluster Gateway backends.

## Checked

2026-10-27. Confirmed: one fleet per project (fleet concepts), sameness and identity sameness, `clusters create --fleet-project`, `memberships get-credentials` through Connect gateway, Config Sync sources (Git, OCI, Helm), Policy Controller basis, bundles, `--audit-interval` and `--referential-rules` on the policycontroller enable page, `-mc` GatewayClasses and direct-to-Pod traffic, `fleet ingress enable`, `multi-cluster-services enable`, `scopes create`. Removed: `config-management apply`/`status` and the `acm.yaml` example (reference pages 404), `--policy-bundles` (not a flag of policycontroller enable), `--management`, `roles/gkehub.gatewayEditor`, bundle version names, `referentialRulesEnabled`, GKE Enterprise billing remark, DNS suffix and unconfirmed gotchas.

Method: documentation only; no commands were run.
