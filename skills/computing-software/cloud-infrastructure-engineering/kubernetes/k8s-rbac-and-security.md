---
id: computing-software.cloud-infrastructure-engineering.kubernetes.k8s-rbac-and-security
name: k8s-rbac-and-security
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, rbac, role, clusterrole, rolebinding, clusterrolebinding, serviceaccount, kubectl-auth-can-i, least-privilege, pod-security-standards, pod-security-admission, restricted, baseline, securitycontext, runasnonroot, readonlyrootfilesystem, capabilities, seccomp, secrets, encryption-at-rest, external-secrets, workload-identity, irsa, validatingadmissionpolicy, cel, kyverno, gatekeeper, opa, audit-logging, cis-benchmark, kube-bench]
level: advanced
status: docs-checked
description: "Lock down Kubernetes: least-privilege RBAC and ServiceAccounts, Pod Security Standards, hardened securityContext, Secrets handling, and admission policy with CEL."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/rbac/", "https://kubernetes.io/docs/concepts/security/rbac-good-practices/", "https://kubernetes.io/docs/concepts/security/pod-security-standards/", "https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/", "https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/", "https://kubernetes.io/docs/concepts/security/service-accounts/", "https://www.cisecurity.org/benchmark/kubernetes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes RBAC and security — who can do what, and what pods may do

**Goal:** humans and workloads hold only the API permissions they need, no pod can escalate
to the node, and policy is enforced at admission rather than by review. Network isolation
is in `computing-software.cloud-infrastructure-engineering.kubernetes.k8s-networking-and-ingress`;
image scanning and signing in `computing-software.cloud-infrastructure-engineering.docker.container-image-security-scanning`.

## 1. RBAC mechanics
- **Role** (namespaced) / **ClusterRole** (cluster-wide or reusable) list `apiGroups`,
  `resources`, `verbs`. **RoleBinding** grants within one namespace — it may reference a
  ClusterRole, which is the standard way to reuse one definition across namespaces.
- RBAC is purely additive; there is no deny.
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata: {name: configmap-reader, namespace: shop}
rules:
- apiGroups: [""]
  resources: [configmaps]
  resourceNames: [api-config]        # narrow to specific objects where possible
  verbs: [get, watch]
```
- Test, do not guess: `kubectl auth can-i --list --as=system:serviceaccount:shop:api -n shop`;
  `kubectl auth can-i create pods --as=jane --as-group=dev -n shop`.

## 2. Dangerous permissions (treat as cluster-admin equivalents)
- `create pods` (or any workload kind) in a namespace = access to every Secret and
  ServiceAccount usable there.
- `get/list/watch secrets` — `list` returns the contents, not just names.
- `escalate`, `bind`, `impersonate`, `*` on anything; `nodes/proxy`; `create` on
  `serviceaccounts/token`; write on `mutatingwebhookconfigurations`.
- Wildcards also match resources added in future versions.
- Audit with `kubectl get clusterrolebindings -o wide | grep -E 'cluster-admin|system:masters'`.

## 3. ServiceAccounts
- One ServiceAccount per workload; never run apps as `default`.
- `automountServiceAccountToken: false` on pods that do not call the API (most of them).
- Since v1.22 Pods get a short-lived, automatically rotating token through the TokenRequest API as a
  projected volume; before v1.24 a permanent token Secret was created for every ServiceAccount, and
  manually created long-lived token Secrets are not recommended.
- For cloud access use workload identity (EKS Pod Identity/IRSA, GKE Workload Identity,
  Azure Workload Identity) — never static cloud keys in Secrets.

## 4. Pod Security Standards
Label namespaces for Pod Security Admission:
```bash
kubectl label ns shop pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/warn=restricted pod-security.kubernetes.io/audit=restricted
```
Roll out with `warn`/`audit` first, read the warnings, then `enforce`. `restricted` requires:
```yaml
securityContext:              # pod level
  runAsNonRoot: true
  runAsUser: 10001
  seccompProfile: {type: RuntimeDefault}
containers:
- securityContext:
    allowPrivilegeEscalation: false
    readOnlyRootFilesystem: true      # not required by restricted, but recommended
    capabilities: {drop: [ALL]}
