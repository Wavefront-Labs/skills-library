---
id: computing-software.ai-ml-engineering.ml-platform-engineering.orchestration-with-kubeflow-and-ray
name: orchestration-with-kubeflow-and-ray
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, kubernetes, kubeflow, ray, ray-train, ray-tune, workflow-orchestration, pipeline-dag, autoscaling, resource-quotas, job-scheduling, kubeflow-pipelines, slurm, cluster-scheduling]
level: advanced
status: draft
description: "Orchestrate ML jobs on shared infrastructure with Kubeflow Pipelines or Ray: DAG design, resource requests that avoid starving other jobs, and scheduler-level failure modes."
sources:
  - https://www.kubeflow.org/docs/
  - https://docs.ray.io/en/latest/train/train.html
  - https://docs.ray.io/en/latest/tune/index.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Orchestrating ML jobs: Kubeflow Pipelines vs Ray on shared infrastructure

**Goal:** run training/pipeline jobs on a shared cluster (Kubernetes or Ray) that get the resources they ask for, release them when done, and don't starve or get starved by other teams' jobs.

## 1. Choosing between them
- **Kubeflow Pipelines**: good fit when the unit of work is a **DAG of discrete steps** (preprocess → train → evaluate → register), each containerized independently, and you want each step's lineage, caching, and resource requests to be explicit and auditable in Kubernetes-native terms. Heavier to set up; pays off as the pipeline count and team count grow and you need standard tooling across teams.
- **Ray (Train/Tune/Serve)**: better fit for **Python-native distributed compute** where the unit of work is "run this function across N workers" rather than a container DAG — distributed data processing, hyperparameter sweeps (Ray Tune), or distributed training (Ray Train) that needs fine-grained control inside a single Python process group. Lower ceremony to get a single job running; pipeline-level lineage/caching is less built-in than Kubeflow's.
- Many platforms run **both**: Kubeflow (or Airflow/Argo) for the pipeline-level DAG and promotion gating, Ray as the compute engine for the distributed-training or hyperparameter-sweep step inside that DAG. Don't pick one to the exclusion of the other without checking whether the actual need is DAG orchestration or distributed compute — they're not substitutes.

## 2. Resource requests: the thing that breaks shared clusters
- Always set explicit CPU/memory/GPU **requests and limits** on every job — a job with no request can get scheduled onto a node another job already committed to, and a job with no limit can balloon and get OOM-killed (taking other pods on the node with it under memory pressure, depending on QoS class). "It worked once" without requests set is not evidence it's safe at scale.
- GPU requests are **not fractional** by default in vanilla Kubernetes device plugins — a pod asking for 1 GPU gets a whole GPU even if it uses 20% of it. If many small jobs need partial GPU, that needs a sharing layer (NVIDIA MPS, time-slicing config, or a scheduler plugin) deliberately set up — don't assume `resources.limits: {"nvidia.com/gpu": 1}` on Kubernetes gives you fractional sharing, because by default it doesn't.
- Set **priority classes / queues** (Kubeflow with Kueue, or Ray's placement groups with priority) so a long batch job doesn't block an interactive/urgent job indefinitely — without this, first-come-first-served scheduling means a 12-hour training job can starve a 2-minute debugging job for most of a working day.
- Namespace-level **resource quotas** prevent one team's runaway sweep (e.g. a hyperparameter search that launches 200 trials) from consuming the whole cluster and starving every other team — set these at the platform level, don't rely on individual users self-limiting.

## 3. Failure modes specific to orchestrated/distributed jobs
- **Zombie resources after a crashed driver**: if the orchestrating process (the Kubeflow pipeline step pod, or the Ray driver) dies without cleanup, worker pods/actors can be left running and holding GPUs indefinitely — set up liveness probes / job TTLs (`ttlSecondsAfterFinished` on Kubernetes Jobs, Ray's `ray.shutdown()` idempotent cleanup) so a crashed driver doesn't leak allocated resources silently for hours.
- **Pipeline step caching staleness**: Kubeflow Pipelines caches step outputs by input hash to skip redundant reruns — if a step reads from an external resource (a database query, an API) that changed without the step's declared inputs changing, the cache serves a stale result silently. Only rely on step caching for steps whose entire behavior is captured by their declared inputs.
- **Ray cluster version/dependency skew**: every Ray worker needs the same Ray version and (for most workloads) compatible Python/library versions as the head node — an autoscaled cluster that pulls a worker image with a different library version produces confusing remote-call errors far from the actual mismatch; pin and build worker images from the same base as the driver's environment.
- **Autoscaler lag**: Kubernetes cluster autoscaling (or Ray autoscaling) to add GPU nodes takes minutes, not seconds — a burst of submitted jobs expecting instant capacity will queue, and a platform that doesn't communicate "provisioning" state to users gets interpreted as "the scheduler is broken." Surface queue/provisioning status, don't just block silently.

## Verify
- [ ] Every submitted job has explicit CPU/memory/GPU requests and limits, not defaults.
- [ ] GPU sharing behavior (whole-GPU vs fractional) for the cluster is known and matches what the jobs actually need.
- [ ] Priority classes or queues exist so long batch jobs can't indefinitely starve short/interactive jobs.
- [ ] Namespace/team-level resource quotas are enforced at the platform level.
- [ ] Crashed-driver cleanup (Job TTLs, Ray actor cleanup) tested — resources don't leak after a killed driver process.
- [ ] Ray worker images pinned to the same library/Python versions as the driver environment.
