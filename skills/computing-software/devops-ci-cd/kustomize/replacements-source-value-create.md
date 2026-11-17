---
id: computing-software.devops-ci-cd.kustomize.replacements-source-value-create
name: replacements-source-value-create
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [replacements, sourcevalue, create, options]
level: practitioner
status: docs-checked
description: "Inject a literal with sourceValue and create missing target fields with options.create, as in setting a CPU limit across Jobs, Deployments and Pods."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/replacements/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`sourceValue` supplies a scalar instead of reading one resource; `options.create: true` adds the target field if missing (default `false`).

```yaml
replacements:
- source:
    kind: Secret
    name: my-secret
  targets:
  - select:
      name: hello
      kind: Job
    fieldPaths:
    - spec.template.spec.containers.[name=hello].env.[name=SECRET_TOKEN].value
- sourceValue: "500m"
  targets:
  - select:
      kind: Job|Deployment
    fieldPaths:
    - spec.template.spec.containers.*.resources.limits.cpu
    options:
      create: true
  - select:
      kind: Pod
    fieldPaths:
    - spec.containers.*.resources.limits.cpu
    options:
      create: true
```

Build output from the docs: the Job env `SECRET_TOKEN` value becomes `my-secret` (copied from the Secret's name, the default `metadata.name`); a `cpu: "500m"` limit is created in the Job and the Pod.

You can also keep a replacement in its own file referenced with `path: my-replacement.yaml`, with `source:` and `targets:` at the top level of that file, for example copying `spec.restartPolicy` from Pod `my-pod` into the Job with `create: true`.

The `create` option defaults to `false`; the page example sets it where `resources.limits` is absent.

## Checked

2026-11-03. Confirmed against: the replacements reference page.
Removed or reworded: the claim about what happens without create.

Method: documentation only; no commands were run.
