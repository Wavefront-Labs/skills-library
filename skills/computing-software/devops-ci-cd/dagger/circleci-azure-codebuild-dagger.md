---
id: computing-software.devops-ci-cd.dagger.circleci-azure-codebuild-dagger
name: circleci-azure-codebuild-dagger
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, circleci, azure-pipelines, aws-codebuild, ci, dagger-cloud]
level: practitioner
status: docs-checked
description: "Install the Dagger CLI and call functions from CircleCI, Azure Pipelines and AWS CodeBuild configs, with the token wiring and checkout quirks each page states."
sources: [https://docs.dagger.io/0.21/getting-started/ci-integrations/circleci, https://docs.dagger.io/0.21/getting-started/ci-integrations/azure-pipelines, https://docs.dagger.io/0.21/getting-started/ci-integrations/aws-codebuild]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagger on CircleCI, Azure Pipelines and AWS CodeBuild (Dagger 0.21 docs)

Goal: in a YAML-config CI, install the CLI with the official script and run `dagger call`. In all three, the CLI finds or starts an engine on the runner and reports to Dagger Cloud if `DAGGER_CLOUD_TOKEN` is set. Install line used everywhere:

```shell
curl -fsSL https://dl.dagger.io/dagger/install.sh | BIN_DIR=$HOME/.local/bin sh
```

## CircleCI (`.circleci/config.yml`)

Examples use the `docker` executor with `cimg/base:2024.09` and `setup_remote_docker`; with other executors (for example `machine`) install Docker yourself. Token: a project environment variable `DAGGER_CLOUD_TOKEN`.

```yaml
version: 2.1
jobs:
  hello:
    docker:
      - image: cimg/base:2024.09
    steps:
      - setup_remote_docker
      - run:
          name: Install Dagger CLI
          command: curl -fsSL https://dl.dagger.io/dagger/install.sh | BIN_DIR=$HOME/.local/bin sh
      - run:
          name: Call Dagger Function
          command: dagger -m github.com/shykes/daggerverse/hello@v0.1.2 call hello --greeting="bonjour" --name="monde"
workflows:
  dagger:
    jobs:
      - hello
```

For test then build, use `checkout` in each job and `requires: [test]` on the build job. Gotcha from the page: CircleCI's test splitting is not available inside Dagger; distribute tests yourself or run them in one execution.

## Azure Pipelines (`azure-pipelines.yml`)

Needs an Azure DevOps org/project and an agent. Page quirk: use a full clone and a branch checkout, otherwise traces are orphaned in the Dagger Cloud UI.

```yaml
steps:
- checkout: self
  fetchDepth: 0
- script: git checkout $(Build.SourceBranchName)
- script: curl -fsSL https://dl.dagger.io/dagger/install.sh | BIN_DIR=$HOME/.local/bin sh
- script: dagger -m github.com/shykes/daggerverse/hello@v0.1.2 call hello --greeting="bonjour" --name="monde"
  env:
    DAGGER_CLOUD_TOKEN: $(DAGGER_CLOUD_TOKEN)
```

The secret must be mapped into each script step's `env` explicitly.

## AWS CodeBuild (`buildspec.yml`)

Token from Secrets Manager via `env.secrets-manager` (`DAGGER_CLOUD_TOKEN: "arn:aws:secretsmanager:...:dagger_cloud_token"`). Install in `phases.install` and add `export PATH=$PATH:$HOME/.local/bin/`; run tests in `pre_build` (`dagger -m github.com/kpenfound/dagger-modules/golang@v0.2.0 call test --source=.`) and `build-container ... publish --address=ttl.sh/my-app-$RANDOM` in `build`.

Related: computing-software.devops-ci-cd.dagger.github-actions-dagger, computing-software.devops-ci-cd.dagger.jenkins-teamcity-dagger.

## Checked

2026-11-07

Read in full from the docs source: ci-integrations/circleci.mdx, azure-pipelines.mdx and aws-codebuild.mdx, plus the snippets circle-hello.yml, circle-test-build.yml, azure-pipelines-hello.yml, azure-pipelines-test-build.yml, buildspec-hello.yml and buildspec-test-build.yml. Confirmed the install line, executors, test splitting note, full-clone and branch-checkout requirement, env mapping of the secret, secrets-manager entry, phases and PATH export. No corrections needed.

Method: documentation only; no commands were run.
