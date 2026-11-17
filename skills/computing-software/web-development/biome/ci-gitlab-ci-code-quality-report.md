---
id: computing-software.web-development.biome.ci-gitlab-ci-code-quality-report
name: ci-gitlab-ci-code-quality-report
category: computing-software
field: web-development
product: biome
tags: [biome, gitlab-ci, code-quality, docker-image, reporter-gitlab, ghcr, entrypoint, colors-off]
level: practitioner
status: docs-checked
description: "Run Biome in GitLab CI from the official Docker image and publish a Code Quality report with --reporter=gitlab."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/recipes/continuous-integration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use the Biome Docker image `ghcr.io/biomejs/biome:latest` and clear its entrypoint, which is required for the image to work in GitLab CI. Write the gitlab reporter output to a JSON file and publish it as a `codequality` report artifact:

```yaml
stages:
  - quality

lint:
  image:
    name: ghcr.io/biomejs/biome:latest
    entrypoint: [""]
  stage: quality
  script:
    - biome ci --reporter=gitlab --colors=off > /tmp/code-quality.json
    - cp /tmp/code-quality.json code-quality.json
  artifacts:
    reports:
      codequality:
        - code-quality.json
  rules:
    - if: $CI_COMMIT_BRANCH
    - if: $CI_MERGE_REQUEST_ID
```

Notes from the example's comments: `--colors=off` keeps ANSI codes out of the JSON; the job runs for commits on branches and for merge requests. The `gitlab` reporter produces a GitLab Code Quality report (see the reporters skill).

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the paragraph restating the example structure beyond what its comments say and the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
