---
id: computing-software.devops-ci-cd.kustomize.configmap-generator-sources
name: configmap-generator-sources
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [configmapgenerator, files, literals, envs, configmap]
level: practitioner
status: docs-checked
description: "Generate ConfigMaps from files, literals or env files, rename file keys, and set per-ConfigMap labels and annotations."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/configmapgenerator/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Each `configMapGenerator` entry produces one ConfigMap.

```yaml
configMapGenerator:
- name: my-application-properties
  files:
  - application.properties          # key = file name
- name: app-whatever
  files:
  - myFileName.ini=whatever.ini     # key=file
- name: my-java-server-env-vars
  literals:
  - JAVA_HOME=/opt/java/jdk
  - JAVA_TOOL_OPTIONS=-agentlib:hprof
- name: tracing-options
  envs:
  - tracing.env
- name: dashboards
  files:
  - mydashboard.json
  options:
    annotations:
      dashboard: "1"
    labels:
      app.kubernetes.io/name: "app1"
```

Differences:

- `files`: each file becomes one data item keyed by its filename (or the key before `=`), with the whole contents as the value.
- `literals`: key=value pairs.
- `envs`: each line `KEY=value` becomes its own key; pairs span a single line only.

Generated names get a content-hash suffix, such as `my-application-properties-f7mm6mhf59`.

The per-entry `options` field has the same subfields as `generatorOptions`: labels, annotations and `disableNameSuffixHash`.

Quick check: run kustomize build on the directory, then confirm each generated ConfigMap has the expected keys and that the Deployment references the suffixed name. Choose files for whole-file values, literals for a handful of keys, and envs when every line should become its own key.

## Checked

2026-11-03. Confirmed against: the configMapGenerator reference page and the task page.
Removed or reworded: the 'split at the first =' detail and the files-versus-envs comparison attributed to the task page.

Method: documentation only; no commands were run.
