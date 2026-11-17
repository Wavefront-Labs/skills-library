---
id: computing-software.cloud-infrastructure-engineering.kubernetes.argo-workflows-and-tekton-pipelines
name: argo-workflows-and-tekton-pipelines
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, argo-workflows, tekton, kubernetes-native-ci, pipelines, platform-engineering, ci-cd]
level: advanced
status: docs-checked
description: "Run CI and batch pipelines as Kubernetes resources with Argo Workflows (DAG templates, artifacts, cron) or Tekton (Tasks, Pipelines, workspaces, Triggers, Chains), and operate them."
sources: ["https://argo-workflows.readthedocs.io/en/latest/", "https://argo-workflows.readthedocs.io/en/latest/workflow-rbac/", "https://tekton.dev/docs/pipelines/", "https://tekton.dev/docs/triggers/", "https://tekton.dev/docs/chains/", "https://github.com/tektoncd/pipeline/blob/main/docs/hub-resolver.md", "https://github.com/tektoncd/pipeline/blob/main/docs/affinityassistants.md", "https://github.com/argoproj/argo-workflows/blob/main/docs/cost-optimisation.md", "https://github.com/tektoncd/cli/blob/main/docs/cmd/tkn_pipeline_start.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo Workflows and Tekton pipelines

Both run every step as a pod. Choose Argo Workflows for data/ML/batch DAGs and general
workflow automation; Tekton for CI/CD building blocks with supply-chain provenance.

## Argo Workflows
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata: {generateName: build-, namespace: ci}
spec:
  entrypoint: main
  serviceAccountName: workflow-runner
  ttlStrategy: {secondsAfterCompletion: 86400}
  podGC: {strategy: OnPodSuccess}
  arguments: {parameters: [{name: repo, value: "https://github.com/acme/api"}]}
  templates:
  - name: main
    dag:
      tasks:
      - {name: test,  template: run, arguments: {parameters: [{name: cmd, value: "make test"}]}}
      - {name: build, template: run, dependencies: [test], arguments: {parameters: [{name: cmd, value: "make image"}]}}
  - name: run
    inputs: {parameters: [{name: cmd}]}
    container: {image: golang:1.23, command: [sh, -c], args: ["{{inputs.parameters.cmd}}"]}
```
```bash
argo submit -n ci build.yaml --watch
argo logs -n ci @latest
argo cron create nightly.yaml            # CronWorkflow
```
Operate: reusable `WorkflowTemplate`/`ClusterWorkflowTemplate`; artifact repository
configured through the `artifact-repositories` ConfigMap (the default name; `artifactRepositoryRef`
selects another); the workflow archive stores completed workflows in Postgres, MySQL or MariaDB;
the workflow service account needs `create` and `patch` on `workflowtaskresults` at minimum (use a
dedicated service account, not `default`). By default pods are not deleted, so set `ttlStrategy`
(`secondsAfterCompletion`) and `podGC` (`strategy` one of `OnPodCompletion`, `OnPodSuccess`,
`OnWorkflowCompletion`, `OnWorkflowSuccess`) to clean up.

## Tekton
```yaml
apiVersion: tekton.dev/v1
kind: Pipeline
metadata: {name: build}
spec:
  params: [{name: repo-url}]
  workspaces: [{name: src}]
  tasks:
  - name: clone
    taskRef: {resolver: hub, params: [{name: name, value: git-clone}, {name: version, value: "<task-version>"}]}
    params: [{name: url, value: $(params.repo-url)}]
    workspaces: [{name: output, workspace: src}]
  - name: test
    runAfter: [clone]
    taskRef: {name: go-test}
    workspaces: [{name: source, workspace: src}]
---
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata: {generateName: build-run-}
spec:
  pipelineRef: {name: build}
  params: [{name: repo-url, value: "https://github.com/acme/api"}]
  workspaces:
  - name: src
    volumeClaimTemplate: {spec: {accessModes: [ReadWriteOnce], resources: {requests: {storage: 1Gi}}}}
```
```bash
tkn pipeline start build -p repo-url=https://github.com/acme/api -w name=src,volumeClaimTemplateFile=pvc.yaml --showlog
tkn pipelinerun logs -f --last
```
Operate: Triggers (`EventListener` + `TriggerBinding` + `TriggerTemplate`) for Git webhooks;
**Chains** signs TaskRuns, PipelineRuns and OCI images and supports `slsa/v1` attestations; the
hub resolver must be enabled (`enable-hub-resolver` in the `resolvers-feature-flags` ConfigMap);
the affinity assistant (default **coschedule workspaces** mode) co-schedules pods that share a
PVC-backed workspace on one node, and has a `disabled` mode if it blocks scheduling; the Tekton
Operator's `TektonConfig` has a `pruner` section to clean up old runs.

## Both
- Isolate CI in its own namespace/node pool; builds need resources and sometimes privileges.
- Prefer a daemonless image builder over Docker-in-Docker.
- Secrets via workload identity, not long-lived tokens in Secrets.

## Verify
- [ ] A run completes, artifacts/logs are retained per policy, and completed pods are garbage-collected.

## Checked

2026-10-25, against Argo Workflows docs (cost optimisation, fields, workflow RBAC, workflow archive, artifact repository ref, CLI pages), and Tekton docs (pipeline hub resolver and affinity assistants, Chains README and config, Triggers README, Operator TektonConfig, tkn pipeline start and pipelinerun logs). Confirmed: `ttlStrategy.secondsAfterCompletion`, `podGC.strategy` values, pods not deleted by default, `workflowtaskresults` create/patch RBAC, archive databases, `artifact-repositories` ConfigMap, `argo submit --watch`, `argo logs @latest`, hub resolver params and its feature flag, affinity assistant modes, Chains `slsa/v1`, Trigger CRD names, `tkn pipeline start -p/-w` with `volumeClaimTemplateFile`, `tkn pipelinerun logs -f --last`, Operator pruner. Removed as unconfirmed: the pinned git-clone task version, the 'kaniko forks' builder list, and the emissary executor attribution.

Method: documentation only; no commands were run.
