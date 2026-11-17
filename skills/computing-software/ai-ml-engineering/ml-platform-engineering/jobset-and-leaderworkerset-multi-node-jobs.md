---
id: computing-software.ai-ml-engineering.ml-platform-engineering.jobset-and-leaderworkerset-multi-node-jobs
name: jobset-and-leaderworkerset-multi-node-jobs
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, jobset, leaderworkerset, kubernetes, multi-node-training, distributed-inference]
level: practitioner
status: docs-checked
description: "Run multi-node training with JobSet and multi-host inference with LeaderWorkerSet on Kubernetes: success policies, all-or-nothing restart and Kueue integration."
sources:
  - https://jobset.sigs.k8s.io/docs/overview/
  - https://lws.sigs.k8s.io/stable/docs/overview/
  - https://kueue.sigs.k8s.io/docs/tasks/run/jobsets/
  - https://docs.vllm.ai/en/latest/deployment/frameworks/lws/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# JobSet and LeaderWorkerSet for multi-node jobs

**Goal:** distributed training jobs and multi-host model servers run as single Kubernetes units with all-or-nothing handling and queue-based admission.

## JobSet (training, batch)
JobSet models a distributed workload as a group of Kubernetes Jobs (API `jobset.x-k8s.io/v1alpha2`, kind `JobSet`), so different groups of pods (leader, workers, parameter servers) can use different pod templates, which a single Job cannot do.
- Configurable success policies target specific ReplicatedJobs with operators for Any or All child jobs, e.g. complete when all pods of the "worker" ReplicatedJob finish.
- Startup sequencing (JobSet v0.6.0 and later) lets the leader run before workers start.
- Kueue integration: add the `kueue.x-k8s.io/queue-name` label on the JobSet (see the Kueue "Run JobSets" page for full examples). Before Kueue v0.8.1 you must restart Kueue after installing JobSet support.
- Make training resume from the latest checkpoint, since a failed attempt restarts work.

## LeaderWorkerSet (multi-host inference)
LWS deploys a group of pods as one unit of replication, aimed at multi-host inference where an LLM is sharded across devices on several nodes.
- Each replica is one leader plus a set of workers; there is a template for workers and an optional second one for the leader.
- Opt-in all-or-nothing restart: all pods in the group are recreated if one pod fails or a container restarts.
- Gang scheduling per replica is Alpha, so its API may change.
- See the vLLM LWS deployment page for a worked serving example.

## Placement
Use topology-aware scheduling (node selectors for the same fast-interconnect domain) so groups are not split across slow links.

## Verify
- [ ] Killing one worker pod restarts the whole group/job and training resumes from checkpoint.
- [ ] Kueue shows the workload admitted atomically, not partially.

## Checked
2026-11-01. Confirmed against the JobSet overview, LeaderWorkerSet overview and Kueue JobSet task pages: `v1alpha2` API version, multi-template jobs, success policies, startup sequencing (v0.6.0), Kueue queue label and the pre-v0.8.1 restart note, LWS leader/worker templates, opt-in all-or-nothing restart, Alpha gang scheduling. Removed (not confirmed on the pages read): the full YAML examples, torchrun and ray commands, stable-hostname pattern, `maxRestarts` and `completionMode` fields, `LWS_*` environment variables, `leaderworkerset.x-k8s.io/v1` version, rolling-update behaviour.
Method: documentation only; no commands were run.
