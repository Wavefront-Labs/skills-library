---
id: computing-software.cloud-infrastructure-engineering.harbor.user-defined-oci-artifacts
name: user-defined-oci-artifacts
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [oci-artifact, skip-list, artifact-icon, annotations, harbor]
level: advanced
status: docs-checked
description: "Make custom OCI artifacts such as ML models display rich metadata and icons in Harbor with the skip-list and icon annotations."
sources:
  - https://goharbor.io/docs/main/administration/user-defined-OCI-artifact/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Harbor can show rich metadata and icons for custom OCI artifacts, such as Kubeflow or other machine learning data models, when they carry Harbor-specific annotations in the manifest.

Two annotation keys:
- `io.goharbor.artifact.v1alpha1.skip-list` goes in `manifest.config.annotations`. Optional. A comma-separated string of keys that Harbor ignores in the configuration JSON layer, for example `"metrics,git"`.
- `io.goharbor.artifact.v1alpha1.icon` goes in `manifest.layers[].annotations`. Only the key matters; the value must be an empty string. The icon must itself be a layer of the artifact when you build it, and its `mediaType` must be `image/gif`, `image/png` or `image/jpeg`.

Example manifest shape:
```json
{
  "schemaVersion": 2,
  "config": {
    "mediaType": "application/vnd.caicloud.model.config.v1alpha1+json",
    "annotations": { "io.goharbor.artifact.v1alpha1.skip-list": "metrics,git" }
  },
  "layers": [
    { "mediaType": "image/png",
      "annotations": { "io.goharbor.artifact.v1alpha1.icon": "" } },
    { "mediaType": "application/tar+gzip" }
  ]
}
```
(digest and size fields omitted here; a real manifest needs them on every descriptor.)

The page names ORMB as a worked example of a tool that builds such artifacts.

## Checked

2026-11-03. Both annotation keys and their locations, the empty-string icon value, the icon media types and the example manifest shape were read against the Harbor docs page User-defined OCI artifact. Removed: the closing claim about artifacts without annotations (not on the page).

Method: documentation only; no commands were run.
