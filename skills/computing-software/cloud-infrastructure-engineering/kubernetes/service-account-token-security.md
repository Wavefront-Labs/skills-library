---
id: computing-software.cloud-infrastructure-engineering.kubernetes.service-account-token-security
name: service-account-token-security
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, serviceaccount, bound-service-account-token, tokenrequest, projected-volume, automountserviceaccounttoken, audience, oidc, legacy-token, csrf, workload-identity, pod-identity, sidecar-token-theft, kubectl-create-token, per-workload-serviceaccount]
level: advanced
status: docs-checked
description: "Bound (projected) ServiceAccount tokens vs. legacy long-lived Secret tokens, the TokenRequest API, audience/expiration scoping, and why auto-mounted tokens are a lateral-movement path."
sources: ["https://kubernetes.io/docs/concepts/security/service-accounts/", "https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ServiceAccount token security — the credential every pod has by default

**Goal:** stop treating the mounted ServiceAccount token as a harmless default —
it's an API credential, and the single most common lateral-movement path after
initial container compromise is reading `/var/run/secrets/kubernetes.io/
serviceaccount/token` and calling the API as whatever that pod's ServiceAccount
can do. RBAC scoping of what a ServiceAccount is *allowed* to do is in
`computing-software.cloud-infrastructure-engineering.kubernetes.k8s-rbac-and-security`;
this skill is about the token's own lifecycle and exposure.

## 1. Bound (projected) tokens vs. legacy Secret tokens
- **Legacy** (Secret tokens; before 1.24 one was created automatically for every
  ServiceAccount, and the `LegacyServiceAccountTokenNoAutoGeneration` gate stopped that
  from 1.24, GA in 1.27): a long-lived, non-expiring token in a Secret — anyone who could
  `get` that Secret had a permanent credential. Docs mark Secret-based tokens as not recommended.
- **Bound tokens** (mounted into pods via a projected volume since 1.22): projected into the pod
  via a `serviceAccountToken` volume, JWT-signed, with a **default 1-hour expiry** (the default
  mounted token may be extended up to a year for old clients, see the projected-token skill),
  refreshed by the kubelet, and **bound to the specific pod**. For TokenRequest tokens the API
  server checks that the bound object still exists, matching by UID, so a token from a pod that
  has since been deleted stops working immediately even though the JWT's stated expiry hasn't
  passed. Validators that only check the JWT via OIDC keep accepting it until it expires, so
  prefer the TokenReview API for your own services.
- Check which you're on: `kubectl get sa <name> -o yaml` — legacy accounts carry
  a `secrets:` list pointing at a token Secret; pure bound-token accounts don't.
  Clusters upgraded from very old versions can still have legacy Secret tokens
  lingering — audit and delete them (`kubectl delete secret` does **not** delete
  the ServiceAccount, just the stale credential).

## 2. The TokenRequest API — minting scoped tokens on demand
```yaml
spec:
  containers:
  - volumeMounts: [{name: vault-token, mountPath: /var/run/secrets/tokens}]
  volumes:
  - name: vault-token
    projected:
      sources:
      - serviceAccountToken: {path: vault-token, expirationSeconds: 600, audience: vault}
```
`audience` scopes the token to a specific consumer (e.g. `vault`, `sts.amazonaws.
com` for IRSA) — a token minted for audience `vault` is **rejected** by the
Kubernetes API server itself (and by any other properly-configured audience
check) if presented somewhere else, limiting blast radius if it leaks. This is
the pattern external integrations use: they accept such audience-scoped tokens in exchange for
their own credentials, so the pod holds a short-lived token rather than a static key; check each
integration's documentation for the audience and issuer it expects. A service that validates
tokens should always define the audience it accepts.
`expirationSeconds` as low as operationally tolerable (minutes, not the 1hr
default) further shrinks the usable window of a stolen token.

## 3. `automountServiceAccountToken: false` — the default you should flip
Every pod gets a token mounted **unless told not to**, even pods that never call
the Kubernetes API (most application containers: web servers, batch workers that
only talk to a database). That mounted token is a standing credential a container
compromise hands the attacker for free.
```yaml
apiVersion: v1
kind: ServiceAccount
metadata: {name: web}
automountServiceAccountToken: false   # set at SA level...
---
spec:
  serviceAccountName: web
  automountServiceAccountToken: false  # ...or per-pod (pod setting wins if both set)
```
Set it at the ServiceAccount level as the default for everything using that SA,
and only re-enable per-pod (`automountServiceAccountToken: true` on the pod spec)
for the specific workloads that genuinely call the API.

## 4. Audit what auto-mounted tokens can actually do
```bash
kubectl auth can-i --list --as=system:serviceaccount:<ns>:<sa>
```
Run this for every ServiceAccount with a mounted token, not just the ones you
remember configuring — `default` ServiceAccounts in namespaces nobody locked down
often carry no explicit RoleBinding but can still enumerate with whatever
cluster-wide `view`-ish aggregated ClusterRole accidentally applies (see the
aggregated-ClusterRole gotcha in `k8s-rbac-and-security`). A token that can do
nothing is a much smaller incident than one that can list Secrets.

## 5. Sidecar/ambient token theft
Any container in the pod can read the same projected volume — a compromised
sidecar (a logging agent, a service-mesh proxy with an unrelated RCE) reads the
main app's mounted token just as easily as the app itself. Per-container
isolation of the token volume mount (only mount it into the container that
actually needs it, via selective `volumeMounts`, not a blanket pod-level mount
every container inherits) reduces this; it does not eliminate it if containers
share a network namespace and one can reach the other's filesystem through
`/proc/<pid>/root` with sufficient privilege.

## Gotchas
- The "bound to pod" check is by the pod's UID, so a token copied out of a pod cannot be reused
  for a different pod, but replaying a stolen token from outside the cluster still works until
  the pod is deleted or the token expires, whichever comes first. Short
  `expirationSeconds` shortens that window; the binding alone does not stop replay.
- `kubectl create token <sa> --duration=1h` mints an ad hoc bound token for
  testing/debugging — treat it with the same care as any credential; it's easy to
  forget it's sitting in shell history or a CI log.
- Disabling automount on a ServiceAccount used by an operator/controller that
  *does* need API access breaks it (its API calls are unauthenticated) — test automount
  changes against every workload using that
  SA, not just the ones you intended to restrict.

## Verify
- [ ] `kubectl get sa -A -o yaml` shows no lingering legacy long-lived Secret
      tokens on clusters that have ever been upgraded from pre-1.24.
- [ ] `automountServiceAccountToken: false` is the default on ServiceAccounts for
      workloads that don't call the Kubernetes API; API-calling workloads are the
      explicit exception, not the rule.
- [ ] `kubectl auth can-i --list` reviewed for every ServiceAccount with a
      mounted token, including `default` in every namespace.
- [ ] Cloud credential access uses audience-scoped TokenRequest tokens
      (workload identity) instead of static keys in Secrets.
- [ ] `expirationSeconds` on projected tokens is set to the shortest value the
      consuming integration tolerates, not left at the 1-hour default by habit.

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37) and kubectl reference.
Confirmed: projected tokens in pods since 1.22; automatic legacy Secret tokens before 1.24 and the NoAutoGeneration gate (enabled 1.24,
GA and removed 1.27); bound-object UID check for TokenRequest tokens and OIDC-only validators accepting until expiry; default 1-hour
projected expiry (3607 s default token); `automountServiceAccountToken` at ServiceAccount and pod level with the pod taking precedence;
`kubectl create token <sa> --duration`. Wrong in the original: "bound tokens default since 1.24" (1.22), "deleting the ServiceAccount
didn't revoke the legacy Secret token" (removed, unconfirmed), "same name" binding (the binding is by UID), and the workload-identity
"under the hood" list (removed, unconfirmed). The prose `sources` entries are replaced with URLs.
Method: documentation only; no commands were run.
