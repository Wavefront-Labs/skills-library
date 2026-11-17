---
id: computing-software.ai-ml-engineering.mlops.cml-model-reports-on-pull-requests
name: cml-model-reports-on-pull-requests
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, cml, continuous-training, ci-cd, github-actions, dvc-metrics-diff, model-pr-review]
level: practitioner
status: docs-checked
description: "Post model metrics, metric diffs and plots as pull-request comments with CML and DVC in GitHub Actions or GitLab CI, including cloud GPU runners."
sources:
  - https://cml.dev/doc/usage
  - https://cml.dev/doc/ref/comment
  - https://cml.dev/doc/ref/runner
  - https://dvc.org/doc/command-reference/metrics/diff
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CML model reports on pull requests

**Goal:** every PR that touches data, features or training code shows its effect on model metrics right in the review thread.

## Minimal GitHub Actions workflow
```yaml
name: train-report
on: pull_request
permissions:
  contents: read
  pull-requests: write
jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: {fetch-depth: 0}          # needed to diff against main
      - uses: iterative/setup-cml@v2
      - uses: iterative/setup-dvc@v1
      - run: pip install -r requirements.txt
      - run: dvc pull && dvc repro       # or python train.py
      - name: Report
        env:
          REPO_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          echo "## Metrics vs main" >> report.md
          dvc metrics diff main --md >> report.md
          cml comment create --watermark-title="train-report" report.md
```
- `cml comment create` posts markdown. `--publish` (default true) uploads local images found in the report, but the default image host no longer accepts uploads: configure image hosting (see cml.dev/doc/image-hosting) before relying on images.
- Repeated `cml comment create` adds a comment per run. Use `cml comment update` with `--watermark-title` to edit one bot comment. The CML docs say `update` fails with the default GitHub token: use a personal access token for it.
- Without DVC, write your own `metrics.json` and render a table with a few lines of Python; `cml` only needs a markdown file.

## GPU training on cloud runners
```yaml
jobs:
  launch:
    runs-on: ubuntu-latest
    steps:
      - uses: iterative/setup-cml@v2
      - run: cml runner launch --cloud=aws --cloud-region=us-west --cloud-type=g5.xlarge --labels=cml-gpu --idle-timeout=600
        env: {REPO_TOKEN: "${{ secrets.PERSONAL_ACCESS_TOKEN }}", AWS_ACCESS_KEY_ID: ..., AWS_SECRET_ACCESS_KEY: ...}
  train:
    needs: launch
    runs-on: [self-hosted, cml-gpu]
```
Launching a runner needs a repo token with sufficient rights (see the CML runner docs for the exact scope). `--idle-timeout=<seconds>` terminates an idle instance (default 300) and `--cloud-spot` requests a preemptible instance.

## Gotchas
- Comparing against `main` needs `main`'s metrics: either committed `metrics.json` via DVC, or a stored artifact from the last main build.
- Keep data access credentials out of fork PR runs.

## Verify
- [ ] A PR shows one bot comment with a metrics diff table that updates on each push.
- [ ] Cloud runner terminates after idle timeout (check the console).
- [ ] Fork PRs don't expose secrets (check GitHub's documentation on fork workflow permissions).

## Checked

2026-11-02. Checked against cml.dev usage, comment and runner reference pages and the DVC metrics diff page. Confirmed: cml comment create/update, --watermark-title, REPO_TOKEN, --publish, runner flags (--cloud, --cloud-region, --cloud-type accepts native types, --labels, --idle-timeout in seconds, --cloud-spot), dvc metrics diff --md. Corrected: local image upload is not automatic with the defaults (the default image host no longer accepts uploads, so set up image hosting), and re-running create with the same watermark does not edit the comment (use update; update with the default GitHub token errors and needs a PAT). Removed: the dvc plots diff --show-vega and vl2png recipe and the claim that the instance self-terminates after the job (the docs describe idle-timeout termination), plus the fork-token and PAT-scope statements, which are GitHub behaviour not confirmed from the fetched pages.

Method: documentation only; no commands were run.
