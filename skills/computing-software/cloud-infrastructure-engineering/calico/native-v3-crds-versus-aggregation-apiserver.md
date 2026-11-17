---
id: computing-software.cloud-infrastructure-engineering.calico.native-v3-crds-versus-aggregation-apiserver
name: native-v3-crds-versus-aggregation-apiserver
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [install, native-crds, apiserver, v3, crd, gitops, admission-policy, kubectl]
level: advanced
status: docs-checked
description: "Choose between native projectcalico.org/v3 CRDs (Kubernetes 1.34+) and the aggregation API server, and how the mode is auto-detected."
sources:
  - https://docs.tigera.io/calico/latest/operations/native-v3-crds
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
New installs default to native `projectcalico.org/v3` CRDs: Calico resources are CRDs themselves, with no aggregation API server. The older mode serves v3 through an aggregation API server and stores resources internally as `crd.projectcalico.org/v1` CRDs. The aggregation server remains supported for now but is slated for removal.

**Benefits listed:** simpler architecture, GitOps friendliness (no ordering dependency between CRDs and an API server, so Argo CD and Flux can apply in any order), no host-network pod requirement, `kubectl` works directly, and Kubernetes-native validation (CEL rules in the CRD schemas) with MutatingAdmissionPolicies for defaulting.

**How the mode is chosen.** Calico auto-detects at startup from the CRDs present: `projectcalico.org/v3` CRDs mean native mode; `crd.projectcalico.org/v1` CRDs mean API-server mode. The `APIServer` custom resource is still created in native mode, but it deploys a webhooks pod for validation and defaulting instead of the aggregation server.

**Requirements.** A fresh install (migrating an existing cluster has its own page), and Kubernetes 1.34 or later: the beta `admissionregistration.k8s.io/v1beta1` API on 1.34 and 1.35, GA `v1` on 1.36 and later.

**Install notes.** Use the v3 CRD chart or `v3_projectcalico_org.yaml` manifest instead of the v1 equivalents and never install both. Then install the Tigera Operator as normal. API-server mode is the default installation, which uses the `crd.projectcalico.org/v1` CRD chart or manifest.

## Checked

Read in full on 2026-11-08: the Native v3 CRDs page. The mode description, benefits, auto-detection, Kubernetes version requirements and the do-not-install-both note match it. A remark on how API-server mode is selected was reworded to what the page states.

Method: documentation only; no commands were run.
