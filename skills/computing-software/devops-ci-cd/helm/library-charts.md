---
id: computing-software.devops-ci-cd.helm.library-charts
name: library-charts
category: computing-software
field: devops-ci-cd
product: helm
tags: [library-charts, chart-type, type-library, reusable-templates, named-templates, helpers]
level: advanced
status: docs-checked
description: "Library charts (type: library) share named templates and cannot be installed; how they differ from application charts."
sources:
  - "https://helm.sh/docs/topics/library_charts/"
  - "https://helm.sh/docs/topics/charts/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`type` in `Chart.yaml` is `application` (default) or `library`.

A library chart provides utilities or functions for other charts. It is not installable and has no renderable resources: Helm refuses to install a library chart. Its templates are meant to be defined with `define` and reused by charts that depend on it. Any manifest-producing templates inside a library chart are not rendered; only named templates are usable.

Library files whose names begin with `_` are the intended contents; `helm create` is used then the unneeded template files removed.

Using one:

```yaml
dependencies:
  - name: mylib
    version: 1.0.0
    repository: https://example.com/charts
```

Then `helm dependency update`, and call `{{ include "mylib.labels" . }}` in your templates.

Rules and tips:

- Because named templates are global, prefix with the library name.
- The `type` field is a `v2` feature, so a library chart needs `apiVersion: v2`.
- An application chart can be used as a library chart by setting its type to `library`; its resource objects are then not rendered.
- Library charts exist to share snippets across charts (the guide's example is a common ConfigMap definition merged with the caller's overrides).
- Because a library chart cannot be installed on its own, `.Files` refers to file paths in the parent chart and `.Values` is the same as the parent's, unlike application subcharts which get only the section under their own key.
- The older Common Helm Helper Chart (helm/charts incubator) is no longer maintained, archived and deprecated.

Application charts are installable and the default.

## Checked

2026-11-08. Read the Library Charts page in full and the Charts topic page. Removed an unsupported claim that a library can be used by another library; added the .Files/.Values behaviour, type switching and the deprecated Common Helm Helper Chart note.

Method: documentation only; no commands were run.
