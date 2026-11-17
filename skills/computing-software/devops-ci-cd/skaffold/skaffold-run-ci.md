---
id: computing-software.devops-ci-cd.skaffold.skaffold-run-ci
name: skaffold-run-ci
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [run, ci, cd, build-file-output, deploy]
level: practitioner
status: docs-checked
description: "Use skaffold run, or the build, render, apply and deploy building blocks, in CI/CD pipelines."
sources:
  - "https://skaffold.dev/docs/workflows/ci-cd/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`skaffold run` is the simplest CI/CD command: build, tag (optionally push), deploy and monitor readiness once, then exit. It tails no logs by default (`--tail` enables it).

For finer control, the docs name these building blocks: `build`, `deploy`, `render`, `apply` and status-check.

```bash
skaffold build --file-output build.json --default-repo gcr.io/my-project
skaffold deploy --build-artifacts build.json
```

`--file-output` writes the built image references, and `deploy --build-artifacts` (or `-a`) consumes them, so build and deploy can run in separate jobs.

Other CI-friendly choices:

1. `--tag $GIT_SHA` to pin a deterministic tag.
2. `--status-check=false` or a tuned deadline for deploys that may be slow.
3. `skaffold render` to commit or review the YAML.
4. `skaffold delete` to remove a deployment.

Select the environment with `-p prod` and `--kube-context`.

The docs suggest "committing" a build by naming the file after the git state, for example `--file-output build-$STATE.json` with `STATE` taken from `git rev-list -1 HEAD --abbrev-commit`, then `skaffold deploy -a build-$STATE.json`. The file holds a `builds` list of `imageName` and `tag` pairs, with the digest appended to the tag.

`skaffold render --output render.yaml` hydrates manifests with the new image tags, and `skaffold apply render.yaml` sends them to the cluster through `kubectl` and then runs the status check. This split suits GitOps pipelines. Apply honours only a small subset of deploy settings, such as `deploy.statusCheckDeadlineSeconds`, `deploy.kubeContext` and the kubectl flags and default namespace, and it fails when a multi-config project has conflicting deploy settings.

## Checked

2026-11-09: confirmed against the Skaffold docs page "Continuous Delivery" (source docs-v2/content/en/docs/workflows/ci-cd.md) and the CLI reference for run (`--tail` defaults to false), build, deploy, delete and the `--kube-context`, `--default-repo` and `-p` flags. Removed unverified reproducibility advice, the claim that run renders as a distinct step, and local-cluster advice.

Method: docs-checked 2026-11-09 against skaffold.dev ci-cd page and CLI reference (read as source markdown).
