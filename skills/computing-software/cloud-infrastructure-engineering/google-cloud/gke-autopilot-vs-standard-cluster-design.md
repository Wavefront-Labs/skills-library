---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gke-autopilot-vs-standard-cluster-design
name: gke-autopilot-vs-standard-cluster-design
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, gke-autopilot, gke-standard, cluster-creation, regional-cluster, zonal-cluster, private-cluster, gke-enterprise, compute-classes, autopilot-pricing, control-plane, cluster-design, kubernetes-engine, gke-cluster]
level: practitioner
status: docs-checked
description: "Choose GKE Autopilot or Standard and create it right: regional control plane, private nodes, VPC-native ranges, Workload Identity, release channel, and the Autopilot constraints that change manifests."
sources: ["https://docs.cloud.google.com/kubernetes-engine/docs/concepts/choose-cluster-mode", "https://docs.cloud.google.com/kubernetes-engine/docs/concepts/autopilot-resource-requests", "https://docs.cloud.google.com/kubernetes-engine/docs/concepts/autopilot-security", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/creating-an-autopilot-cluster", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/flexible-pod-cidr"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GKE Autopilot vs Standard cluster design

**Goal:** a cluster whose operating model matches the team: Autopilot unless you have a reason,
Standard when you do, and in both cases the create command you cannot change later is right.

## 1. Choose
| Need | Autopilot | Standard |
|---|---|---|
| Configuration | pre-configured with Google best practices, runs only Autopilot workloads | you configure Pods in any way you want, including privileged mode, and own node pools |
| Privileged containers | blocked unless deployed by a Google Cloud partner | allowed |
| hostPath, host namespaces | hostPath blocked by default (read-only `/var/log` paths allowed); host namespaces blocked except for verified partners | allowed |
| `CAP_NET_ADMIN` | dropped for all containers (re-enable with `--workload-policies=allow-net-admin`) | allowed |
| Workload types | Autopilot workloads only | both Autopilot and Standard workloads |
| Charges | depend on the mode of operation; see the GKE pricing page | see the GKE pricing page |
Google's guidance: use Autopilot for most workloads unless your application requires privileges; use
Standard for the granular control it provides. For SLA, node limits and pricing, check the current GKE SLA,
quota and pricing pages rather than relying on figures from memory.

## 2. Settings fixed at creation (get them right)
- **Location:** pick a region (or zone for Standard) deliberately; check the location type you need before creating.
- **VPC-native** (alias IP) networking with **pod and service secondary ranges** that will not collide with on-prem. On Standard the maximum pods per node sets the per-node CIDR block (the default of 110 uses a /24; 33-64 uses a /25; 17-32 uses a /26).
- **Private nodes** (`--enable-private-nodes`, which requires `--enable-ip-alias` on Standard): nodes get internal IPs only; egress via Cloud NAT. Control plane access can use authorized networks or the DNS-based endpoint (`--enable-dns-access`).
- **Release channel:** new Autopilot clusters enroll in Regular by default.
- Choose the **cluster name** and **network/subnet** carefully; plan for them to be fixed for the life of the cluster.

```bash
gcloud container clusters create-auto prod-euw1 --location=europe-west1 \
  --network=prod-vpc --subnetwork=prod-euw1-gke \
  --cluster-secondary-range-name=gke-pods --services-secondary-range-name=gke-services \
  --enable-private-nodes --enable-master-authorized-networks --master-authorized-networks=10.0.0.0/8 \
  --release-channel=regular --enable-dns-access
```
Standard: `gcloud container clusters create` with `--enable-ip-alias`, `--workload-pool=<PROJECT_ID>.svc.id.goog` and node pools afterwards (see `gke-node-pools-and-upgrades`).

## 3. Autopilot constraints that change manifests
- General-purpose Pod requests must keep a CPU:memory ratio between 1:1 and 1:6.5. Minimum requests are 50m CPU and 52 MiB on clusters that support bursting, otherwise 250m CPU and 512 MiB.
- Requests equal to limits gives the `Guaranteed` QoS class; with no limits set, Pods may burst where bursting is supported, otherwise GKE sets limits equal to requests.
- The total ephemeral storage request across a Pod's containers must be between 10 MiB and 10 GiB.
- Compute classes: general-purpose (default), `Balanced`, `Performance` and `Scale-Out`; accelerators (GPUs and TPUs) have their own minimums and maximums.
- `cloud.google.com/gke-spot: "true"` in a nodeSelector requests Spot Pods.
- GKE modifies mutating webhooks on Autopilot clusters so they do not intercept resources in managed namespaces such as `kube-system`.

## Gotchas
- Pod secondary range exhaustion is a common reason a cluster cannot scale; size ranges for growth.
- Check what the node count flag means per zone or total for your cluster type before sizing a regional Standard cluster.

## Verify
- [ ] `gcloud container clusters describe` shows the intended location, private nodes, workload identity and release channel.
- [ ] A Deployment without resources on Autopilot gets requests mutated (visible in `kubectl get pod -o yaml`) and a privileged Pod is rejected.

## Checked

2026-10-24, GKE choose-cluster-mode, Autopilot resource-request, Autopilot security, create-Autopilot-cluster and flexible Pod CIDR pages on docs.cloud.google.com. Confirmed: Autopilot guidance and restrictions (privileged, hostPath, host namespaces, CAP_NET_ADMIN, webhooks), CPU:memory ratio, minimum requests, ephemeral storage bounds, QoS behaviour, compute class names, Regular release channel default, pods-per-node to CIDR table. Removed unconfirmed claims: SLA percentages, node-count limits, billing description, Windows/sole-tenant statements, Cloud NAT and finalizer gotchas, GKE Enterprise fee, the `Accelerator` compute class name (not a compute class on the resource-requests page), regional-only claim for Autopilot, `--default-max-pods-per-node` flag name.

Method: documentation only; no commands were run.
