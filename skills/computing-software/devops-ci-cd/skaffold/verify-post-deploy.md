---
id: computing-software.devops-ci-cd.skaffold.verify-post-deploy
name: verify-post-deploy
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [verify, integration-test, kubernetescluster, job]
level: advanced
status: docs-checked
description: "Run post-deploy verification containers locally in Docker or as Kubernetes Jobs with skaffold verify."
sources:
  - "https://skaffold.dev/docs/verify/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Verification (Skaffold v2.0.0 and later) runs containers after deployment to check the result.

```yaml
verify:
- name: smoke
  container:
    name: smoke
    image: my-registry/smoke:latest
    command: ["./smoke.sh"]
  executionMode:
    kubernetesCluster:
      jobManifestPath: k8s/verify-job.yaml
```

Execution modes:

- Local Docker is the default.
- `kubernetesCluster` runs each verification as a Kubernetes Job. You can override the Job inline with JSON via `overrides`, or give a `jobManifestPath`.

Run only this stage:

```bash
skaffold verify -a build.json
```

The `-a` / `--build-artifacts` flag takes a file of pre-built images, such as the output of `skaffold build --file-output`, so verify uses those tags. `skaffold deploy -q | skaffold verify` is the documented piped form.

A verification container that exits non-zero fails the run: `skaffold verify` prints the error and exits with code 1, and exits 0 when all pass. Use it for smoke or integration checks against the deployed environment, separate from unit-level `test`.

Local mode runs the container with the `docker` CLI; cluster mode uses `kubectl` to run it as a Job. `--docker-network` names an existing Docker network for local runs, and `--env-file` sets environment variables in all verify containers.

## Checked

2026-11-09: confirmed against the Skaffold docs page "Verify" (source docs-v2/content/en/docs/verify.md), its sample verify.yaml and the `skaffold verify` section of the CLI reference: v2.0.0 or later, execution modes, overrides and jobManifestPath, exit codes, the `-a` and other flags. Removed unverified pipeline advice about image sizing, rollback jobs and log collection.

Method: docs-checked 2026-11-09 against skaffold.dev verify page and CLI reference (read as source markdown).
