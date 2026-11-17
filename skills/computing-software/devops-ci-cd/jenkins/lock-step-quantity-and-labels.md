---
id: computing-software.devops-ci-cd.jenkins.lock-step-quantity-and-labels
name: lock-step-quantity-and-labels
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, lockable-resources, lock-step, lock-quantity, lock-label, resource-pool, mutual-exclusion, test-environments, variable-binding, inverse-precedence, declarative-lock-option, shared-environments]
level: practitioner
status: docs-checked
description: "Serialise access to shared environments in Jenkins with the lockable-resources lock step: named locks, label pools with quantity, the variable option, and fair queueing."
sources: ["https://plugins.jenkins.io/lockable-resources/", "https://www.jenkins.io/doc/pipeline/steps/lockable-resources/", "https://github.com/jenkinsci/lockable-resources-plugin/blob/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lock: quantity and labels

## Named lock (one environment)
```groovy
stage('Deploy staging') {
  options { lock(resource: 'staging-env') }      // declarative: whole stage holds the lock
  steps { sh './deploy.sh staging' }
}
```
A resource that doesn't exist is created on the fly as an ephemeral resource (removed
when unlocked), handy, but typos silently create a new lock and give no exclusion.
Define real ones under *Manage Jenkins -> Lockable Resources* or JCasC:
```yaml
unclassified:
  lockableResourcesManager:
    declaredResources:
      - name: "perf-env-1"
        labels: "perf-env"
      - name: "perf-env-2"
        labels: "perf-env"
      - name: "device-pixel8-1"
        labels: "android-device pixel8"
```

## Pool by label with quantity
```groovy
lock(label: 'perf-env', quantity: 1, variable: 'PERF_ENV') {
  sh 'echo "running against $PERF_ENV"; ./perf-test.sh --env "$PERF_ENV"'
}
```
- `quantity: 0` or omitted with `label` = lock **all** resources with that label.
- `variable` gets a comma-separated list of locked names; with quantity > 1 also
  `PERF_ENV0`, `PERF_ENV1`, ... (prefer the numbered ones: names may contain commas).
- `skipIfLocked: true`: skip the block instead of waiting.
- `inversePrecedence: true`: newest waiting build gets the lock first (pairs well with
  `milestone` to drop older builds).
- `extra: [[resource: 'db'], [label: 'gpu', quantity: 1]]`: acquire several at once
  atomically (avoids deadlock from nested locks taken in different orders).

## Rules
- Hold locks as briefly as possible and **outside** `node` if the wait could be long; the
  executor is held while queued for the lock otherwise.
- Use locks for external, finite things (envs, devices, licences). For "one build of this
  job at a time" use `disableConcurrentBuilds`.

## Gotchas
- Stuck lock after a hard kill: *Lockable Resources* page -> *Unlock* / *Reset*.
- Nested locks in opposite order across jobs can deadlock; use `extra` to take them together.
- `label` accepts expressions such as `labelA && labelB` or `labelA || labelB`.
  `resourceSelectStrategy: 'random'` randomises which free resource is chosen; the default
  `sequential` follows the order of the resource list, so the first resource is used most.
- `priority` (higher number served first) and `timeoutForAllocateResource` exist; do not
  mix `inversePrecedence` and `priority`.

## Verify
Start two builds needing `perf-env` quantity 1 with two resources: both run in parallel
with different `$PERF_ENV`; a third waits in the lock queue.

## Checked
2026-11-02. Confirmed against the lockable-resources step reference and plugin README: lock parameters (resource, label, quantity, variable and numbered variables, skipIfLocked, inversePrecedence, priority, extra, resourceSelectStrategy, timeoutForAllocateResource), ephemeral resources for undeclared names, all-resources meaning of quantity 0, JCasC lockableResourcesManager.declaredResources, Unlock/Reset actions. Corrected: label expressions are supported. Removed: controller-restart persistence and release-on-abort claims, exact log message.
Method: documentation only; no commands were run.
