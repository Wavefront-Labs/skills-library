---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gke-cluster-creation-protection-and-control-plane-access
name: gke-cluster-creation-protection-and-control-plane-access
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, gcloud-container-clusters-create, terraform-gke-module, deletion-protection, cluster-deletion, dns-endpoint, control-plane-access]
level: practitioner
status: docs-checked
description: "Create GKE clusters reproducibly with gcloud or the Terraform GKE modules, protect them from deletion, and expose the control plane via the IAM-gated DNS endpoint."
sources: ["https://docs.cloud.google.com/kubernetes-engine/docs/how-to/latest/network-isolation", "https://docs.cloud.google.com/kubernetes-engine/docs/concepts/network-isolation", "https://docs.cloud.google.com/sdk/gcloud/reference/container/clusters/create-auto", "https://docs.cloud.google.com/sdk/gcloud/reference/container/clusters/get-credentials", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/managing-clusters", "https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/container_cluster"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GKE cluster creation, deletion protection and control-plane access

## 1. Create with gcloud (Autopilot, private nodes, DNS endpoint)
```bash
gcloud container clusters create-auto prod-eu --project=<P> --region=europe-west2 \
  --release-channel=regular \
  --network=projects/<HOST>/global/networks/prod --subnetwork=projects/<HOST>/regions/europe-west2/subnetworks/gke-prod \
  --cluster-secondary-range-name=pods --services-secondary-range-name=services \
  --enable-private-nodes \
  --enable-dns-access --no-enable-ip-access
```
Standard clusters: `gcloud container clusters create <C> --enable-private-nodes --enable-ip-alias --enable-dns-access --enable-ip-access ...` (`--enable-ip-alias` is required with `--enable-private-nodes`).
Save the exact command (or better, Terraform): the network, secondary ranges and Autopilot-versus-Standard choice are fixed when the cluster is created.

## 2. Create with Terraform
Use the `google_container_cluster` resource from the `hashicorp/google` provider and keep `deletion_protection = true` (the provider's documented default). Terraform refuses to destroy the cluster until that field is false in state.

## 3. Deletion protection — two layers
- Terraform `deletion_protection` only stops Terraform from destroying the cluster; it does not stop deletion through the console or gcloud.
- For a guard that applies outside Terraform, the GKE cluster-management docs describe tagging a cluster and attaching an IAM deny policy so that no one can delete a cluster carrying that tag.

## 4. Control-plane access via the DNS endpoint
The DNS-based endpoint gives each cluster a unique, immutable FQDN under `gke.goog` that resolves to an endpoint reachable from any network that can reach Google Cloud APIs. Access needs a role with the `container.clusters.connect` permission (included in `roles/container.developer` and `roles/container.viewer`).
```bash
gcloud container clusters get-credentials prod-eu --region=europe-west2 --dns-endpoint
gcloud container clusters update prod-eu --region=europe-west2 --enable-dns-access
```
`get-credentials` uses the IP-based endpoint by default while IP access is enabled, so pass `--dns-endpoint`. `--no-enable-ip-access` turns off both the internal and external IP endpoints; keep IP access only if a tool cannot use DNS. To protect the DNS endpoint with VPC Service Controls, add the listed Google APIs to the perimeter's restricted services. Kubernetes ServiceAccount tokens and client certificates over DNS are disabled by default.

## Gotchas
- Secondary range names must exist on the subnet first; a typo fails creation late.
- `--no-enable-ip-access` breaks in-VPC tools that hardcode the private IP; update kubeconfigs.

## Verify
- [ ] `gcloud container clusters describe prod-eu --region=<R>` shows DNS access enabled and IP access disabled.
- [ ] `kubectl get ns` works through the DNS endpoint for an IAM-authorised user and fails for one without `container.clusters.connect`.
- [ ] `terraform plan` shows no drift and a destroy is refused while `deletion_protection` is true.

## Checked

2026-10-24, GKE network-isolation concept and how-to pages, gcloud create-auto and get-credentials references, GKE manage-clusters page and the Terraform google_container_cluster documentation. Confirmed: `--enable-dns-access`, `--enable-ip-access`/`--no-enable-ip-access`, `--enable-private-nodes` requiring `--enable-ip-alias`, `get-credentials --dns-endpoint`, `container.clusters.connect`, the `gke.goog` FQDN, VPC Service Controls support, Terraform `deletion_protection` semantics and the tag-plus-deny-policy approach. Removed unconfirmed claims: the Terraform module block and version, a `--deletion-protection` gcloud flag (none found), the exact deny permission string, the claim that Autopilot cannot convert to Standard.

Method: documentation only; no commands were run.
