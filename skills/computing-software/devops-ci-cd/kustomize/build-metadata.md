---
id: computing-software.devops-ci-cd.kustomize.build-metadata
name: build-metadata
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [buildmetadata, managedbylabel, originannotations, transformerannotations]
level: advanced
status: docs-checked
description: "Add build provenance with buildMetadata options managedByLabel, originAnnotations and transformerAnnotations."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/buildmetadata/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`buildMetadata` is a list of strings choosing metadata that kustomize adds to each resource about how it was built:

```yaml
buildMetadata: [managedByLabel, originAnnotations, transformerAnnotations]
```

- `managedByLabel` adds the label `app.kubernetes.io/managed-by` with the version of kustomize that built it, for example `kustomize-v4.4.1`.
- `originAnnotations` adds the annotation `config.kubernetes.io/origin`. Generated resources get data about the generator that produced them; a resource from `resources` gets data about its file. Possible fields: `path`, `ref` and `repo` (for remote files or generators), `configuredIn` (path to the generator config; the kustomization file itself if the generator is invoked via a kustomization field) and `configuredBy` (ObjectReference of the generator config).
- `transformerAnnotations` is marked Alpha. It adds annotation `config.kubernetes.io/transformations`, a list of data about the transformers that acted on each resource; fields are the same as for origin except there is no `path`. While alpha, the key is shown with an alpha prefix (`alpha.config.kubernetes.io/transformations`), and content stability is not guaranteed.

Local file paths are relative to the top-level kustomization, that is the directory passed to `kustomize build`. Remote paths are relative to the root of the remote repository. Fields that do not apply are omitted.

Example: `resources: [deployment.yaml]` with `originAnnotations` gives `config.kubernetes.io/origin` with `path: deployment.yaml`.

## Checked

2026-11-08: read the buildMetadata reference page in full; confirmed the three options, label and annotation keys, field lists, path rules, the example and the Alpha status of transformerAnnotations. Removed the debugging advice and the note about stripping annotations before production, which the page does not state.

Method: documentation only; no commands were run.
