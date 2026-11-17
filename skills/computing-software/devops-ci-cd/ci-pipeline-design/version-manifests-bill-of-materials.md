---
id: computing-software.devops-ci-cd.ci-pipeline-design.version-manifests-bill-of-materials
name: version-manifests-bill-of-materials
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, version-manifest, component-pipelines, artifact-promotion]
level: practitioner
status: docs-checked
description: "Describe a releasable system as a version manifest (bill of materials) of component digests: formats (umbrella chart, BOM, lock file), generation, and promotion."
sources: ["https://helm.sh/docs/helm/helm_dependency/", "https://docs.gradle.org/current/userguide/platforms.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Version manifests (bill of materials)

A manifest pins every component of a release to an immutable version so "release 2026.10" means
exactly one set of artifacts.

## Formats by ecosystem
| Context | Manifest |
|---|---|
| Kubernetes apps | umbrella Helm chart `Chart.yaml` dependencies with exact versions, or a GitOps env file listing image digests |
| JVM libraries | Maven BOM / Gradle platform (`java-platform`) |
| Mixed services | custom `release.yaml` with digests |

```yaml
# release.yaml
release: 2026.10.18-1
components:
  api:      { image: registry.example.com/api@sha256:4f1c..., git: 9a1b2c3 }
  worker:   { image: registry.example.com/worker@sha256:77de..., git: 1d2e3f4 }
  web:      { image: registry.example.com/web@sha256:a0b1..., git: 5c6d7e8 }
schema: 20261015_add_orders
```

## Practices
- Generate, do not hand-edit: the integration/release pipeline writes it from built artifacts
  (`crane digest registry.example.com/api:1.4.2`).
- Use digests, not tags; tags can move.
- Promotion = copying the same manifest to the next environment (GitOps PR).
- Sign or attest the manifest and keep it in the release.
- Diff manifests between releases to produce release notes of what changed.

## Verify
- [ ] Deploying the manifest twice yields identical running digests; `diff` of two manifests lists exactly the changed components.

## Checked

2026-10-28. Confirmed: Helm dependency docs (dependencies declared in Chart.yaml), Gradle platforms docs (`java-platform` plugin, publishable as a Maven BOM), and `crane digest` in the crane reference. Removed: the JS monorepo changesets row and the cosign sign-blob command.

Method: documentation only; no commands were run.