```
- `readOnlyRootFilesystem` needs an `emptyDir` for `/tmp` and any cache dirs.
- `runAsNonRoot` fails at start if the image uses a named non-numeric `USER`.
- `privileged`, `hostPath`, `hostNetwork`, `hostPID` = node compromise; restrict to
  `kube-system`-style namespaces labelled `privileged`.

## 5. Secrets
- Secrets are stored unencrypted in etcd by default (the data field is only base64-encoded). Enable
  **encryption at rest** (the API supports a KMS v2 provider, stable from Kubernetes 1.29) and
  restrict `get/list secrets` tightly.
- Source them from a vault with External Secrets Operator or the Secrets Store CSI driver;
  keep only references in Git (or Sealed Secrets/SOPS for encrypted-in-Git).
- Mounted Secret volumes are updated by the kubelet when the Secret changes, except `subPath`
  mounts, which do not receive updates. Applications must still avoid logging secret values.

## 6. Admission policy
- **ValidatingAdmissionPolicy** (CEL, GA in 1.30) for in-tree rules with no webhook:
```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata: {name: require-digest}
spec:
  matchConstraints: {resourceRules: [{apiGroups: ["apps"], apiVersions: ["v1"], operations: [CREATE, UPDATE], resources: [deployments]}]}
  validations:
  - expression: "object.spec.template.spec.containers.all(c, c.image.contains('@sha256:'))"
    message: "images must be pinned by digest"
```
  (needs a `ValidatingAdmissionPolicyBinding` to take effect).
- **MutatingAdmissionPolicy** (CEL, stable in 1.36) covers in-tree mutation; **Kyverno** and
  **Gatekeeper** are third-party policy engines, so check their own docs for features beyond CEL.
- Webhooks with `failurePolicy: Fail` that go down block all matching writes — exclude
  `kube-system` and run them highly available.

## Gotchas
- `system:masters` group membership bypasses RBAC entirely and cannot be revoked by RBAC;
  never issue client certs with it except break-glass.
- Deleting a RoleBinding does not revoke tokens already issued; it revokes the *permission*.
- Aggregated ClusterRoles (`aggregate-to-edit`) silently grant CRD permissions to `edit` users.
- Exact PSS field requirements change between versions; check the doc for your cluster minor.

## Verify
- [ ] `kubectl auth can-i --list` for each app ServiceAccount shows only intended verbs.
- [ ] No non-system subject is bound to `cluster-admin`; break-glass is documented.
- [ ] All app namespaces enforce `restricted` (or `baseline` with a written exception).
- [ ] A test pod with `privileged: true` is rejected in an app namespace.
- [ ] `kube-bench` (CIS) shows no failing control you have not accepted in writing.
- [ ] API audit logging is on and Secret reads are queryable.

## Checked

2026-10-27. Release: Kubernetes v1.37 docs (kubernetes/website main), October 2026
- Confirmed in RBAC Good Practices: `list`/`watch` on Secrets reveal contents, workload creation grants access to Secrets, the `escalate`, `bind`, `impersonate` verbs, `nodes/proxy` (including `get`), `create` on `serviceaccounts/token`, control of webhook configurations, wildcards covering future resources, and `system:masters` bypassing RBAC irrevocably.
- Confirmed ValidatingAdmissionPolicy is stable since v1.30 and needs a binding; MutatingAdmissionPolicy is stable and enabled by default from v1.36 (feature-gate page); confirmed webhook `failurePolicy` defaults to `Fail`.
- Confirmed Pod Security Standards `restricted` requirements (runAsNonRoot, allowPrivilegeEscalation false, drop ALL, seccomp) and that `readOnlyRootFilesystem` is not among them; confirmed the ServiceAccount token behaviour (v1.22 TokenRequest, v1.24 no automatic token Secrets), Secrets stored unencrypted by default, KMS v2 stable from v1.29, and that `subPath` Secret mounts do not update.
- Removed the unsupported crash-dump claim about environment-variable secrets and the Kyverno/Gatekeeper feature list. The CIS Benchmark itself was not read (registration-gated); the `kube-bench` verify item is a practice, not a stated control value.

Method: documentation only; no commands were run.
