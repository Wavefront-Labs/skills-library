---
id: computing-software.devops-ci-cd.backstage.catalog-descriptor-format
name: catalog-descriptor-format
category: computing-software
field: devops-ci-cd
product: backstage
tags: [descriptor-format, catalog-info-yaml, entity-envelope, backstage]
level: intro
status: docs-checked
description: "Write a catalog-info.yaml entity with apiVersion, kind, metadata and spec, and know the common metadata fields."
sources:
  - https://backstage.io/docs/features/software-catalog/descriptor-format
  - https://backstage.io/docs/features/software-catalog/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Catalog entities are YAML documents, usually named `catalog-info.yaml` and stored beside the code they describe. Every entity has the same envelope: `apiVersion`, `kind`, `metadata` and a kind-specific `spec`.

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: artist-web
  description: The place to be, for great artists
  labels:
    system: public-websites
  annotations:
    github.com/project-slug: example-org/artist-web
  tags:
    - java
  links:
    - url: https://admin.example-org.com
      title: Admin Dashboard
      icon: dashboard
      type: admin-dashboard
spec:
  type: website
  lifecycle: production
  owner: artist-relations-team
  system: public-websites
```

Metadata fields:

- `name` is required and, with `kind` and `namespace`, identifies the entity.
- `namespace` is optional.
- `uid` is generated output, never written by hand.
- `title`, `description`, `labels`, `annotations`, `tags` and `links` are optional.

When several `catalog-info.yaml` files with the same `metadata.name` are discovered, one is processed and the others are skipped and logged. Labels are key/value pairs for classification and references, while annotations are non-identifying metadata that mainly reference external systems such as `github.com/project-slug`; both use optional domain-prefixed keys, and the `backstage.io/` prefix is reserved.

## Checked

2026-11-03. Confirmed on the descriptor format page: the file naming recommendation, the envelope fields, `name` required, `namespace` optional, `uid` generated output, optional `title`, `description`, `labels`, `annotations`, `tags` and `links` (url required, title, icon, type optional), key prefix rules and the reserved `backstage.io/` prefix. On the catalog configuration page: duplicate `metadata.name` files, one processed and the rest skipped with a log entry. Removed: the claim that one file can hold several entities separated by `---`, which neither page states.

Method: documentation only; no commands were run.
