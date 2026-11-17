---
id: computing-software.devops-ci-cd.argo-workflows.artifact-repository-ref
name: artifact-repository-ref
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [artifact-repository-ref, artifact-repositories, default-artifact-repository, s3-bucket, repository-configmap]
level: practitioner
status: docs-checked
description: "Define shared artifact repositories in a ConfigMap, choose a default key by annotation, and override per Workflow with spec.artifactRepositoryRef."
sources: ["https://argo-workflows.readthedocs.io/en/latest/artifact-repository-ref/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Artifact repository ref
Reduce duplication and keep credentials out of templates by defining repositories once in a ConfigMap, placed in either the workflow's namespace or the managed namespace.

- Name the ConfigMap `artifact-repositories` to use it by default; any other name is chosen with `artifactRepositoryRef.configMap`.
- Each `data` key holds a YAML repository definition, e.g. an `s3` block with `bucket`, `endpoint`, `insecure`, `accessKeySecret` and `secretKeySecret` (each a secret `name` and `key`).
- The annotation `workflows.argoproj.io/default-artifact-repository` on the ConfigMap names the key used when a workflow does not pick one.

Override in a Workflow:

```yaml
spec:
  artifactRepositoryRef:
    configMap: my-artifact-repository   # default "artifact-repositories"
    key: v2-s3-artifact-repository      # default from the annotation
```

The feature pays off most when combined with key-only artifacts, where templates name only the artifact key.

Each key under `data` is one repository, so a single ConfigMap can hold several, such as `default-v1-s3-artifact-repository` and `v2-s3-artifact-repository`.

## Checked
2026-11-03. Confirmed against the Argo Workflows Artifact Repository Ref page: ConfigMap placement, the `artifact-repositories` default name, the default-artifact-repository annotation, the s3 fields, the `artifactRepositoryRef` override and the key-only artifacts note. Removed an uncited fields.md pointer.
Method: documentation only; no commands were run.
