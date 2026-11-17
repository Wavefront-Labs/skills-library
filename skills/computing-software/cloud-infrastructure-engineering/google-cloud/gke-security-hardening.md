---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gke-security-hardening
name: gke-security-hardening
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, gke-security, gke-hardening, shielded-nodes, private-cluster, binary-authorization, workload-identity, gke-workload-identity, security-posture-dashboard, gke-sandbox, gvisor, node-service-account, metadata-concealment, pod-security-admission, cis-gke-benchmark, authorized-networks, secrets-encryption, application-layer-secrets-encryption]
level: advanced
status: docs-checked
description: "Harden GKE to the CIS benchmark: private nodes, minimal node SA, Workload Identity, Shielded nodes, Binary Authorization, Pod Security admission, KMS secrets encryption, gVisor, posture dashboard."
sources: ["https://docs.cloud.google.com/kubernetes-engine/docs/how-to/shielded-gke-nodes", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/workload-identity", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/encrypting-secrets", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/dataplane-v2", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/sandbox-pods", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/protect-workload-configuration", "https://docs.cloud.google.com/binary-authorization/docs/policy-yaml-reference", "https://docs.cloud.google.com/kubernetes-engine/docs/concepts/network-isolation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GKE security hardening

**Goal:** a cluster where a compromised pod cannot reach the metadata server, steal node
credentials, run an unsigned image, or talk to the internet, and where the posture is measured, not assumed.

## 1. Cluster-level (set at creation where possible)
| Control | Flag / setting | Why |
|---|---|---|
| Private nodes | `--enable-private-nodes` | no node external IPs |
| Control plane access | `--enable-master-authorized-networks` + CIDRs, or the DNS-based endpoint with IAM (`--enable-dns-access`) | restrict who can reach the API server |
| Shielded nodes | `--enable-shielded-nodes --shielded-secure-boot --shielded-integrity-monitoring` | verified boot; Shielded GKE Nodes are on by default (Autopilot cannot override) and Secure Boot is off by default on node pools |
| Workload Identity | `--workload-pool=<PROJECT_ID>.svc.id.goog` and `--workload-metadata=GKE_METADATA` on node pools | pods get their own Google identity without SA keys |
| Minimal node SA | `--service-account=gke-nodes@...` with only the roles nodes need | avoid the Compute Engine default service account |
| Secrets encryption | `--database-encryption-key=projects/<KEY_PROJECT>/locations/<LOC>/keyRings/<RING>/cryptoKeys/<KEY>` | application-layer secrets encryption with Cloud KMS |
| Dataplane V2 | `--enable-dataplane-v2` (only at cluster creation; always on in new Autopilot clusters) | built-in NetworkPolicy enforcement |
| Release channel | `--release-channel=regular` | Google-managed versions |
| Security posture | `--security-posture=standard` (workload configuration auditing is on by default in new clusters from 1.27) | misconfiguration dashboard |

## 2. Workload Identity in practice
```bash
gcloud iam service-accounts add-iam-policy-binding app@<PROJECT_ID>.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="serviceAccount:<PROJECT_ID>.svc.id.goog[payments/app-ksa]"
kubectl annotate sa app-ksa -n payments iam.gke.io/gcp-service-account=app@<PROJECT_ID>.iam.gserviceaccount.com
```
Or skip the GSA entirely: grant IAM directly to `principal://iam.googleapis.com/projects/<NUM>/locations/global/workloadIdentityPools/<PROJECT_ID>.svc.id.goog/subject/ns/payments/sa/app-ksa`. Both the binding and the annotation are required for the GSA method. Test from a pod that it acts as the intended identity, not the node service account.

## 3. Admission: what may run
- **Pod Security admission** (built-in): label namespaces `pod-security.kubernetes.io/enforce: restricted` (`baseline` for legacy apps). Autopilot enforces most of this anyway.
- **Binary Authorization**: policy `defaultAdmissionRule: {evaluationMode: REQUIRE_ATTESTATION, enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG, requireAttestationsBy: [projects/<P>/attestors/<ATTESTOR>]}`. Start with `enforcementMode: DRYRUN_AUDIT_LOG_ONLY` (allows non-conformant images and writes the violation to the audit log) before enforcing. `admissionWhitelistPatterns` with `namePattern` entries exempt images such as system images. Binary Authorization does not enforce init containers. Enable enforcement on the cluster as described in the Binary Authorization GKE guide.
- **Policy Controller** (Gatekeeper-based): constraint templates for rules such as required labels or disallowing hostNetwork.

## 4. Runtime isolation and egress
- **GKE Sandbox (gVisor)**: `--sandbox=type=gvisor` on a node pool; pods set `runtimeClassName: gvisor`. For untrusted code. It has limitations such as GPU and TPU support, and on Standard you need at least one extra node pool that does not use GKE Sandbox for system workloads.
- Default-deny egress `NetworkPolicy` per namespace with explicit allows to DNS and required dependencies.

## 5. Measure
- Use the security posture dashboard in the console for workload configuration findings, and review the GKE security documentation for the current vulnerability scanning and threat detection options.

## Gotchas
- Workload Identity needs `--workload-metadata=GKE_METADATA` on each Standard node pool; a pool without it does not use the GKE metadata server.
- Dataplane V2 can only be enabled when you create a cluster, and toggling NetworkPolicy enforcement on a Dataplane V2 cluster is rejected.
- The Cloud KMS key for `--database-encryption-key` must be in the same region as the cluster, and the Kubernetes Engine Service Agent (`service-<CLUSTER_PROJECT_NUMBER>@container-engine-robot.iam.gserviceaccount.com`) needs `roles/cloudkms.cryptoKeyEncrypterDecrypter` on the key before you enable the feature.

## Verify
- [ ] A Pod acts as the intended Google identity, not the node service account.
- [ ] An image without the required attestation is rejected (or audit-logged in dry-run mode).
- [ ] A `privileged: true` pod is rejected in a `restricted` namespace.
- [ ] The security posture dashboard shows no unaccepted high-severity findings.

## Checked

2026-10-24, GKE Shielded Nodes, Workload Identity Federation, secrets encryption, Dataplane V2, GKE Sandbox, workload configuration auditing and network-isolation pages plus the Binary Authorization policy YAML reference on docs.cloud.google.com. Confirmed: the flags in the control table (`--enable-shielded-nodes`, `--workload-pool`, `--database-encryption-key` format, `--enable-dataplane-v2`, `--security-posture=standard`, `--sandbox=type=gvisor`), KMS location and service agent role requirement, Dataplane V2 creation-only and Autopilot default, Binary Authorization policy fields and enforcement mode values. Removed unconfirmed claims: `--binauthz-evaluation-mode` value, `--workload-vulnerability-scanning`, gVisor overhead, private.googleapis.com range, Security Command Center finding names, kube-bench and CIS statements, metadata concealment wording, legacy ABAC row.

Method: documentation only; no commands were run.
