---
id: computing-software.devops-ci-cd.backstage.techdocs-annotation-and-mkdocs
name: techdocs-annotation-and-mkdocs
category: computing-software
field: devops-ci-cd
product: backstage
tags: [techdocs-ref, mkdocs-yml, docs-as-code, backstage]
level: intro
status: docs-checked
description: "Enable docs-as-code for an entity with the backstage.io/techdocs-ref annotation, mkdocs.yml and a docs folder."
sources:
  - https://backstage.io/docs/features/techdocs/creating-and-publishing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

TechDocs renders Markdown stored beside code as a docs site inside Backstage. Add an annotation to the entity and an `mkdocs.yml` plus a `docs/` directory to the repository.

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: artist-web
  annotations:
    backstage.io/techdocs-ref: dir:.
spec:
  type: website
  lifecycle: production
  owner: artist-relations-team
```

```yaml
site_name: 'artist-web'
nav:
  - Home: index.md
plugins:
  - techdocs-core
```

- `dir:.` means the docs source is relative to the `catalog-info.yaml` location. A URL form such as `url:https://github.com/example-org/repo/tree/main` points elsewhere.
- Backstage automatically adds the `techdocs-core` plugin to the MkDocs config if it is missing (this can be turned off in configuration), and extra plugins must be installed locally or in the Docker image.
- The `mkdocs.yml` file should be a sibling of `catalog-info.yaml` unless the annotation points elsewhere.

Use `backstage.io/techdocs-entity` to show another entity's docs, for example for subcomponents.

## Checked

2026-11-03. Confirmed on the Creating and Publishing page: the `backstage.io/techdocs-ref` annotation is used to download the documentation source, `dir:.` is relative to `catalog-info.yaml`, the `mkdocs.yml` and `docs/` layout, and that `techdocs-core` is added automatically if missing. On the How-to guides and Well-known annotations pages: `url:` form of the annotation and `mkdocs.yml` as a sibling of `catalog-info.yaml`. On the configuration page: extra plugins must be installed locally or in the image. Removed: the URL reader versus `git clone` claim and the FAQ remark, not stated on these pages.

Method: documentation only; no commands were run.
