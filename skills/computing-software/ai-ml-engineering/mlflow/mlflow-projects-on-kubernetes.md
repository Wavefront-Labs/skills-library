---
id: computing-software.ai-ml-engineering.mlflow.mlflow-projects-on-kubernetes
name: mlflow-projects-on-kubernetes
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-kubernetes-backend, mlflow-projects, kubernetes-jobs, docker-env, mlproject]
level: practitioner
status: docs-checked
description: "Run MLflow Projects as Kubernetes Jobs: docker_env projects, backend config JSON, job templates, image push, tracking URI wiring and debugging failed pods."
sources:
  - https://mlflow.org/docs/latest/ml/projects/
  - https://github.com/mlflow/mlflow/blob/master/mlflow/projects/kubernetes.py
  - https://github.com/mlflow/mlflow/blob/master/mlflow/projects/docker.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MLflow Projects on the Kubernetes backend

**Goal:** `mlflow run` builds the project image, pushes it, and runs the entry point as a Kubernetes Job that logs to the shared tracking server.

## Requirements
- The MLproject uses `docker_env` (conda/python_env projects cannot run on this backend).
- A registry the cluster can pull from and your machine can push to.
- A kube context with permission to create Jobs in the target namespace.
- A tracking server reachable from inside the cluster (not `localhost`, not a local `mlruns` folder).

## Backend config
`kubernetes_config.json`:
```json
{
  "kube-context": "ml-prod",
  "repository-uri": "registry.example.com/ml/churn-train",
  "kube-job-template-path": "k8s/job-template.yaml"
}
```
`k8s/job-template.yaml`:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: "{replaced with MLflow Project name}"
  namespace: ml-jobs
spec:
  ttlSecondsAfterFinished: 86400
  backoffLimit: 0
  template:
    spec:
      containers:
      - name: "{replaced with MLflow Project name}"
        image: "{replaced with URI of Docker image created during Project execution}"
        command: ["{replaced with MLflow Project entry point command}"]
        resources:
          limits: {nvidia.com/gpu: 1, memory: 32Gi}
        env:
        - name: AWS_REGION
          value: us-east-1
      restartPolicy: Never
      serviceAccountName: ml-train
```
MLflow sets the Job name, container name, image and command and appends the environment variables `MLFLOW_RUN_ID`, `MLFLOW_TRACKING_URI` and `MLFLOW_EXPERIMENT_ID`; the namespace comes from your template. If the cluster must reach the tracking server at a different URI than your machine does, set `KUBE_MLFLOW_TRACKING_URI` on the client, which overrides the Job's `MLFLOW_TRACKING_URI`.

## Run
```bash
export MLFLOW_TRACKING_URI=https://mlflow.internal
mlflow run . --backend kubernetes --backend-config kubernetes_config.json -P epochs=20 --experiment-name churn
```
When the project is a git checkout, the image is tagged `<repository-uri>:<first 7 characters of the commit SHA>`, and the Job runs it by digest after MLflow pushes it. The project directory, including uncommitted files, is copied into the image, so commit first for reproducibility. `backoffLimit: 0` avoids duplicate runs on failure; retries should be a deliberate new run.

## Credentials
Artifact store access comes from the pod's service account (IRSA / Workload Identity), not baked into the image. Tracking server auth: inject `MLFLOW_TRACKING_TOKEN` or username/password from a Kubernetes Secret via `envFrom`.

## Debugging
- Run stuck in RUNNING after the pod died: inspect with `kubectl describe job` / `kubectl logs job/<name>`, then mark the run FAILED with `MlflowClient().set_terminated(run_id, "FAILED")`.
- ImagePullBackOff: registry auth (`imagePullSecrets`) or the push went to a different URI.
- For sweeps and DAGs, a workflow engine (Argo, Kubeflow, Airflow) launching the same image scales better than many `mlflow run` calls.

## Verify
- [ ] Job pod runs the expected image digest and the run's tags record the Docker image URI and ID.
- [ ] Metrics and artifacts appear on the tracking server from inside the cluster.
- [ ] Completed Jobs are cleaned up by `ttlSecondsAfterFinished`.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- Kubernetes backend requires a `docker_env` project (`validate_docker_env`), the config keys `kube-context`, `repository-uri`, `kube-job-template-path`, the 7-character SHA image tag, `tag@digest` Job image, overwritten name/image/command, appended env vars and `KUBE_MLFLOW_TRACKING_URI`: mlflow/projects/__init__.py, kubernetes.py, docker.py and utils.py.
- `mlflow run --backend kubernetes --backend-config`, `--build-image`, `-P`, `--experiment-name`: mlflow/cli/__init__.py and docs/classic-ml/projects/index.mdx (Kubernetes section); `set_terminated(run_id, status)`: MlflowClient.
- Removed as unconfirmed: the OOMKilled cause for stuck runs, and the claim that the run page shows the git commit for Kubernetes runs (the image URI and ID tags are what the code sets).

Method: documentation only; no commands were run.
