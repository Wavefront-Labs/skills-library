---
id: computing-software.devops-ci-cd.gitlab-ci.image-keyword-entrypoint-pull-policy-and-user
name: image-keyword-entrypoint-pull-policy-and-user
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, image-entrypoint, pull-policy, image-docker-user, image-platform, allowed-pull-policies]
level: practitioner
status: docs-checked
description: "Configure the job image fully: image name and digest pinning, overriding entrypoint for tool images, pull_policy and runner allowed_pull_policies, docker user and platform."
sources: ["https://docs.gitlab.com/ci/yaml/#image", "https://docs.gitlab.com/runner/executors/docker/#configure-how-runners-pull-images"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# image: name, entrypoint, pull_policy, docker options

## 1. Full form
```yaml
lint:
  image:
    name: hadolint/hadolint:<tag>@sha256:<digest>    # pin by digest for reproducibility
    entrypoint: [""]
    pull_policy: [if-not-present, always]
    docker:
      user: "1000:1000"
      platform: linux/arm64
  script: hadolint Dockerfile
```

## 2. entrypoint
`image:entrypoint` becomes the Docker `--entrypoint` option. Tool images whose entrypoint is the tool itself can swallow the job script; `entrypoint: [""]` clears it (see the GitLab docs topic "Override the entrypoint of an image").

## 3. pull_policy
- Values: `always`, `if-not-present`, `never`; an array lists several policies. If `pull_policy` is not set the default is `always`.
- The runner must allow it: `config.toml` `[runners.docker] allowed_pull_policies = ["always", "if-not-present"]`,
  otherwise the job fails with an error (if you omit `allowed_pull_policies`, the allowed list matches the `pull_policy` values).
- `if-not-present` speeds up big images but runs stale `:latest` forever — only use with pinned tags/digests.

## 4. docker:user and platform
- `image:docker:user` maps to `docker run --user`, and `image:docker:platform` maps to `docker pull --platform` (default: the runner host's platform).
- With the Docker executor, running an image built for a different architecture needs emulation support on the host (see the image:docker docs).

## Verify
- [ ] The job log shows the pinned digest being used.
- [ ] Tool image job runs the script, not the tool's usage text.

## Checked

2026-10-28. Confirmed on the CI YAML image section and the Docker executor page: image:entrypoint maps to docker --entrypoint, pull_policy values always/if-not-present/never and arrays, default always, allowed_pull_policies under [runners.docker] in config.toml, image:docker:user and platform mappings. Removed: the hadolint tag, named tool images and error symptoms, shell and distroless claims, exact error text, file-ownership claim, and the private image (DOCKER_AUTH_CONFIG) section, which these pages do not cover.
Method: documentation only; no commands were run.
