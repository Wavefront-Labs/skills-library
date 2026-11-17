---
id: computing-software.devops-ci-cd.skaffold.render-command
name: render-command
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [render, manifests, digest-source, hydrate]
level: practitioner
status: docs-checked
description: "Produce final hydrated Kubernetes manifests with skaffold render and control image references, namespace and labels."
sources:
  - "https://skaffold.dev/docs/renderers/"
  - "https://skaffold.dev/docs/references/cli/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`skaffold render` ("Generate rendered Kubernetes manifests") renders the final manifests: Skaffold replaces untagged image names in the manifests with the final tagged image names, possibly after an intermediate step of expanding templates (helm) or calculating overlays (kustomize). The renderer is chosen in the `manifests` section: `rawYaml`, `helm`, `kpt` or `kustomize`, and a combination of renderers can be used in one project.

```bash
skaffold render --digest-source=remote
skaffold render --digest-source local --offline --output out.yaml
skaffold render -a build.json --digest-source none --offline -o out.yaml
```

Flags from the CLI reference:

- `-a` / `--build-artifacts`: a file of pre-built images (a previous `skaffold build --file-output` result) to use instead of rebuilding.
- `-i` / `--images`: pre-built images, either tagged images or `NAME=TAG` pairs.
- `--digest-source`: `remote` skips builds and resolves image digests by tag from the remote registry; `local` builds images locally and uses the built digests; `tag` uses tags directly from the build; `none` uses tags directly from the manifests. If unspecified it defaults to `remote` for remote clusters and `tag` for local clusters like kind or minikube.
- `--offline`: do not connect to the Kubernetes API server for manifest creation and validation (helpful for GitOps with no cluster). No `metadata.namespace` is injected in this case.
- `-n` / `--namespace`: renders manifests containing the namespace. `-l` / `--label`: add custom labels, repeatable.
- `-o` / `--output`: file to write the rendered manifests to.
- Others include `--set` and `--set-value-file` (override templated manifest fields), `-t` / `--tag`, `--platform`, `-m` / `--module`, `-p` / `--profile`, `--enable-platform-node-affinity` and `--loud`.

Rendered output can later be applied with `skaffold apply`, described in the CLI reference as applying hydrated manifests to a cluster.

## Checked

2026-11-04. Read the Skaffold Render overview page and the `skaffold render` section of the CLI reference. Confirmed the renderers, flags and digest-source semantics and defaults. Removed: the claim that render never touches the cluster (without `--offline` it connects to the API server), the claim that a missing build file leaves images untagged, the claim that the deployer is irrelevant, and the GitOps diff advice (only `--offline` mentions GitOps). The CLI reference gives no short `-a` example beyond the file description.
Method: documentation only; no commands were run.
