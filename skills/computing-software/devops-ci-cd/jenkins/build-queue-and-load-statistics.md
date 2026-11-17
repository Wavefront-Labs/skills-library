---
id: computing-software.devops-ci-cd.jenkins.build-queue-and-load-statistics
name: build-queue-and-load-statistics
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, load-statistics, jenkins-build-queue, controller-tuning]
level: advanced
status: docs-checked
description: "Diagnose a growing Jenkins build queue using load statistics, queue \"why\" reasons and the script console, then fix label starvation, throttles and cloud provisioning."
sources: ["https://github.com/jenkinsci/jenkins/blob/master/core/src/main/resources/hudson/model/Messages.properties", "https://github.com/jenkinsci/jenkins/blob/master/core/src/main/java/hudson/slaves/NodeProvisioner.java", "https://www.jenkins.io/doc/book/managing/nodes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build queue and load statistics

## Read the queue
Hover a queued item: the "why" text is the diagnosis.
| Why | Meaning |
|---|---|
| `Waiting for next available executor on 'linux'` | label capacity |
| `There are no nodes with the label 'gpu'` | typo or all such nodes offline |
| `A build is already in progress` | `disableConcurrentBuilds` or a non-concurrent job |
| `Blocked by '<reason>'` | a queue blocker such as a lock or throttle plugin (the text names it) |
| `In the quiet period. Expires in <time>` | quiet period still running |
| `All nodes of label '<label>' are offline` | every node with that label is offline; check the cloud or agents |

## Load statistics
`/label/<name>/load-statistics` (the *Load Statistics* link on a label page) graphs **queue length**,
**busy executors** and **total executors**, among other series. Queue > 0 while busy ==
total means capacity; queue > 0 while busy < total means label/restriction mismatch.

## Script console snapshot
```groovy
Jenkins.instance.queue.items.each { println "${it.task.fullDisplayName} | ${it.why} | ${(System.currentTimeMillis()-it.inQueueSince)/1000}s" }
```

## Fixes
- Capacity: more agents or a cloud with higher `containerCap`/instance caps; Kubernetes provisioning
  speed: the system properties `hudson.slaves.NodeProvisioner.initialDelay` and
  `hudson.slaves.NodeProvisioner.MARGIN` (a percentage, default 10) tune how eagerly cloud
  nodes are provisioned; change them only with measurements.
- Starvation of one label: split labels by workload, avoid single giant label.
- Many cheap jobs (indexing, PR scans) flooding: lower scan frequency, use webhooks.
- Controller executors at 0 (intended); flyweight tasks do not need executors.
- The Prometheus plugin can export queue metrics; alert on sustained queue time.

## Verify
- [ ] Queue wait p95 drops after changes (Prometheus or load statistics long timespan).

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed in Jenkins core source (jenkinsci/jenkins master): queue "why" message texts (`hudson/model/Messages.properties`), the label page *Load Statistics* link `/load-statistics` and its legends, and the `NodeProvisioner.initialDelay` and `.MARGIN` system properties (default 10). Removed the unconfirmed Prometheus metric name, the global Load Statistics path and lock-plugin message texts.
Method: documentation only; no commands were run.
