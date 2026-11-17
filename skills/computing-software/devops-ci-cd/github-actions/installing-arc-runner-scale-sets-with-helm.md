---
id: computing-software.devops-ci-cd.github-actions.installing-arc-runner-scale-sets-with-helm
name: installing-arc-runner-scale-sets-with-helm
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, arc-helm-install, gha-runner-scale-set-controller, actions-runner-controller, runner-scale-set, arc-github-app-auth]
level: advanced
status: docs-checked
description: "Install Actions Runner Controller with the gha-runner-scale-set-controller and gha-runner-scale-set Helm charts, authenticate via GitHub App, and target it with runs-on."
sources: ["https://docs.github.com/en/actions/tutorials/use-actions-runner-controller/get-started", "https://docs.github.com/en/actions/how-tos/manage-runners/use-actions-runner-controller/deploy-runner-scale-sets", "https://docs.github.com/en/actions/how-tos/manage-runners/use-actions-runner-controller/authenticate-to-the-api", "https://docs.github.com/en/actions/concepts/runners/runner-scale-sets", "https://docs.github.com/en/actions/tutorials/use-actions-runner-controller/troubleshoot"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing ARC (runner scale sets) with Helm

## 1. Controller (once per cluster)
```bash
helm install arc --namespace arc-systems --create-namespace \
  oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller   # add --version <x.y.z> to pin
```

## 2. Auth: GitHub App (preferred over PAT)
App permissions — repo-level runners: Administration RW, Metadata R; org-level: Self-hosted runners RW.
```bash
kubectl create namespace arc-runners
kubectl create secret generic gh-app -n arc-runners \
  --from-literal=github_app_id=123456 \
  --from-literal=github_app_installation_id=7890123 \
  --from-file=github_app_private_key=app.private-key.pem
```

## 3. A scale set (one per runner flavour)
```yaml
# values-linux.yaml
githubConfigUrl: https://github.com/my-org        # org, repo, or enterprise URL
githubConfigSecret: gh-app
runnerGroup: default
minRunners: 1          # minimum idle runners; if both min and max are unset ARC scales with jobs, down to 0
maxRunners: 30
template:
  spec:
    containers:
      - name: runner
        image: ghcr.io/actions/actions-runner:latest
        command: ["<RUNNER_HOME>/run.sh"]   # run.sh in the runner user home of the official image
        resources: { requests: { cpu: "2", memory: 4Gi } }
```
```bash
helm install linux-x64 -n arc-runners -f values-linux.yaml \
  oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set   # add --version <x.y.z> to pin
```
```yaml
runs-on: linux-x64        # the installation (Helm release) name can be used as the runs-on value
```

## 4. Gotchas
- Helm cannot upgrade ARC because it does not upgrade or delete CRDs. GitHub's documented upgrade:
  uninstall every `gha-runner-scale-set` release, wait for cleanup, uninstall the controller, remove
  the `actions.github.com` CRDs if they changed, then reinstall.
- A scale set can have more than one label (support added in ARC 0.14.0), and a scale set belongs
  to only one runner group (`runnerGroup`).
- The listener pod runs in the controller namespace (`arc-systems` in the quickstart); its pods carry
  the label `app.kubernetes.io/component=runner-scale-set-listener`, which helps when runners never
  appear.
- Runners are ephemeral: collect logs from the controller, listeners and runners, since pods are
  short-lived.

## Verify
- [ ] `kubectl get pods -n arc-systems` shows the controller and a listener Running; GitHub's runner settings show the scale set.
- [ ] A test job with `runs-on: linux-x64` starts a pod and completes; the pod is deleted afterwards.

## Checked

2026-10-25, against GitHub Docs (ARC get started, deploy runner scale sets, authenticate to the API, runner scale sets concept, troubleshoot). Confirmed: controller and scale-set chart OCI paths, `arc-systems` quickstart namespace, GitHub App permissions and secret key names, `githubConfigSecret`, `runnerGroup`, `minRunners`/`maxRunners` semantics, `run.sh` runner command in the runner home directory, installation name usable in `runs-on`, upgrade procedure, listener pod label. Wrong earlier: scale sets can have more than one label (ARC 0.14.0+); the upgrade guidance (GitHub says uninstall all scale sets and the controller, then reinstall). Removed as unconfirmed: the cold-start time, pinned chart version, the public-repository fork note, and the `autoscalingrunnersets` check.

Method: documentation only; no commands were run.
