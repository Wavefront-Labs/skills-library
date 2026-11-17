---
id: computing-software.devops-ci-cd.jenkins.scripted-node-stage-and-parallel
name: scripted-node-stage-and-parallel
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, scripted-parallel, node-block, scripted-pipeline]
level: practitioner
status: docs-checked
description: "Write scripted Jenkins pipelines with node, stage and parallel: dynamic branch maps, failFast, per-branch nodes and workspaces, and limiting parallelism."
sources: ["https://www.jenkins.io/doc/book/pipeline/syntax/#scripted-pipeline", "https://www.jenkins.io/doc/pipeline/steps/workflow-cps/#parallel-execute-in-parallel"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# node, stage and parallel in scripted pipelines

```groovy
def targets = ['linux', 'windows', 'mac']
def branches = [:]
for (t in targets) {
  def target = t                     // capture: closures see the loop variable by reference
  branches["test-${target}"] = {
    node(target) {
      checkout scm
      stage("Test ${target}") {
        sh "./test.sh ${target}"
      }
    }
  }
}
stage('Build') {
  node('linux') { checkout scm; sh 'make'; stash name: 'bin', includes: 'out/**' }
}
stage('Tests') {
  branches.failFast = true
  parallel branches
}
```

## Rules
- `node(label)` allocates an executor and a workspace; everything that touches files must be
  inside it. Code outside `node` has no workspace; keep it light.
- `parallel` takes a map of name to closure; `failFast: true` (map key) aborts siblings on first failure.

## Limiting concurrency
Parallel has no built-in throttle. Options: label capacity (executors), the `lock` step, or batching:
```groovy
branches.collate(5).each { batch -> parallel batch.collectEntries { it } }
```

## Gotchas
- Forgetting `def target = t` makes every branch use the last value.

## Verify
- [ ] Each branch appears in the run; a failure in one with failFast aborts the others.

## Checked

2026-10-28. Confirmed from the Pipeline Steps reference (`parallel` takes a map of branch names to closures and an optional `failFast` argument that terminates all branches when one fails) and the Pipeline syntax page (`lock` with `quantity` as used in an options example). Removed (not found): flyweight executor, `@2` workspace suffixes, claims about `stage`, flow-graph size and nested parallel rendering.

Method: documentation only; no commands were run.
