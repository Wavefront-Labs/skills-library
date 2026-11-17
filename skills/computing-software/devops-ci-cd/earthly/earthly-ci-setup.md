---
id: computing-software.devops-ci-cd.earthly.earthly-ci-setup
name: earthly-ci-setup
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, ci, strict, no-output, save-inline-cache, no-color, force-color, cni-mtu, buildkit-host]
level: practitioner
status: docs-checked
description: "Set up earthly in any CI: install and bootstrap, the --ci flag, --push, env vars NO_COLOR, FORCE_COLOR, CNI_MTU, EARTHLY_BUILDKIT_HOST, qemu binfmt, GitHub Actions."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/ci-integration/overview.md
  - https://github.com/earthly/earthly/blob/main/docs/basics/part-8a-using-earthly-in-your-current-ci.md
  - https://github.com/earthly/earthly/blob/main/docs/ci-integration/guides/gh-actions-integration.md
  - https://github.com/earthly/earthly/blob/main/docs/earthly-command/earthly-command.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Earthly in CI

Goal: run Earthly builds in an existing CI system.

Steps: install dependencies (`docker` and `git`; Earthly will not install them, and the prebuilt images already include them), install Earthly, log in to registries and set credentials, run Earthly.

## Install (direct)
```shell
wget https://github.com/earthly/earthly/releases/download/v0.8.13/earthly-linux-amd64 -O /usr/local/bin/earthly && \
chmod +x /usr/local/bin/earthly && \
/usr/local/bin/earthly bootstrap
```
Pin the version, and install as part of host provisioning rather than every build. Alternatively use the `earthly/earthly` image (built-in `earthly-buildkitd`, needs a source mount and an accessible `DOCKER_HOST`) or `earthly/buildkitd` (experimental).

## Key flags and variables
- `--ci`: the CI overview page calls it shorthand for `--save-inline-cache --strict --no-output`, but the command reference says it is an alias for `--no-output --strict` in target mode and `--strict` in artifact and image modes (no mention of inline cache). Strict mode blocks features that make builds less repeatable and disables local outputs; push results with `RUN --push` or `SAVE IMAGE --push`.
- `--push` pushes images and runs push-only commands.
- `NO_COLOR` / `FORCE_COLOR`: set to `1` to disable or force ANSI colors when Earthly misreads the terminal.
- `CNI_MTU`: fix a mismatch between external and internal MTU.
- `EARTHLY_BUILDKIT_HOST`: use an external BuildKit.
- Secrets: `--secret`, or Earthly cloud secrets. Earthly Cloud credentials: `earthly account create-token my-ci-token`.
- Cross-platform builds need binfmt_misc entries: `docker run --rm --privileged multiarch/qemu-user-static --reset -p yes` (once per physical machine).
- `earthly-buildkitd` must run `--privileged`; rootless is unsupported. User namespaces work if `buildkit_additional_args` includes `--userns host`.

## GitHub Actions
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    env:
      DOCKERHUB_USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}
      DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
      FORCE_COLOR: 1
    steps:
    - uses: earthly/actions-setup@v1
      with:
        version: v0.8.0
    - uses: actions/checkout@v4
    - name: Docker Login
      run: docker login --username "$DOCKERHUB_USERNAME" --password "$DOCKERHUB_TOKEN"
    - name: Run build
      run: earthly --ci --push +build
```
With Satellites add `--org <org-name> --sat <satellite-name>`; without `--sat` the build runs in the CI environment with limited caching.

## Gotcha
Do not set the `ref` option of `actions/checkout`: re-running an older commit no longer at branch head can produce inconsistent builds. Docker login avoids Docker Hub rate limiting.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: ci-integration/overview.md, basics/part-8a-using-earthly-in-your-current-ci.md, ci-integration/guides/gh-actions-integration.md, earthly-command/earthly-command.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: the CI overview says `--ci` expands to `--save-inline-cache --strict --no-output` but the command reference says `--no-output --strict` (target mode) or `--strict` (artifact and image modes); both are now stated. Added earthly-command.md to sources.

Method: documentation only; no commands were run.
