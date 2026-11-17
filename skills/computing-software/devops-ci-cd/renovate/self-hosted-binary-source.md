---
id: computing-software.devops-ci-cd.renovate.self-hosted-binary-source
name: self-hosted-binary-source
category: computing-software
field: devops-ci-cd
product: renovate
tags: [binary-source, containerbase, full-image, renovate]
level: advanced
status: docs-checked
description: "Choose how self-hosted Renovate gets tools like npm and go with binarySource install, global or hermit."
sources:
  - https://docs.renovatebot.com/self-hosted-configuration/#binarysource
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Renovate calls third-party tools to update lock files and checksums, such as `npm` for `package-lock.json` or `go` for `go.sum`. `binarySource` selects where they come from:

- `global`: use tools already installed on the host, for example `npm` installed globally.
- `install` (default): download and install tools at runtime if running in a Containerbase environment, otherwise fall back to `global`.
- `hermit`: use the Hermit tool installation approach.

The `docker` value needs Docker installed and the Docker socket available to Renovate. It is deprecated and the docs say it will be removed in the future.

Image choices:

- In an environment where runtime download and install of tools is not possible, use the "full" image.
- If you build your own image, for example by installing Renovate with `npm`, install all necessary tools globally before running Renovate so that `binarySource=global` works.

`containerbaseDir` is the directory used to cache downloads when `binarySource=docker` or `binarySource=install`. Set it if such downloads must be stored outside Renovate's regular `cacheDir`.

## Checked

2026-11-08: read the `binarySource` and `containerbaseDir` sections of the Self-Hosted Configuration page (raw source; partial read of that page). Confirmed the three `binarySource` values and the install default and fallback, the full-image advice, the own-image `global` advice, the deprecated `docker` mode and its requirements, and the `containerbaseDir` purpose. Removed the image-name, `constraints`, tool-cache-reuse and arm64 claims, which the sections do not state.
Method: documentation only; no commands were run.
