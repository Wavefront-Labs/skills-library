---
id: computing-software.devops-ci-cd.argo-workflows.container-set-template
name: container-set-template
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [container-set, containerset, empty-dir, dependencies, main-container]
level: practitioner
status: docs-checked
description: "Run several dependent containers in one Pod with containerSet, sharing an emptyDir, with rules for the main container, artifacts and caveats versus DAG."
sources: ["https://argo-workflows.readthedocs.io/en/latest/container-set-template/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ContainerSet template
A `containerSet` template runs multiple containers in a single Pod, so they share a host and can exchange data through a cheap `emptyDir` volume instead of a PVC. It avoids waiting for several Pods to start and removes the init and wait container overhead of separate steps, which can beat a DAG.

```yaml
containerSet:
  volumeMounts:
    - {mountPath: /workspace, name: workspace}
  containers:
    - name: a
      image: argoproj/argosay:v2
    - name: main
      image: argoproj/argosay:v2
      dependencies: [a]
```
The `workspace` volume is declared at template level under `volumes` (`emptyDir: {}`). Containers form a graph through `dependencies`.

Caveats:
- Enhanced depends logic is not available.
- It only runs container templates.
- Resource requests are summed over every container, which can cost more than a DAG.
- Meant for tens, not hundreds, of containers.
- All containers share one host's resources.

Inputs and outputs: as with container and script templates, only a container named `main` can load inputs and save outputs. Include a `main` container in any ContainerSet with artifacts. For base-layer artifacts `main` must finish last, making it the root of the graph; otherwise put all artifact paths on the shared workspace volume. Output parameters can read a path such as `/workspace/message` via `valueFrom.path`.

Resource requests: all containers start at once and a dependent container still holds its requests while waiting. If requests are large, set them so the sum is the most you need at one time (for a diamond a, b, c, d where b and c run together, the total must cover b plus c).

## Checked
2026-11-03. Confirmed against the Argo Workflows ContainerSet Template page: shared Pod and emptyDir, dependencies, the caveats, main container rules for inputs and outputs, and resource request summing. Nothing removed.
Method: documentation only; no commands were run.
