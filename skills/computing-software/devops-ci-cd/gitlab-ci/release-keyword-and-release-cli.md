---
id: computing-software.devops-ci-cd.gitlab-ci.release-keyword-and-release-cli
name: release-keyword-and-release-cli
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, release-keyword, release-cli, gitlab-release, release-assets-links, glab-release]
level: practitioner
status: docs-checked
description: "Create GitLab releases from a tag pipeline with the release keyword: tag_name, description, asset links, milestones, and the glab image the keyword requires."
sources: ["https://docs.gitlab.com/ci/yaml/#release", "https://docs.gitlab.com/user/project/releases/release_cicd_examples/", "https://docs.gitlab.com/user/project/releases/release_fields/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The `release` keyword

## 1. Tag-pipeline release
```yaml
release:
  stage: release
  image: registry.gitlab.com/gitlab-org/cli:latest
  rules:
    - if: $CI_COMMIT_TAG =~ /^v\d+\.\d+\.\d+/
  script:
    - echo "Releasing $CI_COMMIT_TAG"
  release:
    tag_name: $CI_COMMIT_TAG
    name: "Release $CI_COMMIT_TAG"
    description: ./CHANGELOG-release.md        # file path relative to $CI_PROJECT_DIR (no spaces) or text
    milestones: ["$CI_COMMIT_TAG"]
    assets:
      links:
        - name: app-linux-amd64
          url: "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/generic/app/${CI_COMMIT_TAG}/app-linux-amd64"
          link_type: package
          filepath: /binaries/app-linux-amd64     # stable permalink .../releases/<tag>/downloads/binaries/...
```
The `release` keyword uses the `glab` CLI (`glab release create`), which must be in `$PATH`: use
`registry.gitlab.com/gitlab-org/cli:latest` on the Docker executor, or install `glab` on the host for the
Shell executor. The job must have a `script`; the `release` section runs after it and before
`after_script`, and only if `script` succeeded. (Older setups used `release-cli`; GitLab documents a
migration to `glab`.)

## 2. Release from a branch pipeline (creates the tag)
```yaml
  rules: [{ if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH }]
  release:
    tag_name: v$VERSION
    ref: $CI_COMMIT_SHA        # tag is created at this commit
    description: "Release v$VERSION"
```
If `tag_name` does not exist yet it is created at the pipeline's SHA (or `ref`); `tag_message` makes it an annotated tag.

## 3. Upload binaries first
`assets:links` entries point at files hosted elsewhere (for example the generic package registry);
upload them in an earlier job and link the URL, as in the first example.

## 4. Gotchas
- Release already exists → it is not updated and the job fails.
- `description` is evaluated by the shell that runs `glab`: variable syntax and escaping (for example backticks) depend on the shell.
- Authentication is `CI_JOB_TOKEN` by default; if `GITLAB_TOKEN`, `GITLAB_ACCESS_TOKEN` or `OAUTH_TOKEN` is defined in the job, `glab` uses that instead, and a token without API scope gives `401 Unauthorized`.
- `link_type` takes one of four values (runbook, package, image, other); `filepath` must start with `/`.

## Verify
- [ ] Deployments → Releases shows the release with working asset links.
- [ ] Permalink `/-/releases/permalink/latest/downloads/binaries/app-linux-amd64` downloads.

## Checked
2026-10-31. Confirmed in the GitLab CI/CD YAML reference (release keyword) and the release fields and release CI/CD examples pages: glab requirement and image, subkeys, ordering around `script`/`after_script`, existing-release failure, token precedence, description file rules, `filepath` and latest-release permalink format, `link_type` values.
Fixed: the skill named the `release-cli` image; the docs now use the glab image. Removed: the tag-pipeline and curl upload claims, the CLI one-liner, the dotenv and protected-tag claims.
Method: documentation only; no commands were run.
