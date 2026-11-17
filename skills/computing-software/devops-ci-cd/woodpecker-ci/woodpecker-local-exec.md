---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-local-exec
name: woodpecker-local-exec
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [exec, local-execution, debugging]
level: practitioner
status: docs-checked
description: "Run Woodpecker workflows locally with woodpecker-cli exec and override metadata."
sources: ["https://woodpecker-ci.org/docs/usage/local-execution"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker local execution

`woodpecker-cli exec` runs workflow files from your checkout, so you can test changes before pushing. Run it from the repository, or pass `--repo-path`. The Docker backend needs a Docker daemon; the local backend runs commands on your host and does not reproduce the image environment.

```shell
woodpecker-cli exec .woodpecker/my-first-workflow.yaml
woodpecker-cli exec .woodpecker/
```

The backend is auto-detected; choose one with `--backend-engine docker` or `--backend-engine local`.

Override metadata to test conditions:

```shell
woodpecker-cli exec \
  --pipeline-event push \
  --commit-branch main \
  --commit-sha "$(git rev-parse HEAD)" \
  --repo octocat/hello-world \
  .woodpecker/my-first-workflow.yaml
```

Replay with a downloaded file via `--metadata-file pipeline-metadata.json`. Its format is only guaranteed for the same server and CLI version, so re-download after upgrades.

Environment and secrets: `--env GOFLAGS=-mod=readonly`. Secrets are not downloaded from the server; pass `--secrets deploy_token="$DEPLOY_TOKEN"` or `--secrets-file` pointing to a YAML map of names to values. Keep that file out of Git.

See the CLI reference for all `exec` flags.

## Checked

2026-11-03. Confirmed against: local-execution (exec, --backend-engine, metadata flags, --metadata-file warning, --env, --secrets, --secrets-file). Removed: nothing.

Method: documentation only; no commands were run.
