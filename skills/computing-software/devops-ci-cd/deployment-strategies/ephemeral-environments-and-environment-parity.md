---
id: computing-software.devops-ci-cd.deployment-strategies.ephemeral-environments-and-environment-parity
name: ephemeral-environments-and-environment-parity
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, ephemeral-environments, preview-environments, environment-provisioning, environment-parity, environment-management, dev-staging-prod, namespace-per-pr, vcluster, review-apps, ttl-controller, environment-cleanup, cost-control, shared-staging-problem, data-for-ephemeral-envs, dns-wildcard, ingress-per-env, service-mesh-routing, signadot, dynamic-environments, environment-registry, infrastructure-as-code, terraform-workspaces, kubernetes]
level: advanced
status: draft
description: "Manage environments as disposable, consistent things: dev/staging/prod parity rules, ephemeral preview environments per PR (namespaces, vclusters, wildcard DNS, TTL cleanup), data, cost, a registry."
sources: ["Humble & Farley, Continuous Delivery (2010), ch. 11 Managing Infrastructure and Environments", "https://12factor.net/dev-prod-parity", "https://www.vcluster.com/docs", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Pull-Request/", "https://docs.gitlab.com/ee/ci/review_apps/", "https://ephemeralenvironments.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ephemeral environments and environment parity

**Goal:** every environment is created from code, looks like production in the ways that
matter, exists only while needed, and nobody waits for "the staging slot".

## 1. Parity: what must match, what may differ
Match production in: OS/base image, runtime versions, service topology (same services,
same ingress/mesh, same auth path), config *mechanism*, migrations path, observability
stack, deploy mechanism. May differ: scale (replicas, instance size), data volume,
external integrations (sandbox/stubs), cost-driven managed-service tiers. Write the parity
table down; every "differs" entry is a known blind spot (e.g. single-replica staging never
catches rolling-update bugs → run at least 2 replicas for the services that matter).
Dev/prod parity failures come from *drift*: manual tweaks to staging, pinned old versions,
different feature-flag defaults. Rebuild staging from code regularly (weekly or on every
infra change) so drift cannot accumulate.

## 2. The environment ladder
| env | purpose | lifetime | data |
|---|---|---|---|
| local/dev | inner loop | minutes–days | synthetic |
| **preview/ephemeral** | one per PR/feature; review, e2e, demos | PR lifetime (+TTL) | seeded synthetic or anonymised subset |
| integration/acceptance | pipeline stage; latest green of everything | per pipeline run or persistent-but-rebuilt | seeded |
| staging/pre-prod | prod-like rehearsal, capacity tests, UAT | persistent, rebuilt from code | anonymised prod subset |
| production | — | — | real |
Ephemeral previews remove most of the contention on staging; staging then stays prod-like
instead of being a shared dev playground.

## 3. Building preview environments
**Kubernetes namespace per PR** (most common):
- Name `pr-<n>-<repo>`; labels `env=preview, pr=<n>, ttl=72h, owner=<team>`.
- Wildcard DNS `*.preview.example.com` → ingress; host `pr-123-web.preview.example.com`;
  wildcard TLS cert via cert-manager (DNS-01).
- Deploy the PR's image with the production Helm chart + a `values-preview.yaml`
  (1 replica, small limits, stubs for third parties, feature flags on).
- Dependencies: own Postgres/Redis in the namespace (bitnami charts or operators) seeded
  by a Job, *or* shared "preview" instances with a schema/db per PR for speed.
- Trigger: Argo CD `pullRequest` generator (app per open PR with label `preview`), GitLab
  review apps (`environment: review/$CI_COMMIT_REF_SLUG` + `on_stop`), GitHub Actions
  job on `pull_request` + `environment: preview-${{ github.event.number }}` writing the
  URL to a PR comment.
- Teardown: PR close/merge event → delete namespace; plus a **TTL controller**
  (`kube-janitor`, `k8s-ttl-controller`, or a CronJob checking the `ttl` label against
  creation time) for the ones events missed.
**vcluster per PR** when teams need cluster-scoped things (CRDs, operators, different
Kubernetes versions): virtual control plane in a namespace; `vcluster create pr-123 --upgrade`,
`vcluster connect`; slower (30–60 s) but isolates everything.
**Request-level routing** (Signadot, mesh header-based routing, Uber's "slate"): deploy
only the changed service into a shared baseline and route requests with a header to it
— cheapest at scale for microservice fleets; needs context propagation.
**Non-Kubernetes**: Terraform workspace per PR (`terraform workspace new pr-123`) for
cloud resources with tags `ttl`; app platforms (Vercel/Netlify/Render/Heroku review apps)
give it for free for web tiers.

## 4. Data in ephemeral environments
Seeded synthetic data (factories/golden dataset — see test-data skill) by default; an
anonymised subset snapshot restored from a template (`CREATE DATABASE … TEMPLATE`, or
RDS snapshot restore for staging-sized) when realism matters. Never point previews at
shared mutable data. Migrations run on creation — a free migration test per PR.

## 5. Cost and limits
- `ResourceQuota` + `LimitRange` per preview namespace; cluster autoscaler with a
  preview node pool (spot/preemptible) and a hard cap.
- TTL 24–72 h, extendable by label; auto-sleep (scale to zero) after N hours idle
  (`keda` HTTP add-on or a nightly scale-down CronJob) with wake on first request.
- Dashboard: namespaces by age/owner/cost (Kubecost/OpenCost labels `env=preview`).
- Shared stubs for expensive third parties (payment, email) via WireMock/Prism in a
  `preview-shared` namespace.
- Build once: previews use the PR's CI image; never rebuild inside the environment.

## 6. Environment registry
A small table/CRD/`environments.yaml`: name, type, owner, created, ttl, URL, versions
deployed (service → digest), data source, status. Fed by the provisioning pipeline;
read by the PR bot, the TTL janitor, the cost dashboard and humans asking "what's on
staging?". Argo CD/GitLab environments pages approximate this; for mixed infra, maintain
it explicitly.

## 7. Access and security
Previews are internet-reachable only behind SSO/IP allowlist (oauth2-proxy at the
ingress, or private DNS + VPN); no production secrets; sandbox credentials only; images
scanned like any other; namespaces isolated by NetworkPolicy (default deny egress to
other namespaces except shared stubs and DNS). Treat preview URLs as untrusted
surfaces — they run unreviewed PR code.

## Verify
- [ ] Opening a PR yields a working URL in a comment within ~5 min; closing it removes the namespace within 10 min.
- [ ] Orphan check: no `env=preview` namespace older than its TTL (janitor report).
- [ ] Staging is rebuilt from code on a schedule; `diff` of staging vs prod config is explainable.
- [ ] Preview cost per week is on a dashboard and under the agreed cap.
