---
id: computing-software.devops-ci-cd.jenkins.replaying-pipeline-runs
name: replaying-pipeline-runs
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, replay-pipeline, replay, pipeline-development, shared-library-debugging, rebuild, replay-permission, jenkins-cli-replay, pipeline-iteration, script-security]
level: practitioner
status: docs-checked
description: "Iterate on a Jenkinsfile or shared library without commits using Replay: edit the main script and loaded libraries, permissions it needs, CLI replay, and why to port changes back."
sources: ["https://www.jenkins.io/doc/book/pipeline/development/#replay", "https://www.jenkins.io/doc/book/managing/cli/", "https://www.jenkins.io/doc/book/pipeline/shared-libraries/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replaying a run with an edited script

**Replay** (a completed Pipeline build's menu) allows quick modification and execution of an existing Pipeline without changing
the Pipeline configuration or creating a new commit. If the run references a Shared Library, the library code is shown and
modifiable on the Replay page too.

## When to use
- Fix a typo in a long pipeline without a commit + push + wait cycle.
- Debug a shared library: add `echo` lines to the library code in the replay editor; nothing is committed.
- Reproduce a failure with extra diagnostics (`sh 'env | sort'`, `sh 'ls -la'`).

## Rules
- Replay needs the dedicated "Run / Replay" permission, implied by "Job / Configure". Replay lets a user edit code that runs in
  the pipeline, so restrict the permission to people you trust.
- As long as the Pipeline contained syntactically correct Groovy and was able to start, it can be replayed.
- A replay is a new build: it may deploy if the pipeline deploys. Guard with a parameter or `when` while experimenting.
- Changes live only in that replayed run. **Port them back to git**; replay is a debugger, not a workflow.
- See the "Limitations" part of the Pipeline Development Tools page for what replay cannot do.

## Verify
Replay with an added `echo 'REPLAY TEST'`; the new build shows the line.

## Checked

2026-10-28. Confirmed in the Jenkins Pipeline development tools page: Replay edits and reruns a Pipeline without changing configuration or committing, shared library code is shown and modifiable, access control via the Run / Replay permission implied by Job / Configure, replay possible when the Groovy is syntactically correct. Removed: the replay-pipeline CLI command (not in the CLI page), sandbox and Overall/RunScripts claims, SCM-revision, build-record and untrusted-fork claims, and the example library file name. Sources kept; the CLI and shared-libraries pages were fetched but do not document replay.
Method: documentation only; no commands were run.
