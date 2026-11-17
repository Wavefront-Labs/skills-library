---
id: computing-software.cloud-infrastructure-engineering.kubernetes.platform-api-design-abstracting-kubernetes-complexity
name: platform-api-design-abstracting-kubernetes-complexity
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [platform-api, internal-developer-platform, idp, abstraction-design, crd-design, intent-vs-implementation, platform-as-a-product, api-versioning, backward-compatibility, cognitive-load, team-topologies]
level: sme
status: docs-checked
description: "Designing a thin platform API that hides Kubernetes YAML/CRD complexity behind intent-level fields, without becoming a leaky or unmaintainable abstraction."
sources: ["https://teamtopologies.com/key-concepts", "https://tag-app-delivery.cncf.io/whitepapers/platforms/", "https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Platform API design — abstracting Kubernetes without leaking it

**Goal:** design the API surface an app team actually interacts with (a CRD,
a Backstage template form, a CLI) so it hides Deployment/Service/Ingress/
NetworkPolicy/ResourceQuota wiring behind a handful of intent fields, while
staying honest about what it can't abstract away. This is the design
discipline underneath both Crossplane XRDs
(`computing-software.cloud-infrastructure-engineering.kubernetes.crossplane-compositions-and-xrds`)
and Backstage templates
(`computing-software.cloud-infrastructure-engineering.kubernetes.backstage-scaffolder-golden-path-templates`)
— those are two possible *implementations* of a platform API; this skill is
how to decide what the API says before picking either.

## 1. Start from the job, not the resource
The anti-pattern is a "platform API" that's really just a thin YAML template
exposing every Kubernetes field as a parameter — that's not abstraction, it's
indirection, and it inherits every Kubernetes footgun (wrong `resources.limits`
units, missing `readinessProbe`, no `PodDisruptionBudget`) while adding a UI
on top. Start instead from the job the app team is doing: "run a stateless
HTTP service," "run a worker that drains a queue," "get a Postgres database."
Each job becomes one API (`AppService`, `Worker`, `PostgresInstance`) with
fields that are *decisions a developer should actually have an opinion about*
(CPU/memory tier, scaling range, public vs. internal) and nothing else.
Fields they shouldn't have an opinion about (which CNI, which storage class,
how probes are wired) are the platform's problem, encoded once in the
implementation.

## 2. The intent/implementation split is the whole skill
For every field you're tempted to expose, ask: if the platform team changed
the underlying mechanism tomorrow (switched ingress controllers, changed
autoscaler, moved to a new node pool class), would this field still make
sense? `replicas: 3` fails that test (survives a migration badly — should be
`minScale`/`maxScale` or just `tier: small|medium|large` with the platform
picking real numbers). `cpuRequest: 500m` mostly fails it too — expose
`tier` and translate internally so the platform can retune the mapping (e.g.
after a benchmarking pass) without 200 teams editing YAML. Fields that pass
the test — `public: true`, `minReplicas: 2` as a *floor* for availability
intent, `region` — are the right things to expose.

## 3. Versioning and the compatibility promise
Once an API ships, every consumer manifest is a contract. Favor additive
changes (new optional field, sane default) over anything that changes
behavior for existing resources without a version bump. If you must break a
field's meaning, ship it as a new API version with a conversion path (a
conversion webhook for CRDs, or a migration script + deprecation window for a
Backstage template), and give a real deprecation timeline — "this field is
removed in 90 days, here's the replacement" — rather than silent drift.
Treat `v1alpha1` as genuinely unstable (fine to break) but don't let
`v1alpha1` live in production for two years; that's a broken promise to
anyone who built on it believing the label.

## 4. The abstraction leaks when you don't expect it
No matter how clean the API, app teams eventually need an escape hatch —
custom sidecar, non-standard port, an annotation your controller doesn't
know about. Decide deliberately whether to support that via an `overrides:`
or `raw:` field that merges into the generated manifests (flexible, but every
override is now outside the platform's guarantees — document that it voids
the "we manage this for you" promise) or to refuse and make the team file a
platform feature request. Silently *not* deciding this means teams fork your
templates locally the first time they hit the wall, and now you have
shadow infrastructure.

## Verify
- A new consumer can accomplish a standard job (ship a stateless HTTP
  service) using only intent-level fields, with zero knowledge of what
  Kubernetes resources get created underneath.
- Changing an implementation detail (swap the underlying autoscaler, change
  the default resource-tier mapping) requires zero changes to any existing
  consumer manifest.
- A field audit of the API surface — for each field, can you name a reason a
  developer, not the platform, should own this decision? Any field that
  fails gets removed or defaulted away.
- The API has a stated deprecation policy for breaking a field, and at least
  one real deprecation has followed it (or, if none yet, the policy is
  written down before it's needed — note this is unverified until exercised
  once in practice).

## Checked
2026-10-27, against Team Topologies key concepts (teamtopologies.com), the CNCF TAG App Delivery Platforms white paper and the Kubernetes CRD versioning task (kubernetes/website main, v1.38 dev tree). Confirmed: CRDs serve multiple versions with conversion between them by a conversion webhook configured in `spec.conversion`. The rest of the skill is design guidance, not checkable fact.
Method: documentation only; no commands were run.
