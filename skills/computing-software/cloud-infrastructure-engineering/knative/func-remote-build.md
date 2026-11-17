---
id: computing-software.cloud-infrastructure-engineering.knative.func-remote-build
name: func-remote-build
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [on-cluster-build, deploy-remote, tekton, git-url, func-remote]
level: advanced
status: docs-checked
description: "Build functions on the cluster with func deploy --remote when no local Docker daemon exists."
sources:
  - https://knative.dev/docs/functions/building-functions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: build and deploy a function without a local Docker daemon, such as in CI/CD.

Instead of a local build, you can build on the cluster with `func deploy --remote`.

Prerequisites:
- The function must exist in a Git repository.
- The cluster must be configured to use Tekton Pipelines. The upstream on-cluster build documentation describes that setup.

The first time, you must specify the Git URL:

```bash
func deploy --remote --registry <registry> --git-url <git-url> -p hello
```

`kn func deploy` accepts the same flags. After you have specified the Git URL for your function once, you can omit it in later commands.

Direct upload: if the source code is on your local machine rather than in a Git repository, you can still do an on-cluster build without a Git URL. If you already specified a Git URL earlier and now want direct upload, pass the flag with an empty value: `func deploy --remote --git-url=""`.

Compare with local builds:
- `func build` builds an image on your machine and needs a Docker daemon.
- `func deploy --remote` moves the build onto the cluster through Tekton.

The private-registry note on the Functions pages (`FUNC_USERNAME`, `FUNC_PASSWORD`) lists the `host`, `s2i` and `pack` builders; it does not say whether on-cluster builds read those variables.

## Checked

2026-11-04. Confirmed against the Building functions page and its snippets (knative/docs source): on-cluster build with `func deploy --remote` when there is no Docker daemon or in CI/CD, the Git repository and Tekton Pipelines prerequisites, the first-run command with `--registry` and `--git-url`, omitting the Git URL afterwards, the direct-upload note with `--git-url=""`, and the local `func build` Docker daemon prerequisite. Spelled out the direct-upload command from the page. Replaced the claim about registry credentials for remote builds with what the page actually says.

Method: documentation only; no commands were run.
