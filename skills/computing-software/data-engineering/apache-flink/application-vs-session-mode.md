---
id: computing-software.data-engineering.apache-flink.application-vs-session-mode
name: application-vs-session-mode
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, application-mode, session-mode, per-job-mode, deployment, flink-kubernetes-operator]
level: practitioner
status: docs-checked
description: "Choose Flink application or session deployment mode: isolation, resource use, where main() runs, and how each looks on Kubernetes and YARN."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/overview/#deployment-modes
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/resource-providers/native_kubernetes/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/elastic_scaling/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/resource-providers/yarn/
  - https://github.com/apache/flink-kubernetes-operator/blob/main/docs/content/docs/custom-resource/overview.md
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Application vs session deployment modes

| | Application mode | Session mode |
|---|---|---|
| Cluster lifetime | one cluster per application, torn down when the application finishes | long-running, shared |
| `main()` runs | on the JobManager | on the client for CLI and SQL Client submissions; on the cluster when submitted through the REST API `/jars/:jarid/run-application` |
| Isolation | application-level (own JobManager and TaskManagers) | jobs compete for the same resources; a misbehaving job or a lost TaskManager affects every job on it |
| Startup cost | a cluster is started per application | no cluster start; the cluster already runs |
| Typical use | production streaming jobs | ad-hoc SQL, many small or short jobs, dev |

## Application mode
- The docs assume the user jars are on the classpath (`usrlib` folder) of the JobManager and TaskManagers: for example baked into the image (`local:///opt/flink/usrlib/job.jar`), or uploaded to a remote target with `kubernetes.artifacts.local-upload-enabled` and `kubernetes.artifacts.local-upload-target`.
- Multiple `execute()`/`executeAsync()` calls in one `main()` are allowed, but High Availability in application mode is only supported for a single streaming job or multiple batch jobs.
- Kubernetes native: `flink run-application -t kubernetes-application -Dkubernetes.cluster-id=orders -Dkubernetes.container.image.ref=registry/orders:1.4 local:///opt/flink/usrlib/orders.jar`.
- YARN: `flink run-application -t yarn-application ...`; the `yarn.provided.lib.dirs` option points at a remote copy of the Flink distribution to cut upload time.
- Kubernetes operator: a `FlinkDeployment` with `spec.job` set is application mode.

## Session mode
- Kubernetes operator: a `FlinkDeployment` without `spec.job` is a bare session cluster; `FlinkSessionJob` resources (linked by `spec.deploymentName`) submit jobs to it.
- Native: `kubernetes-session.sh -Dkubernetes.cluster-id=shared`, then `flink run -t kubernetes-session -Dkubernetes.cluster-id=shared job.jar`.
- SQL Gateway and SQL client typically use a session cluster.
- Size slots for the mix of jobs. The Adaptive Scheduler can run on a session cluster, but Reactive Mode (`scheduler-mode: reactive`) is only supported as a standalone application deployment.

## Choosing
Production streaming: application mode (isolation, independent upgrades and scaling, clean failure domains). Session mode when submission latency and resource sharing matter more than isolation.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub) and the flink-kubernetes-operator custom-resource overview (main). Confirmed: where `main()` runs per mode, HA limit for multi-job applications, `kubernetes-session` and `kubernetes-application` targets, `kubernetes.artifacts.local-upload-*`, `yarn.provided.lib.dirs`, Reactive Mode restrictions, `FlinkDeployment`/`FlinkSessionJob` semantics. Removed unconfirmed claims (startup times, per-job removal in 2.0, classloading advice).

Method: documentation only; no commands were run.

## Verify
- [ ] Each production job has its own JobManager (`kubectl get flinkdeployment`), or the session cluster's shared-risk is documented.
- [ ] Killing one job's TaskManager does not affect unrelated jobs.
