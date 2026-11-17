---
id: computing-software.devops-ci-cd.gitlab-ci.kaniko-builds-args-and-cache
name: kaniko-builds-args-and-cache
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, kaniko-cache, kaniko-executor-args, kaniko-gitlab, daemonless-build]
level: practitioner
status: docs-checked
description: "Build images without a Docker daemon using the kaniko executor in GitLab CI: auth config, key flags, registry layer cache, snapshot modes, and its archived status."
sources: ["https://github.com/GoogleContainerTools/kaniko"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kaniko builds in GitLab CI

## 0. Status first
The upstream repository `GoogleContainerTools/kaniko` is archived: its README says the project
is no longer developed or maintained. Keep existing jobs pinned to a fixed executor version and
plan a move to another builder (BuildKit or buildah, see their skills).

## 1. Job
```yaml
build-image:
  image:
    name: gcr.io/kaniko-project/executor:<pinned-version>-debug   # pick a real tag; the debug variant has a shell
    entrypoint: [""]
  script:
    - |
      cat > /kaniko/.docker/config.json <<EOF
      {"auths":{"$CI_REGISTRY":{"username":"$CI_REGISTRY_USER","password":"$CI_REGISTRY_PASSWORD"}}}
      EOF
    - /kaniko/executor
        --context "$CI_PROJECT_DIR"
        --dockerfile "$CI_PROJECT_DIR/Dockerfile"
        --destination "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA"
        --build-arg "VERSION=$CI_COMMIT_SHORT_SHA"
        --cache=true --cache-repo "$CI_REGISTRY_IMAGE/cache"
        --snapshot-mode=redo
```
Kaniko reads registry credentials from `/kaniko/.docker/config.json`.

## 2. Flags (all in the kaniko README)
- `--destination` (repeatable), `--build-arg`, `--label key=value`, `--target <stage>`,
  `--skip-unused-stages`, `--reproducible`, `--single-snapshot`, `--registry-mirror`,
  `--use-new-run`.
- `--no-push` skips the image push but still pushes cache layers; add `--no-push-cache` to push
  nothing. `--tar-path <path>` saves the image as a tarball (needs `--destination`; add
  `--no-push` for tarball only).
- `--snapshot-mode=<full|redo|time>`: `full` is the default and most robust; `redo` considers
  mtime, size, mode, uid and gid and the README says it may be up to 50% faster with many files;
  `time` considers only mtime.
- `--compressed-caching=false` trades runtime for lower memory (try it on out-of-memory
  failures); default true.

## 3. Cache
- Opt in with `--cache=true`. `--cache-repo` names the remote repository for cached layers; if
  omitted it is inferred from `--destination` (`<destination repo>/cache`). `--cache-ttl` is in
  hours, default two weeks. `--cache-run-layers` defaults to true.
- A local cache directory (`--cache-dir`) is read-only for the build and must be populated with the
  `gcr.io/kaniko-project/warmer` image.

## 4. Gotchas
- Kaniko cannot use chroot or bind mounts, so it unpacks into its own container root and may
  overwrite anything already there: use one container per build.

## Verify
- [ ] A second build reuses cached layers for unchanged steps.
- [ ] The image appears in the project's container registry with the expected tags.

## Checked
2026-10-31. Confirmed in the kaniko README (archive notice, flag list and semantics, cache
defaults, warmer, config.json path, root/chroot note). The GitLab kaniko page returned a stub,
so GitLab-specific claims are limited to predefined registry variables.
Removed as unconfirmed: pinned executor tag, forks, `--cache-ttl 168h` example, BuildKit
`--mount=type=cache` unsupported claim, log message text, OOM memory advice beyond the flag.
Method: documentation only; no commands were run.
