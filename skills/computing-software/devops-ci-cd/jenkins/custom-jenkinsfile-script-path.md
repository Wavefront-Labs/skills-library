---
id: computing-software.devops-ci-cd.jenkins.custom-jenkinsfile-script-path
name: custom-jenkinsfile-script-path
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, multibranch-pipeline, script-path, jenkinsfile-location, build-configuration, remote-jenkinsfile-provider, monorepo, multiple-jenkinsfiles, pipeline-from-scm, lightweight-checkout]
level: practitioner
status: docs-checked
description: "Point Jenkins pipeline and multibranch jobs at a non-default Jenkinsfile path, run several pipelines from one monorepo, and use lightweight checkout or a remote Jenkinsfile."
sources: ["https://github.com/jenkinsci/workflow-multibranch-plugin", "https://github.com/jenkinsci/workflow-cps-plugin", "https://www.jenkins.io/doc/book/pipeline/syntax/", "https://github.com/jenkinsci/remote-file-plugin", "https://github.com/jenkinsci/pipeline-multibranch-defaults-plugin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom Jenkinsfile script path

## Setting it
- **Pipeline job**: *Pipeline -> Definition: Pipeline script from SCM -> Script Path*.
  It is a relative, `/`-separated location within the checkout (for example
  `ci/Jenkinsfile.release`); `Jenkinsfile` is conventional and eases a later move to multibranch.
- **Multibranch / org folder**: *Build Configuration -> Script Path*: a relative location within
  the checkout, default `Jenkinsfile` when left empty. The script always runs in the Groovy
  sandbox. Use `checkout scm` in the pipeline to fetch sources from the same location.

## Monorepo: one multibranch job per service
Create one multibranch job per service, each with its own script path
(`services/api/Jenkinsfile`, `services/web/Jenkinsfile`). Every job still sees every
commit, so gate stages with `when { changeset 'services/api/**' }` to avoid building unaffected services
(`changeset` accepts an Ant-style glob by default, case-insensitive; `comparator` can be `EQUALS` or
`REGEXP`).

## Lightweight checkout
With *Lightweight checkout* selected, Jenkins tries to obtain the script directly from the SCM
without a full checkout. It is more efficient, but you get no changelog or SCM polling from it
(a `checkout scm` during the build populates the changelog and initialises polling), build
parameters are not substituted into the SCM configuration, and only selected SCM plugins
support it.

## Jenkinsfile outside the app repo
- Shared library + a 3-line Jenkinsfile is the usual answer.
- Remote File plugin: a multibranch *Build Configuration* mode *by Remote Jenkins File Plugin*
  takes the script path from a separate SCM definition; good for platform-owned pipelines, but
  developers can no longer change their pipeline in the repo's own PRs.
- *Pipeline Multibranch Defaults* plugin: a default `Jenkinsfile` stored as a Groovy file in
  Config File Provider; every discovered branch, PR and tag is then assumed to have a Jenkinsfile.

## Gotchas
- The script path is per job, not per branch: a branch with a moved Jenkinsfile no longer matches.
- Check the scan log when nothing is discovered; a wrong script path is a likely cause.

## Verify
The scan log lists the expected branches and the build runs the Jenkinsfile at the configured path.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed: Script Path help texts in workflow-cps (Pipeline job) and workflow-multibranch plugins (relative location, default `Jenkinsfile`, sandbox, `checkout scm`); Lightweight checkout help text; `changeset` condition and comparators (Pipeline Syntax); Remote File plugin mode name and Multibranch Defaults behaviour (plugin READMEs). Removed the Job DSL snippet and log-line examples.
Method: documentation only; no commands were run.
