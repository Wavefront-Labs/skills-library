---
id: computing-software.devops-ci-cd.jenkins.job-dsl-pipeline-and-multibranch-jobs
name: job-dsl-pipeline-and-multibranch-jobs
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, pipelinejob, multibranchpipelinejob, job-dsl]
level: practitioner
status: draft
description: "Generate pipelineJob and multibranchPipelineJob definitions with Job DSL: SCM-backed Jenkinsfiles, GitHub branch sources, discovery traits and orphan strategy."
sources: ["https://jenkinsci.github.io/job-dsl-plugin/", "https://plugins.jenkins.io/job-dsl/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# pipelineJob and multibranchPipelineJob in Job DSL

## Pipeline job from SCM
```groovy
pipelineJob('team-a/nightly') {
  description('Nightly build (generated, do not edit in UI)')
  logRotator { numToKeep(30) }
  properties { pipelineTriggers { triggers { cron { spec('H 2 * * *') } } } }
  definition {
    cpsScm {
      scm { git { remote { url('https://github.com/org/app.git'); credentials('gh-app') }; branch('main') } }
      scriptPath('ci/Nightly.jenkinsfile')
      lightweight(true)
    }
  }
}
```

## Multibranch with GitHub branch source
```groovy
multibranchPipelineJob('team-a/app') {
  branchSources {
    branchSource {
      source {
        github {
          id('app-gh')                      // stable id: changing it re-creates all branches
          repoOwner('org'); repository('app')
          credentialsId('gh-app')
          repositoryUrl('https://github.com/org/app'); configuredByUrl(true)
          traits {
            gitHubBranchDiscovery { strategyId(1) }          // exclude branches filed as PRs
            gitHubPullRequestDiscovery { strategyId(1) }     // merge with target
            gitHubForkDiscovery { strategyId(1); trust { gitHubTrustPermissions() } }
          }
        }
      }
    }
  }
  factory { workflowBranchProjectFactory { scriptPath('Jenkinsfile') } }
  orphanedItemStrategy { discardOldItems { daysToKeep(7); numToKeep(20) } }
  triggers { periodicFolderTrigger { interval('1d') } }
}
```

## Gotchas
- The generic `github {}` uses the dynamic DSL; check exact names in the API viewer
  (`/plugin/job-dsl/api-viewer/index.html`) for your plugin versions.
- Changing a branch source `id` drops build history.
- Seed job needs "Process Job DSLs" with Removed job action decided (ignore/disable/delete).

## Verify
- [ ] Seed run log lists "Added items"; the multibranch job indexes and finds PRs.
