---
id: computing-software.devops-ci-cd.jenkins.disable-concurrent-builds
name: disable-concurrent-builds
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, disableconcurrentbuilds, abort-previous, concurrent-builds, build-queue, options-directive, throttle-concurrent-builds, multibranch, queue-collapsing, quiet-period]
level: practitioner
status: docs-checked
description: "Use options { disableConcurrentBuilds() } correctly: queue vs abortPrevious, per-branch scope in multibranch, queue collapsing, and when throttle or lock fits better."
sources: ["https://www.jenkins.io/doc/book/pipeline/syntax/", "https://github.com/jenkinsci/workflow-job-plugin", "https://github.com/jenkinsci/throttle-concurrent-builds-plugin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# disableConcurrentBuilds

```groovy
pipeline {
  agent any
  options {
    disableConcurrentBuilds()                    // queue: next build waits for the running one
    // disableConcurrentBuilds(abortPrevious: true)  // newest wins: running build is aborted
  }
  ...
}
```
Scripted equivalent: `properties([disableConcurrentBuilds(abortPrevious: true)])` at the
top of the Jenkinsfile.

## Which mode
| Situation | Use |
|---|---|
| PR / feature branch CI: only the latest commit matters | `abortPrevious: true` |
| Deploy jobs that must not overlap, and must each finish | plain (queue) |
| Main branch builds that publish versioned artifacts | plain (queue), every commit gets a build |
| Limit across *different* jobs or a shared env | `lock` or Throttle Concurrent Builds category |

## Behaviour details
- Scope is the job; in multibranch each branch/PR is its own job, so two branches still
  run concurrently.
- With `abortPrevious: true` the older build is cancelled and its log shows `Superseded by`
  followed by the newer build; keep cleanup in `post { aborted {} }` idempotent.

## Gotchas
- Plain mode with a long `input` wait blocks every later build of that branch for hours;
  add a `timeout` on the input, or move approval to a separate deploy job.
- Matrix/parallel inside one build are unaffected; this only limits whole builds.
- Throttle Concurrent Builds plugin's `throttle(['category'])` step throttles the `node()` runs
  inside its block by category; it doesn't replace this option for one job.

## Verify
Trigger two builds quickly: in queue mode the second waits in the build queue; with
`abortPrevious` the first ends ABORTED with a `Superseded by` message.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed: `disableConcurrentBuilds()` and `disableConcurrentBuilds(abortPrevious: true)` declarative option (Pipeline Syntax); the `Superseded by` cancellation cause and `disableConcurrentBuilds` symbol (workflow-job source); `throttle(['category']) { node() {...} }` (Throttle Concurrent Builds README). Removed unconfirmed queue-collapsing and property-lifecycle claims.
Method: documentation only; no commands were run.
