---
id: computing-software.cloud-infrastructure-engineering.kubernetes.ephemeral-preview-environments-namespace-as-a-service
name: ephemeral-preview-environments-namespace-as-a-service
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [preview-environment, namespace-as-a-service, ephemeral-environment, pr-environment, ttl-controller, gitops, argocd-applicationset, helm-release-per-pr, cost-control, self-service-infra]
level: advanced
status: docs-checked
description: "Standing up per-PR ephemeral Kubernetes namespaces with automatic TTL cleanup, as a self-service platform capability instead of a one-off CI script."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Pull-Request/", "https://github.com/argoproj/argo-cd/blob/master/docs/operator-manual/applicationset/Application-Deletion.md", "https://github.com/argoproj/argo-cd/blob/master/docs/operator-manual/applicationset/Controlling-Resource-Modification.md", "https://github.com/argoproj/argo-cd/blob/master/docs/user-guide/sync-options.md", "https://codeberg.org/hjacobs/kube-janitor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ephemeral preview environments — namespace-as-a-service

**Goal:** give every open PR (or every developer, on demand) a real,
isolated, short-lived environment in the cluster — not a shared "staging"
everyone steps on — provisioned and torn down automatically, as a platform
capability a team requests rather than a bespoke CI script each repo
reinvents. Often implemented as a thin layer over
`computing-software.cloud-infrastructure-engineering.kubernetes.crossplane-compositions-and-xrds`
or a dedicated operator
(`computing-software.cloud-infrastructure-engineering.kubernetes.kubebuilder-operator-pattern-for-platform-crds`).

## 1. The unit is a namespace, not a cluster
Per-PR *clusters* are almost never worth it (provisioning latency, cost);
per-PR *namespaces* with ResourceQuota, NetworkPolicy default-deny, and a
LimitRange are the standard unit. A `PreviewEnvironment` CRD (or a
Crossplane claim) takes `{repo, prNumber, ref}` and produces: a namespace
named deterministically (`pr-1234-checkout`), a ResourceQuota scoped to
what one PR's worth of testing actually needs (not full prod sizing), a
NetworkPolicy isolating it from other preview namespaces and from prod, and
the actual workload — usually a Helm release or an ArgoCD `Application`
pointed at the PR's branch/image tag.

## 2. GitOps pattern: ApplicationSet per-PR generator
ArgoCD's `ApplicationSet` with a **Pull Request generator** watches a repo's
open PRs (GitHub, GitLab, Gitea, Azure DevOps and others; polling or webhook) and materializes one
`Application` per open PR from a template, each targeting its own namespace
and the PR's branch. This is the lowest-maintenance implementation for teams
already on ArgoCD — no custom controller needed, just the ApplicationSet
manifest and a Helm chart parameterized by PR number. Gotcha: the PR
generator polls every `requeueAfterSeconds`, which defaults to 30 minutes. Lower it, or
configure the ApplicationSet webhook server so Git provider events trigger generation; that
needs the webhook endpoint reachable from the Git provider, a separate networking/secret setup
most teams skip until someone asks why a preview took half an hour to appear.

## 3. TTL and cost control — the part that gets skipped and then hurts
Preview environments that never expire become a second production cluster's
worth of cost silently. Attach a TTL at creation (`PreviewEnvironment.spec.ttl`
or kube-janitor's `janitor/ttl: 4h` / `janitor/expires` annotations) and run a janitor
controller (kube-janitor, or a `CronJob` calling the platform API) that deletes namespaces
past TTL — tie deletion to the actual CR/Claim delete path (so finalizers and
owned-resource GC run), not a raw `kubectl delete namespace` from a cron,
which bypasses any platform bookkeeping (cost attribution records, audit
trail) the CRD's controller maintains. Also auto-delete on PR close/merge via
a CI step or the ApplicationSet PR generator's own cleanup: with the default `sync` policy
(`applicationsSync`; `create-only` and `create-update` block deletion) the controller deletes
the `Application` when the PR closes, and the `resources-finalizer.argocd.argoproj.io`
finalizer then deletes its deployed resources unless `preserveResourcesOnDeletion: true`.
Confirm the namespace itself goes too (a namespace made by `CreateNamespace=true` is not one
of the chart's resources), or the namespace outlives the PR.

## 4. Secrets and data in ephemeral environments
Never seed preview environments with real production data or credentials by
default — generate synthetic fixtures or use masked/sampled data, and make
seeding an explicit opt-in requiring the same approval as any production-
data access elsewhere. Preview namespaces are the most likely place a
short-lived, half-forgotten credential leaks because "it's just a test
environment" lowers everyone's guard — apply the same secret-management
hygiene as production (`computing-software.devops-ci-cd.secrets-management.secrets-and-supply-chain-hygiene`),
not a relaxed version.

## 5. Gotchas
- Node capacity: if the cluster's node pool isn't sized for N concurrent
  preview namespaces during a busy PR day, new previews queue in `Pending`
  with no obvious signal to the developer beyond "my environment never came
  up" — set cluster/node autoscaling limits deliberately for this workload
  class, or cap concurrent previews with a platform-side admission check.
- Shared external dependencies (a shared dev database, a shared message
  broker) that every preview namespace points at defeats the isolation
  purpose and reintroduces the "staging that everyone steps on" problem one
  layer down — give previews either fully isolated or explicitly
  shared-and-documented dependencies, never silently shared ones.

## Verify
- Opening a PR produces a reachable, isolated environment within the
  platform's stated SLA, without manual intervention.
- Closing or merging the PR deletes the namespace and all its resources
  within one cleanup cycle — confirmed by checking the namespace actually
  disappears (`kubectl get ns`), not just that the ArgoCD `Application`
  object is gone.
- An environment left running past its TTL is force-deleted by the janitor,
  and the deletion goes through the same path (finalizers, cost-tracking)
  as a normal teardown.
- A network policy check confirms one PR's preview namespace cannot reach
  another PR's preview namespace or any production namespace.

## Checked
2026-10-27, against Argo CD docs on master (argoproj/argo-cd: Pull Request generator, Application Deletion, Controlling Resource Modification, Sync Options) and the kube-janitor README (codeberg.org/hjacobs/kube-janitor). Confirmed: PR generator providers, `requeueAfterSeconds` default 30 minutes and webhook option, `applicationsSync` policies (`sync` default; `create-only`/`create-update` prevent deletion), the resources finalizer and `preserveResourcesOnDeletion`, `CreateNamespace=true`, and the `janitor/ttl` and `janitor/expires` annotations.
Method: documentation only; no commands were run.
