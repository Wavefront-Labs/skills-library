---
id: computing-software.devops-ci-cd.argo-rollouts.kubectl-plugin-install-and-completion
name: kubectl-plugin-install-and-completion
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [kubectl-plugin, install, completion, homebrew, mise, docker, argo-rollouts]
level: intro
status: docs-checked
description: "Install the kubectl argo rollouts plugin via Homebrew, mise, a manual binary or a container, and enable shell completion."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/installation/
  - https://argo-rollouts.readthedocs.io/en/stable/FAQ/
  - https://argo-rollouts.readthedocs.io/en/stable/features/kubectl-plugin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The kubectl plugin is optional but is the main way to view and drive rollouts from a terminal. Pick one install path.

```bash
brew install argoproj/tap/kubectl-argo-rollouts
mise use -g argo-rollouts
```

Manual install: download the release binary (for example `kubectl-argo-rollouts-darwin-amd64`; replace `darwin` with `linux` on Linux), `chmod +x` it, and move it onto your PATH as `kubectl-argo-rollouts`:

```bash
curl -LO https://github.com/argoproj/argo-rollouts/releases/latest/download/kubectl-argo-rollouts-darwin-amd64
chmod +x ./kubectl-argo-rollouts-darwin-amd64
sudo mv ./kubectl-argo-rollouts-darwin-amd64 /usr/local/bin/kubectl-argo-rollouts
kubectl argo rollouts version
```

The CLI is also a container image, `quay.io/argoproj/kubectl-argo-rollouts`, handy in CI: `docker run quay.io/argoproj/kubectl-argo-rollouts:master version`.

Completion. For `kubectl` 1.26 or newer, create an executable script named `kubectl_complete-argo-rollouts` on your PATH containing:

```sh
#!/usr/bin/env sh
kubectl argo rollouts __complete "$@"
```

For the standalone binary, `kubectl-argo-rollouts completion bash` (also zsh, fish, powershell) prints completion code, e.g. `source <(kubectl-argo-rollouts completion bash)`.

Keep the plugin reasonably current with the controller, since it only patches or reads Rollout fields and older clients may not understand newer spec fields. Verify with `kubectl argo rollouts version`, which prints the client version, and run `kubectl argo rollouts` to confirm the command list appears.

## Checked

2026-11-08. Confirmed against the Argo Rollouts installation page (read in full): brew, mise, manual binary steps, container image, kubectl 1.26 completion script, completion shells. The plugin version-skew note is from the FAQ (read in full) and the command list from the kubectl plugin page (read in full).

Removed or corrected: nothing; claims matched.

Method: documentation only; no commands were run.
