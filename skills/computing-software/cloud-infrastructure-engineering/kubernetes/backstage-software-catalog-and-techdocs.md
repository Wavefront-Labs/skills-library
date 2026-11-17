---
id: computing-software.cloud-infrastructure-engineering.kubernetes.backstage-software-catalog-and-techdocs
name: backstage-software-catalog-and-techdocs
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [backstage, software-catalog, catalog-info-yaml, techdocs, idp, internal-developer-portal, entity-provider, kubernetes-plugin, service-ownership, mkdocs, backstage-app, spotify-backstage, cncf]
level: advanced
status: docs-checked
description: "Modeling services, APIs and ownership in Backstage's catalog-info.yaml and keeping TechDocs from rotting, as the entry point to an internal developer portal."
sources: ["https://backstage.io/docs/features/software-catalog/descriptor-format", "https://backstage.io/docs/features/software-catalog/configuration", "https://backstage.io/docs/features/software-catalog/life-of-an-entity", "https://backstage.io/docs/integrations/github/discovery", "https://backstage.io/docs/features/techdocs/getting-started", "https://backstage.io/docs/features/techdocs/configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backstage software catalog and TechDocs

**Goal:** stand up the catalog as the single source of truth for "what exists and
who owns it," with the Kubernetes plugin wired to show live pod/deployment state
per entity, without the catalog decaying into stale YAML nobody trusts.

## 1. catalog-info.yaml is the unit of truth
Every repo gets one `catalog-info.yaml` at root defining at minimum a `Component`
kind, with `spec.type` (`service`, `website`, `library`), `spec.lifecycle`
(`experimental`, `production`, `deprecated`), `spec.owner` (best practice: a `Group` entity ref
rather than a person), and `spec.system` (groups related
components). Model `API` entities separately with an OpenAPI/AsyncAPI/gRPC spec in
`spec.definition`, and link via `providesApis`/`consumesApis` so the catalog graph
shows real dependencies, not just an org chart.

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: checkout-service
  annotations:
    backstage.io/techdocs-ref: dir:.
    backstage.io/kubernetes-id: checkout-service
    github.com/project-slug: org/checkout-service
spec:
  type: service
  lifecycle: production
  owner: group:platform-team
  system: payments
  providesApis: [checkout-api]
```

## 2. Entity ingestion — don't hand-register everything
Hand-adding `catalog-info.yaml` per repo in the UI does not scale. Use a catalog
**provider**: the GitHub discovery provider (module `@backstage/plugin-catalog-backend-module-github`,
added with `backend.add(import(...))`) crawls an org for files at a configured `catalogPath` (for example
`/catalog-info.yaml`, wildcards allowed), configured under `catalog.providers.github.<providerId>` with a
`schedule` (the documented example uses `frequency: { minutes: 30 }` and `timeout: { minutes: 3 }`).
Orphaned entities (for example a catalog-info file moved without updating the registration) get a
`backstage.io/orphan: 'true'` annotation, and with the default `catalog.orphanStrategy: delete` they are
removed automatically; set `orphanStrategy: keep` to keep them.

## 3. Kubernetes plugin — live state per entity
The `@backstage/plugin-kubernetes` + backend plugin reads
`backstage.io/kubernetes-id` (or `-label-selector`) on the entity, matches it
against configured clusters (via `clusterLocatorMethods`: `config`, `catalog`, `gke`,
`localKubectlProxy`), and renders the entity's Kubernetes objects on the entity page. With the
`serviceAccount` auth provider it needs a service account token with the documented read-only ClusterRole
(pods, pods/log, deployments, replicasets and so on, and no Secrets), not cluster-admin. Use
`serviceLocatorMethod: singleTenant` with the cluster selection annotation to restrict an entity to one cluster.

## 4. TechDocs — docs-as-code, not a wiki
TechDocs builds MkDocs sites from `docs/` + `mkdocs.yml` next to the code,
versioned with it. Two build modes: `techdocs.builder: 'local'` (the backend generates docs when a page is opened, the "Basic"
setup, with `generator.runIn` `docker` or `local`) vs. `builder: 'external'` (the "Recommended" setup): CI
runs `techdocs-cli generate` and `publish` to cloud storage and the backend only serves what is stored.
The docs recommend generating docs in CI/CD. The annotation
`backstage.io/techdocs-ref: dir:.` points at the doc source relative to the entity's location.

## 5. The actual failure mode: catalog rot
The catalog's value is trust. Entities with dead `owner` groups, `production` lifecycle on decommissioned
services, or stale TechDocs erode it. Mitigate with a CI validation of `catalog-info.yaml`, a periodic
ownership review and keeping the catalog the canonical source of ownership.

## Verify
- `catalog-info.yaml` entities appear in the Backstage catalog UI within one
  ingestion cycle, correctly grouped by `system` and owned by a `Group`, not a
  `User`.
- The Kubernetes tab on a service entity lists the same pods as `kubectl get pods -l backstage.io/kubernetes-id=<id>` in the target cluster.
- TechDocs page renders and a change to `docs/` lands on the published site
  within one CI run, not a manual rebuild.
- An intentionally malformed `catalog-info.yaml` produces an ingestion error you can see in the Backstage logs.

Related: golden-path self-service templates live in
`computing-software.cloud-infrastructure-engineering.kubernetes.backstage-scaffolder-golden-path-templates`.

## Checked

Checked against `backstage/backstage` master docs (last commit 2026-10-25): `features/software-catalog/descriptor-format.md`, `configuration.md`, `life-of-an-entity.md`, `well-known-annotations.md`, `integrations/github/discovery.md`, `features/techdocs/getting-started.md`, `configuration.md`, `features/kubernetes/configuration.md`.
Confirmed: lifecycle values `experimental`, `production`, `deprecated`; `backstage.io/orphan` annotation; `techdocs.builder` `local`/`external`; `techdocs-ref` annotation; GitHub provider config keys and the 30 minute example frequency; Kubernetes locator list.
Wrong in the draft: orphaned entities are deleted by default (`orphanStrategy: delete`); the locators `aws` and `serviceAccount` do not exist; `GithubEntityProvider` class names are not in the current docs.
Removed as unconfirmed: the sequential multi-cluster slowdown claim, the ~50 services threshold, the silent-ingestion-failure claim.

Method: documentation only; no commands were run.
