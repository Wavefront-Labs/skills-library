---
id: computing-software.devops-ci-cd.dagger.github-actions-dagger
name: github-actions-dagger
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, github-actions, ci, dagger-for-github, ghcr, dagger-cloud, pull-request]
level: practitioner
status: docs-checked
description: "Run Dagger Functions in GitHub Actions with dagger/dagger-for-github, use Dagger Cloud engines, publish to ghcr.io, and test PRs by merge-ref URL."
sources: [https://docs.dagger.io/0.21/getting-started/ci-integrations/github-actions, https://docs.dagger.io/0.21/getting-started/ci-integrations/github]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagger in GitHub Actions (Dagger 0.21 docs)

Goal: call Dagger Functions from a workflow, optionally on a Dagger Cloud engine, and publish images or test PR branches.

## How it runs

The "Dagger for GitHub" action calls the Dagger CLI with your sub-command, module, function and args. The CLI finds or starts an engine inside the runner and sends telemetry to Dagger Cloud when `DAGGER_CLOUD_TOKEN` is set.

## Call a function

```yaml
name: dagger
on:
  push:
    branches: [main]
jobs:
  hello:
    name: hello
    runs-on: ubuntu-latest
    steps:
      - name: Call Dagger Function
        uses: dagger/dagger-for-github@v8.3.0
        with:
          version: "latest"
          module: github.com/shykes/daggerverse/hello@v0.1.2
          args: hello --greeting="bonjour" --name="monde"
          cloud-token: ${{ secrets.DAGGER_CLOUD_TOKEN }}
```

For a function on your checked-out repo use `actions/checkout@v4`, `verb: call`, `module: github.com/kpenfound/dagger-modules/golang@v0.2.0`, `args: test --source=.`. A second job with `needs: test` runs `build-container --source=. --args=. publish --address=ttl.sh/my-app-$RANDOM`.

## Dagger shell in a step

```yaml
      - name: Chain in dagger shell
        run: container | from alpine | file /etc/os-release | contents
        shell: dagger {0}
```

(preceded by a `dagger/dagger-for-github` step, as in the page's example).

## Dagger Cloud engine

Copy the Compute Token from Dagger Cloud settings > Tokens, store it as repo secret `DAGGER_CLOUD_TOKEN`, and set `dagger-flags: "--cloud"` on the action step. The CLI then uses a managed engine (persistent cache, extra compute) instead of one in the runner.

## SSH keys

```yaml
- name: Set up SSH
  run: |
    eval "$(ssh-agent -s)"
    ssh-add - <<< '${{ secrets.SSH_PRIVATE_KEY }}'
```

## Publish to ghcr.io

Give the job `permissions: contents: read, packages: write`, then call `module: github.com/daggerverse/dagger-ghcr-demo@v0.1.5` with `verb: call` and `args: build-and-push --registry=$DOCKER_REGISTRY --image-name=$DOCKER_IMAGE_NAME --username=$DOCKER_USERNAME --password=env://DOCKER_PASSWORD --build-context=github.com/daggerverse/dagger-ghcr-demo`, with env `DOCKER_REGISTRY: ghcr.io`, `DOCKER_IMAGE_NAME: ${{ github.repository }}`, `DOCKER_USERNAME: ${{ github.actor }}`, `DOCKER_PASSWORD: ${{ secrets.REGISTRY_PASSWORD }}`.

## Test a pull request without knowing its fork

GitHub's `/merge` ref resolves a PR. Pass it as a `Directory` argument or module ref:

```shell
dagger call foo --directory=https://github.com/ORGANIZATION/REPOSITORY#pull/NUMBER/merge
dagger call -m github.com/ORGANIZATION/REPOSITORY@pull/NUMBER/merge --help
```

Related: computing-software.devops-ci-cd.dagger.gitlab-ci-dagger.

## Checked

2026-11-07

Read getting-started/ci-integrations/github-actions.mdx and github.mdx in full (both slugs return 200), plus the five snippet files they embed: github-hello.yml, github-hello-shell.yml, github-test-build.yml, github-cloud-engine.yml and github-ghcr.yml. Confirmed the seven-step how-it-works flow, action version, call and shell examples, Cloud Engine steps (Compute Token under Tokens, DAGGER_CLOUD_TOKEN, dagger-flags --cloud), the SSH agent snippet, the ghcr.io permissions, module version and env, and the /merge pull-request URLs. Trimmed the unsupported claim that the first step installs the CLI. The external Dagger for GitHub marketplace page was not read.

Method: documentation only; no commands were run.
