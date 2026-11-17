---
id: computing-software.devops-ci-cd.earthly.earthfile-run-secrets-mounts
name: earthfile-run-secrets-mounts
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, earthfile, secret, mount, cache-mount, ssh, aws, oidc, secret-file]
level: practitioner
status: docs-checked
description: "Pass secrets, cache or tmpfs mounts, ssh agent and AWS or OIDC credentials into an Earthfile RUN using --secret, --mount, --ssh, --aws and --oidc."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthfile/earthfile.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RUN --secret, --mount, --ssh, --aws, --oidc

## --secret
`--secret <env-var>=<secret-id>` or `--secret <secret-id>` exposes a secret as an env var (name defaults to the id).
```Dockerfile
release:
    RUN --push --secret GITHUB_TOKEN=GH_TOKEN github-release upload
```
```bash
earthly --secret GH_TOKEN="the-actual-secret-token-value" +release
```
An empty secret id is allowed for optional secrets: `ARG SECRET_ID=GH_TOKEN` then `--secret GITHUB_TOKEN=$SECRET_ID`, and run `earthly +release --SECRET_ID=""`. Do not use `ENV` for secrets; ENV values persist in the image.

## --mount
`--mount <mount-spec>` is comma-separated key=values: `type` (`cache`, `tmpfs`, `secret`), `target`, `mode`/`chmod` (octal), `id` (cache id for global caches, or secret id), `sharing` (`locked` default, `shared`, `private`; cache only).
```Dockerfile
ENV GOCACHE=/go-cache
RUN --mount=type=cache,target=/go-cache go build main.go
RUN --mount=type=secret,id=netrc,target=/root/.netrc curl https://example.earthly.dev/restricted/example-file-that-requires-auth > data
```
```bash
earthly --secret netrc="machine example.earthly.dev login myusername password mypassword" +base
earthly --secret-file netrc="$HOME/.netrc" +base
```
Mounts cannot be shared between targets, nor within one target when build args differ.

## --ssh
Gives the command access to the host ssh agent through `SSH_AUTH_SOCK`: `RUN --ssh git config --global url."git@github.com:".insteadOf "https://github.com/" && go mod download`. It is not related to the git section of the earthly config file.

## --aws and --oidc (experimental)
`--aws` makes host AWS credentials (env vars or ~/.aws) available; enable with `VERSION --run-with-aws 0.8`. `--oidc <oidc-spec>` works only with `--aws` and needs `VERSION --run-with-aws --run-with-aws-oidc 0.8`. Spec keys: `session-name`, `role-arn`, `region`, `session-duration` (default and AWS minimum 15 minutes, e.g. `20m`).

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthfile/earthfile.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
