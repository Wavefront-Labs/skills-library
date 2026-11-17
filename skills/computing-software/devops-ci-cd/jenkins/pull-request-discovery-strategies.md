---
id: computing-software.devops-ci-cd.jenkins.pull-request-discovery-strategies
name: pull-request-discovery-strategies
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, multibranch-pipeline, pr-discovery-strategy, discover-pull-requests, discover-branches, fork-pull-requests, trust-policy, merge-with-target, change-request, pr-head, github-branch-source, jenkinsfile-trust]
level: practitioner
status: gated
description: "Choose Jenkins multibranch discovery traits: branch strategy to avoid double builds, PR merge vs head builds, fork PR trust policies and untrusted Jenkinsfile handling."
sources: ["https://plugins.jenkins.io/github-branch-source/", "https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/github-branch-source", "https://www.jenkins.io/doc/book/pipeline/multibranch/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pull request discovery strategies

Three traits decide what jobs a GitHub/Bitbucket multibranch source creates.

## 1. Discover branches
The GitHub Branch Source docs were not readable here, so the strategy names and what each builds are (gated: unconfirmed, source is paywalled or blocked). Check them in the plugin's UI help.

| Strategy (UI) | Use |
|---|---|
| Exclude branches that are also filed as PRs | default choice: a PR branch builds once, as the PR |
| Only branches that are also filed as PRs | rare |
| All branches | when branch builds must run even with an open PR (doubles load) |

## 2. Discover pull requests from origin
| Strategy | What is built |
|---|---|
| Merging the PR with the current target branch revision | merge of head + target; catches integration breaks |
| The current PR revision | head only; reproducible SHA |
| Both | two jobs per PR |

(gated: unconfirmed, source is paywalled or blocked) Merge builds test a synthetic merge
commit, so the commit differs from the PR head; use the head strategy if you need reproducibility.

## 3. Discover pull requests from forks
The same strategies plus a **trust** policy that decides whose Jenkinsfile is used. The
policy names (Nobody, Contributors, users with Admin or Write permission, Everyone) are
(gated: unconfirmed, source is paywalled or blocked); for untrusted PRs the base branch's
Jenkinsfile is used. The PR's *source code* still runs (it's what you build), so never
expose deploy credentials to PR builds: guard deploy stages with `when { not { changeRequest() } }`
(the `changeRequest` condition is documented in the Pipeline syntax reference).

## Pitfalls
- Changing strategies can rename PR jobs, which changes history and required check names;
  update branch protection accordingly.
- A fork contributor's Jenkinsfile edits not taking effect is the trust policy working.
- `env.CHANGE_ID` (the change request number) is set only on change-request jobs; see the
  Global Variable Reference for the others.

## Verify
Open a PR from a branch and a fork; the scan creates the expected jobs per PR.

## Checked
2026-11-02. Confirmed against the Pipeline multibranch page (pull-request support via branch source plugins, CHANGE_ID) and the Pipeline syntax reference (changeRequest condition). The GitHub Branch Source strategy names, trust policy names and merge/head behaviour could not be read from official docs here and carry the gated marker. Removed: Job DSL strategy ids and trait names, job-name suffixes, log message, other CHANGE_* variable names.
Method: documentation only; no commands were run.
