---
id: computing-software.devops-ci-cd.backstage.catalog-well-known-annotations
name: catalog-well-known-annotations
category: computing-software
field: devops-ci-cd
product: backstage
tags: [annotations, techdocs-ref, project-slug, backstage]
level: practitioner
status: docs-checked
description: "Use the annotations Backstage plugins read, such as techdocs-ref, source-location and github.com/project-slug."
sources:
  - https://backstage.io/docs/features/software-catalog/well-known-annotations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Annotations on `metadata.annotations` carry data that plugins consume. Documented ones include:

- `backstage.io/managed-by-location` and `backstage.io/managed-by-origin-location`: set by the catalog itself, showing where an entity came from.
- `backstage.io/orphan`: marks entities no longer referenced by a location.
- `backstage.io/techdocs-ref`: where TechDocs finds source, for example `dir:.` or `url:https://github.com/example-org/repo/tree/main`.
- `backstage.io/techdocs-entity` and `backstage.io/techdocs-entity-path`: point an entity at another entity's docs.
- `backstage.io/view-url` and `backstage.io/edit-url`: links to the source and edit pages.
- `backstage.io/source-location`: where the code lives.
- `backstage.io/source-template`: the template an entity was created from.
- `github.com/project-slug`, `github.com/team-slug`, `github.com/user-login`, `github.com/user-id`, `gitlab.com/user-id`, `jenkins.io/job-full-name`, `gocd.org/pipelines`: integration keys for plugins.

```yaml
metadata:
  annotations:
    backstage.io/techdocs-ref: dir:.
    github.com/project-slug: example-org/artist-web
```

The `managed-by` annotations are added automatically by the catalog and are not meant to be written by humans, and `backstage.io/orphan` should never be added manually. `github.com/project-slug` has the form `<organization or owner>/<repository>`. Anyone is free to add more annotations, and plugins document their own.

## Checked

2026-11-03. Confirmed on the Well-known annotations page: every annotation key listed in the skill exists there (managed-by-location, managed-by-origin-location, orphan, techdocs-ref with `dir:.` and `url:` forms, techdocs-entity, techdocs-entity-path, view-url, edit-url, source-location, source-template, github.com/project-slug, team-slug, user-login, user-id, gitlab.com/user-id, jenkins.io/job-full-name, gocd.org/pipelines); managed-by and orphan are written by the catalog; the slug format. Removed: advice on committing annotations and waiting for a refresh, which the page does not state.

Method: documentation only; no commands were run.
