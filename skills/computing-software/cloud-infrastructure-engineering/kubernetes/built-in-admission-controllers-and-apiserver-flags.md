---
id: computing-software.cloud-infrastructure-engineering.kubernetes.built-in-admission-controllers-and-apiserver-flags
name: built-in-admission-controllers-and-apiserver-flags
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, admission-controller, kube-apiserver, noderestriction, alwayspullimages, limitranger, resourcequota, podnodeselector, eventratelimit, serviceaccount-admission, denyserviceexternalips, enable-admission-plugins, disable-admission-plugins, managed-kubernetes, eks, gke, aks]
level: advanced
status: docs-checked
description: "The static, always-on kube-apiserver admission controller chain (NodeRestriction, AlwaysPullImages, LimitRanger...) and which flags managed Kubernetes locks away from you."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/", "https://kubernetes.io/docs/concepts/security/pod-security-admission/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Built-in admission controllers — the chain running before any webhook ever fires

**Goal:** know which security properties come from the *static* admission
controller chain compiled into `kube-apiserver` (no webhook, no extra pod, cannot
be down) versus which require `ValidatingAdmissionPolicy`/Gatekeeper/Kyverno. On
managed Kubernetes (EKS/GKE/AKS) you cannot flip most of these — know which ones
the provider already enables and which gaps you must cover elsewhere. Webhook-based
admission is in
`computing-software.cloud-infrastructure-engineering.kubernetes.admission-webhooks-validating-and-mutating`.

## 1. The chain and how to inspect it
Mutating controllers run first, then validating controllers; the order of names in
`--enable-admission-plugins` does not matter. The API server enables a documented default set
(see the docs page "Admission Controllers Reference") and `--disable-admission-plugins`
switches off any plugin even if it is in that default set.
```bash
kube-apiserver -h 2>&1 | grep -A2 enable-admission-plugins   # see available + defaults
ps aux | grep kube-apiserver | grep -o -- '--enable-admission-plugins=[^ ]*'
```
On a kubeadm cluster, flags live in `/etc/kubernetes/manifests/kube-apiserver.yaml`
and changes take effect on static-pod restart (kubelet watches the file).

## 2. The controllers that actually matter for security
- **NodeRestriction** — limits a kubelet's own credentials to modify only its own
  Node object and Pods bound to it, and blocks it from setting
  `node-restriction.kubernetes.io/`-prefixed labels on itself. Without this, a
  compromised kubelet credential can relabel its node to attract workloads it
  wants to attack, or edit arbitrary Node objects. It also blocks kubelets from setting
  `node-role.kubernetes.io/`-prefixed labels and from deleting their Node object. It is **not** in
  the API server's default plugin list; kubeadm adds it with
  `--enable-admission-plugins=NodeRestriction`. Verify it is enabled on any cluster not built by kubeadm.
- **AlwaysPullImages** — forces every pod to re-pull (and thus re-auth against
  the registry / re-check `imagePullSecrets`) rather than trusting whatever image
  is cached on the node. Without it, a user with only `get pods` (no image-pull
  Secret access) on a node that already cached a private image can schedule a pod
  using that image and read its contents — image pull access becomes irrelevant
  because the pull already happened for someone else. **Off by default** — turn it
  on in multi-tenant clusters.
- **LimitRanger / ResourceQuota** — reject objects violating namespace
  `LimitRange`/`ResourceQuota`; the enforcement half of multi-tenant resource
  isolation (the objects themselves are just configuration without this admission
  controller enabled — but it's on by default).
- **ServiceAccount** — auto-mounts a ServiceAccount and its token if none is
  specified; this is *why* `automountServiceAccountToken: false` must be set
  explicitly per pod/ServiceAccount — the controller's default behavior is to
  attach one.
- **PodNodeSelector / PodTolerationRestriction** — enforce per-namespace required
  node selectors / allowed tolerations, e.g. stop a non-privileged namespace from
  tolerating the taint that lets pods land on GPU or control-plane nodes.
- **DenyServiceExternalIPs** — rejects `Service.spec.externalIPs`, closing an
  path where any user who can create/patch a Service can intercept network traffic by
  setting `externalIPs`. It rejects new uses and new values only (existing uses are
  untouched, removals are allowed). **Disabled by default**; enable it explicitly.
- **EventRateLimit** — caps the API's event-write rate per source; mitigates a
  noisy/compromised component flooding etcd via Events (a cheap DoS vector).
  Requires an `EventRateLimit` configuration referenced from the file given to
  `--admission-control-config-file`, not just a flag. Alpha since v1.13 per the docs.
- **ExtendedResourceToleration**, **PodSecurity** (replaced the removed
  PodSecurityPolicy; implements Pod Security Admission) — `PodSecurity` is stable
  since 1.25, is in the default plugin list, and is what actually enforces the namespace
  `pod-security.kubernetes.io/enforce` labels covered in `k8s-rbac-and-security`.

## 3. What managed Kubernetes changes
- Managed services control the API server flags; check each provider's documentation for
  which admission plugins and flags it exposes (this differs per provider and version).
- Where the provider does not enable something you need, the remaining lever is a
  ValidatingAdmissionPolicy or a validating webhook (Kyverno/Gatekeeper) re-implementing
  the check; a webhook adds an extra hop and can go down.

## Gotchas
- `--disable-admission-plugins` removes plugins even if they are in the default set, and the
  default set changes between releases — check the list for your version rather than assuming.
- `ServiceAccount` auto-mount running *before* your own policy webhook fires means
  a validating webhook that tries to reject "pods with a mounted token" must check
  the final object, not assume the author's YAML reflects what's mounted.
- `PodSecurity` restrictions are applied when pods are created; for Deployments and other
  workload resources only the audit and warn modes apply to the template, enforce applies to
  the resulting pods. Sweep already-running pods separately after a label change.

## Verify
- [ ] `kube-apiserver` process flags (or provider's published list) show
      `NodeRestriction`, `PodSecurity`, `ServiceAccount`, `LimitRanger`,
      `ResourceQuota` enabled — these five are the baseline.
- [ ] `AlwaysPullImages` and `DenyServiceExternalIPs` explicitly checked for and
      enabled (or deliberately compensated for via webhook) in multi-tenant clusters.
- [ ] A test `Service` with `spec.externalIPs` set is rejected.
- [ ] A test pod request with no explicit image-pull policy still forces a fresh
      pull under `AlwaysPullImages` (verify via kubelet pull logs, not just the spec).

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37) and kubeadm source.
Confirmed: default plugin list (NodeRestriction and AlwaysPullImages and DenyServiceExternalIPs are not in it; PodSecurity,
LimitRanger, ResourceQuota, ServiceAccount are); NodeRestriction label rules; kubeadm enables NodeRestriction
(cmd/kubeadm manifests.go); EventRateLimit config via `--admission-control-config-file`; PodSecurity stable v1.25 and
pod-creation scope. Wrong in the original: NodeRestriction "on by default since 1.17". Removed unconfirmed managed-provider specifics.
Method: documentation only; no commands were run.
