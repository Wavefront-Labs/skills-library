---
id: computing-software.devops-ci-cd.github-actions.self-hosted-runners
name: self-hosted-runners
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, self-hosted-runner, actions-runner, ephemeral-runner, jit-runner, actions-runner-controller, arc, runner-scale-sets, kubernetes, autoscaling, runner-groups, runner-labels, gpu-runner, arm64-runner, larger-runners, runner-security, public-repo-risk, docker-in-docker, runner-image, svc-sh, config-sh, network-egress, ci-infrastructure]
level: advanced
status: docs-checked
description: "Run GitHub Actions self-hosted runners safely: ephemeral/JIT runners, Actions Runner Controller scale sets, runner groups and labels, image hygiene and the public-repo risk."
sources: ["https://docs.github.com/en/actions/hosting-your-own-runners", "https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners-with-actions-runner-controller/about-actions-runner-controller", "https://github.com/actions/runner"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Self-hosted runners

**Goal:** run jobs on your own hardware (GPU, ARM, private network, big disks, cheaper
minutes) without turning the runner into a persistent foothold for whoever can open a PR.

## 1. Decide first: do you need them?
GitHub-hosted runners (including larger runners) cover many cases with zero ops. Self-host when you need: private-network access, hardware
GitHub doesn't sell, very high volume where cost wins, or data that must not leave your estate.

## 2. Threat model — read before installing
- A runner executes **arbitrary code from the workflow**. Anyone who can change a workflow
  (or trigger one with untrusted input) owns the box for that job.
- GitHub recommends self-hosted runners only for **private** repositories: forks of a public repository can run dangerous code on the runner via a pull request. Public repositories cannot use runners in a runner group by default.
- A non-ephemeral runner keeps workspace, Docker images, `~/.npm`, credentials helpers
  and background processes between jobs → cross-job and cross-repo leakage.
- Treat runner hosts like build-farm workers: no long-lived cloud keys on disk (use OIDC),
  egress restricted, no route to production admin planes unless that's the runner's sole job.

## 3. Ephemeral is the default you want
- Manual: `./config.sh --url https://github.com/<org> --token <REG_TOKEN> --ephemeral`; GitHub only assigns one job
  to an ephemeral runner, so each job gets a clean environment. Wrap it in a VM/container you destroy and recreate,
  and forward runner logs to external storage.
- GitHub recommends autoscaling with ephemeral runners, not persistent ones.
- **JIT runners**: the REST API (`generate-jitconfig`) creates ephemeral just-in-time runners.
- The registration token from `config.sh` expires after one hour.

## 4. Kubernetes: Actions Runner Controller (ARC) scale sets
```bash
# install the gha-runner-scale-set-controller chart first, then a scale set:
helm install linux-x64 --namespace arc-runners --create-namespace \
  --set githubConfigUrl="https://github.com/<org>" \
  --set githubConfigSecret=<k8s-secret-with-github-app-creds> \
  --set minRunners=0 --set maxRunners=40 \
  oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set
```
- Jobs target the scale set by its **installation name** or the `runnerScaleSetName` value: `runs-on: linux-x64`.
  Multiple labels can be assigned with `runnerScaleSetLabels` in `values.yaml` for more flexible routing.
- If you comment out both `minRunners` and `maxRunners`, ARC scales to the number of assigned jobs and back to 0; a
  non-zero `minRunners` keeps that many runners available.
- Container jobs, services and container actions need `containerMode` set to `dind` or `kubernetes`. The default `dind`
  image runs the Docker daemon as root; the rootless image needs `--privileged` pods and has known limitations.
- For repository- or organisation-level runners GitHub recommends authenticating ARC with a **GitHub App**; enterprise-level
  runners require a personal access token (classic).

## 5. Routing and governance
- **Runner groups** (org/enterprise): restrict which repos and which workflows may use
  a group. Put GPU or prod-network runners in a group limited to named repos.
- Labels on classic runners: `runs-on: [self-hosted, linux, arm64]` — the job needs a
  runner carrying *all* labels. A job with no matching runner stays queued and fails after 24 hours.
- Require approval for workflow runs from forks (see GitHub's "Approving workflow runs from forks").

## 6. Image hygiene and ops
- Bake toolchains into the runner image (Packer/Dockerfile), version it, rebuild weekly
  for patches.
- Runners self-update by default. `--disableupdate` (passed to `config.sh`) turns that off, for example for ephemeral
  runners in containers, but you must then update within 30 days of a release or the service stops queuing jobs to the
  runner (critical security updates block sooner).
- Monitor queue time; that's your capacity signal.

## Uncertainty
ARC chart names and values change between releases; check current ARC docs. Not hands-on verified here.

## Verify
- [ ] No self-hosted runner is reachable by any public repository.
- [ ] Runners are ephemeral (log shows de-registration after each job) or JIT.
- [ ] Runner groups restrict sensitive runners to named repos.
- [ ] No long-lived cloud credentials on the runner; OIDC used instead.
- [ ] Median queue time is tracked; scale-set `maxRunners` sized from it.
- [ ] Image has a rebuild cadence and a version tag recorded in job logs.

## Checked
2026-10-31. Confirmed in GitHub's self-hosted runner reference, add-runners, ARC (about and deploying/metrics) and REST self-hosted-runners pages: private-repo recommendation, ephemeral and JIT, one-hour registration token, `--disableupdate` and the 30-day rule, 24-hour queue timeout, scale-set routing and labels, `minRunners`/`maxRunners` behaviour, `containerMode` values, GitHub App versus PAT guidance, Helm chart name and `githubConfigUrl`/`githubConfigSecret`.
Removed or corrected: the claim that scale sets cannot use multiple labels, `--labels`/`--runnergroup` flags, `svc.sh` and docker prune commands, the controller chart path, hosted-runner feature claims.
Method: documentation only; no commands were run.
