---
id: computing-software.devops-ci-cd.jenkins.fork-pull-request-trust-policies
name: fork-pull-request-trust-policies
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, fork-pr-trust, multibranch-pipeline, github-branch-source]
level: advanced
status: docs-checked
description: "Configure fork PR trust in Jenkins multibranch (GitHub/Bitbucket sources) so untrusted contributors cannot change the Jenkinsfile that runs with your credentials."
sources: ["https://github.com/jenkinsci/github-branch-source-plugin", "https://github.com/jenkinsci/workflow-multibranch-plugin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trust policies for fork pull requests

The GitHub Branch Source "Discover pull requests from forks" behaviour has a **Trust** setting deciding
whether the Jenkinsfile comes from the fork or from the target branch.

| Trust option | Jenkinsfile used for fork PRs |
|---|---|
| Nobody | all fork PRs untrusted: trusted files such as the Jenkinsfile come from the target branch (the fork's changes are ignored) |
| Collaborators | PRs from collaborators of the origin repository are trusted, all other forks untrusted; all collaborators count, even those with only read permission through a team; falls back to Nobody if the scan credential cannot list collaborators |
| Everyone | all fork PRs trusted; the plugin help calls this dangerous on public GitHub repositories |
| From users with Admin or Write permission | trusted only if the fork owner has Admin or Write on the origin repository; the plugin help calls this the recommended policy |

When a PR is untrusted, files that Jenkins requires to be trusted (the Jenkinsfile) are read from the
target branch, not the fork. Other files (scripts, Makefile) still come from the PR, so a malicious PR
can change `build.sh` that the trusted Jenkinsfile runs.

## Hardening
- Public repos: prefer *Nobody* or *From users with Admin or Write permission*, and do not expose
  credentials to PR builds:
  ```groovy
  when { not { changeRequest() } }       // deploy/publish stages
  ```
- Run PR builds on isolated, ephemeral agents (Kubernetes pods) with no access to production networks.
- Use folder-scoped credentials only in jobs/branches that need them; PR builds should not see them.
- `readTrusted 'subdir/file'` reads a file from the trusted revision (the path is slash-separated from
  the SCM root); Jenkins reports when such a file has been modified in an untrusted revision.

## Verify
- [ ] A fork PR that edits the Jenkinsfile runs the target branch's version of the Jenkinsfile.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed in the GitHub Branch Source `ForkPullRequestDiscoveryTrait` trust help text and Messages.properties: the four trust policies and their semantics (including the collaborator fallback and the recommended policy); `readTrusted` path semantics and the untrusted-modification message (workflow-multibranch source). Removed the unconfirmed default setting, build-log wording and comment-based build strategy claims.
Method: documentation only; no commands were run.
