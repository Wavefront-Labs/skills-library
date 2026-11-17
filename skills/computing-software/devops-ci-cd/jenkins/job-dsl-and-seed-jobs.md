---
id: computing-software.devops-ci-cd.jenkins.job-dsl-and-seed-jobs
name: job-dsl-and-seed-jobs
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, job-dsl, seed-job, jobs-as-code, dsl-script, folder-dsl, multibranch-pipeline-job, pipeline-job, organization-folder-dsl, configure-block, removed-job-action, removed-view-action, jcasc-jobs, job-dsl-api-viewer, dsl-script-security, unclassified-job-dsl, dynamic-dsl, lookup-strategy, generated-jobs, bootstrap-jobs, gitops-jenkins-jobs]
level: practitioner
status: gated
description: "Define Jenkins jobs as code with Job DSL: a seed job or JCasC jobs block creating folders, pipelineJob and multibranchPipelineJob items, and configure{} for gaps."
sources: ["https://plugins.jenkins.io/job-dsl/", "https://github.com/jenkinsci/job-dsl-plugin/wiki", "https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/demos/jobs/README.md", "https://jenkinsci.github.io/job-dsl-plugin/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job DSL and seed jobs

**Goal:** every job on the controller is generated from Groovy in a reviewed repo; a
fresh controller rebuilds its job tree from JCasC + one seed run.

## 1. Bootstrap via JCasC (no clicking)
```yaml
jobs:
  - script: >
      pipelineJob('seed') {
        definition {
          cpsScm {
            scm { git { remote { url('https://git.example.com/platform/jenkins-jobs.git'); credentials('git-ro') }; branch('*/main') } }
            scriptPath('Jenkinsfile.seed')
          }
        }
      }
```
`Jenkinsfile.seed`:
```groovy
pipeline {
  agent { label 'small' }
  stages {
    stage('Generate') {
      steps {
        jobDsl targets: 'jobs/**/*.groovy',
               removedJobAction: 'DELETE'        // IGNORE | DISABLE | DELETE (gated: unconfirmed, source is paywalled or blocked)
      }
    }
  }
}
```
Run the seed on every push to the jobs repo (webhook). The `jobDsl` step's other options
(removed views/config files, lookup strategy, classpath, failure flags) are listed in the
plugin's Pipeline Syntax snippet generator; their exact names and values were not confirmed
here (gated: unconfirmed, source is paywalled or blocked).

## 2. The DSL you'll actually write
```groovy
// jobs/team-a.groovy
folder('team-a') { displayName('Team A'); description('Generated — do not edit by hand') }

multibranchPipelineJob('team-a/api') {
  branchSources {
    branchSource {
      source {
        github {
          // GitHub source options and traits: take the exact method names from the API viewer
          // (gated: unconfirmed, source is paywalled or blocked)
        }
      }
    }
  }
  factory { workflowBranchProjectFactory { scriptPath('Jenkinsfile') } }
  orphanedItemStrategy { discardOldItems { daysToKeep(7); numToKeep(20) } }
  triggers { periodicFolderTrigger { interval('1d') } }
}

pipelineJob('team-a/nightly-report') {
  parameters { stringParam('DAYS', '7', 'Window') }
  logRotator { numToKeep(30) }
  properties { disableConcurrentBuilds() }
  triggers { cron('H 3 * * *') }
  definition { cpsScm { scm { git('https://github.com/example/api.git', 'main') }; scriptPath('ci/nightly.Jenkinsfile'); lightweight(true) } }
}
```
Loop to generate many: `['api','web','worker'].each { svc -> multibranchPipelineJob("team-a/${svc}") { … } }`
or read a YAML inventory from the jobs repo (`readFileFromWorkspace('services.yaml')`,
then `new org.yaml.snakeyaml.Yaml().load(...)`).

## 3. Finding the syntax
The complete DSL API reference is the Job DSL API Viewer on your own controller:
`https://jenkins/plugin/job-dsl/api-viewer/index.html`. If a plugin option has no DSL method,
use a `configure {}` block.

## 4. configure {} for the rest
Raw XML edits when the DSL has no method:
```groovy
pipelineJob('x') {
  configure { node ->
    node / 'properties' / 'org.jenkinsci.plugins.workflow.job.properties.DurabilityHintJobProperty' {
      hint('PERFORMANCE_OPTIMIZED')
    }
  }
}
```
Get the XML by configuring one job by hand and reading its `config.xml`. Keep `configure` blocks in one helper file; they
break on plugin upgrades first.

## 5. Script security
DSL scripts run in the Groovy sandbox unless *Manage Jenkins → Security → Enable script
security for Job DSL scripts* is off (don't). The seed job's DSL needs approval for
non-whitelisted calls (`readFileFromWorkspace` is fine; `new File(...)` is not). Seed job
must be editable only by platform admins — it can create any job with any credential
binding. Give generated jobs `authorization { permission('hudson.model.Item.Build', 'team-a') }`
via the matrix-auth DSL rather than relying on global rights.

## 6. Relationship to JCasC and Jenkinsfiles
JCasC = controller config (plugins, clouds, credentials refs, the seed). Job DSL = the
**existence and wiring** of jobs. Jenkinsfile = what the job does. Keep them separate:
a DSL script that embeds a 200-line `definition { cps { script(...) } }` is a Jenkinsfile
in the wrong place — use `cpsScm` and point at the repo.

## 7. Migration from hand-made jobs
Export: `curl -u u:t https://jenkins/job/old/config.xml` → either reverse into DSL
(the "Job DSL Playground"/xml-to-dsl tooling is unofficial) or wrap the XML with
`configure` initially. Run the seed with `removedJobAction: IGNORE` on a staging controller
restored from backup; diff `config.xml` before/after (`jobDsl` logs "GeneratedJob" lines).

## Verify
- [ ] Deleting a job from the repo and running the seed removes it; re-adding recreates it with the same `id` (history kept for multibranch).
- [ ] A new multibranch job's first indexing queued no builds.
- [ ] The seed job fails when a referenced plugin is missing (`failOnMissingPlugin`).
- [ ] Fresh controller: JCasC → seed → full job tree in one run, no manual clicks.

## Checked
2026-11-02. Confirmed against the Job DSL plugin page and wiki: the API viewer path on a controller, the configure block for options without DSL methods, readFileFromWorkspace and the SEED_JOB variable exist, and the JCasC jobs demo (seed jobs via the jobs root). The jobDsl step option names, GitHub branch source trait names and strategy ids were not readable in official docs here; the removedJobAction line carries the gated marker and the other option details were removed or deferred to the API viewer.
Method: documentation only; no commands were run.
