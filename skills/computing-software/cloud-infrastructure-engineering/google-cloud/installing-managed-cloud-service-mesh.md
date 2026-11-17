---
id: computing-software.cloud-infrastructure-engineering.google-cloud.installing-managed-cloud-service-mesh
name: installing-managed-cloud-service-mesh
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, cloud-service-mesh-managed, mesh-install, istio, mtls, fleets]
level: advanced
status: docs-checked
description: "Install managed Cloud Service Mesh on fleet GKE clusters with automatic control and data plane management, enable sidecar injection, turn on strict mTLS and verify."
sources: ["https://docs.cloud.google.com/service-mesh/docs/onboarding/provision-control-plane", "https://docs.cloud.google.com/service-mesh/docs/security/configuring-mtls"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing managed Cloud Service Mesh

## 1. Prerequisites
- Cluster registered to a fleet with Workload Identity; enough node capacity (sidecars add CPU/memory to every pod).
- APIs: `mesh.googleapis.com` in the fleet project.
- Firewall ports must be open for cross-cluster endpoint discovery when several fleet clusters share the mesh; see the provisioning page.

## 2. Enable
```bash
gcloud container fleet mesh enable --project=<FLEET_P>
gcloud container fleet mesh update --management=automatic \
  --memberships=<MEMBERSHIP> --location=<REGION> --project=<FLEET_P>
gcloud container fleet mesh describe --project=<FLEET_P>
# wait for controlPlaneManagement.state: ACTIVE and dataPlaneManagement.state: ACTIVE
```
`automatic` = Google runs and upgrades the control plane following the cluster's GKE release channel (changing the channel is not supported by managed Cloud Service Mesh), and the managed data plane restarts workloads to re-inject new proxy versions after a control plane upgrade, normally within 2 weeks.

## 3. Inject sidecars
```bash
kubectl label namespace payments istio-injection=enabled --overwrite
kubectl rollout restart deploy -n payments
kubectl get pods -n payments -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.spec.containers[*].name}{"\n"}{end}'
```
(Revision-label injection, `istio.io/rev=REVISION_LABEL` taken from the available revisions on your cluster, is the alternative; the provisioning page removes `istio-injection` when setting the revision label, so do not set both.)

## 4. Strict mTLS
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata: {name: default, namespace: istio-system}
spec: {mtls: {mode: STRICT}}
```
The default mode is PERMISSIVE; check that all callers are in the mesh, then set STRICT. A mesh-wide policy has no selector and is applied in the root namespace `istio-system`.

## Gotchas
- Existing workloads in labelled namespaces must be restarted (`kubectl rollout restart deployment -n NAMESPACE`) to get proxies.
- On GKE Standard, if `sidecar.istio.io/proxyCPU` or `proxyMemory` is set, also set the matching `...Limit` annotation or the sidecar limit is unlimited.
- GKE Autopilot is supported (version requirements and default proxy resource requests are on the provisioning page); Autopilot considers only requests.
- Sidecar-inject exceptions (hostNetwork pods, never-ending jobs): look up the current Istio injection annotations before relying on one.

## Verify
- [ ] `gcloud container fleet mesh describe` shows ACTIVE for the membership.
- [ ] Each pod in labelled namespaces has an `istio-proxy` container.
- [ ] A plaintext request from a non-mesh pod to a STRICT namespace fails; meshed traffic succeeds.

## Checked
2026-10-31. Confirmed in the Cloud Service Mesh provisioning and mTLS pages: Workload Identity prerequisite, `mesh.googleapis.com`, `--management automatic`, ACTIVE control and data plane states, release-channel behaviour, data plane restart and 2-week figure, injection label commands, restart command, PeerAuthentication form with PERMISSIVE default and `istio-system` root namespace, Standard sidecar limit note, Autopilot notes; the four fleet mesh gcloud commands via check_commands. Removed: the 15017 port, PDB claim, probe-rewrite claim, native-sidecar advice and the `sidecar.istio.io/inject` exception (not on the pages read).
Method: documentation only; no commands were run.
