---
id: computing-software.devops-ci-cd.skaffold.apply-command
name: apply-command
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [apply, rendered, deploy, ci]
level: practitioner
status: docs-checked
description: "Deploy already-rendered manifests with skaffold apply, the second half of a render-then-apply pipeline."
sources:
  - "https://skaffold.dev/docs/workflows/ci-cd/"
  - "https://skaffold.dev/docs/references/cli/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`skaffold apply` deploys manifests that are already hydrated.

```bash
skaffold render --output rendered.yaml
skaffold apply rendered.yaml
```

This splits what `skaffold deploy` does in one step. The docs list the CI/CD building blocks as `build`, `render`, `apply`, `deploy` and `status-check`. `apply` works with any Kubernetes YAML, whether Skaffold generated it or not.

Pattern for a pipeline with an approval gate:

1. Job one: `skaffold build --file-output build.json`.
2. Job two: `skaffold render -a build.json --output rendered.yaml`; store `rendered.yaml` as the artifact to review. `-a` (`--build-artifacts`) takes the build result file so render does not rebuild.
3. After approval: `skaffold apply rendered.yaml`.

Benefits: the exact reviewed YAML is what gets applied, and apply does not build anything.

`skaffold apply` always uses `kubectl` to create the resources, whatever deployer the `skaffold.yaml` configures. Only a small part of the deploy config is honoured: `deploy.statusCheckDeadlineSeconds`, `deploy.kubeContext`, `deploy.logs.prefix`, `deploy.kubectl.flags`, `deploy.kubectl.defaultNamespace`, `deploy.kustomize.flags` and `deploy.kustomize.defaultNamespace`. In a multi-config project with conflicting deploy settings, apply will not work. After creating the resources it runs the built-in status check (`--status-check` controls it).

Use `skaffold run` instead when you want the whole sequence in one command with no gate.

Apply only deploys; it does not build or tag. If the rendered file still has unresolved image names, render was run without the build artifacts, so pass the build file with `-a` there.

## Checked

2026-11-04. Read the Skaffold "Continuous Delivery" page (docs/workflows/ci-cd) and the CLI reference sections for `skaffold apply` and `skaffold render`. Confirmed: the building-block list, apply always using kubectl and the seven honoured deploy fields, the multi-config conflict note, `render -a/--build-artifacts` and `--output`, `build --file-output`. Corrected: the earlier claim that the deployer settings choose how apply deploys (apply always uses kubectl). Removed: the claim that the apply job needs no builder tooling. Replaced the dead `/docs/cli/` source with the two pages above.
Method: documentation only; no commands were run.
