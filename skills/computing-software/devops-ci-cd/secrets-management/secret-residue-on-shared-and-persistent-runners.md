---
id: computing-software.devops-ci-cd.secrets-management.secret-residue-on-shared-and-persistent-runners
name: secret-residue-on-shared-and-persistent-runners
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, runner-residue, self-hosted-runner-security, ephemeral-runners, workspace-cleanup, docker-credential-leak, ci-secrets]
level: practitioner
status: docs-checked
description: "Prevent secrets lingering on persistent or shared CI runners: credential file cleanup, isolated HOME, ephemeral runners and auditing a runner for residue."
sources:
  - https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners#self-hosted-runner-security
  - https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/autoscaling-with-self-hosted-runners#using-ephemeral-runners-for-autoscaling
  - https://docs.gitlab.com/runner/security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Secret residue on shared and persistent runners

A persistent runner reuses its filesystem between jobs. Anything a job writes outside its cleaned workspace survives for the next job, including jobs from other repos or untrusted PRs.

## Where secrets linger
| Location | Written by |
|---|---|
| `~/.docker/config.json` | `docker login` (base64 credentials, not encrypted) |
| Other credential files in the runner user's home (cloud CLIs, kubeconfig, package-manager auth, git credentials) | check each tool's docs for where it writes credentials |
| `/tmp`, tool caches, Docker build cache and images | build steps |
| Environment of leftover background processes | jobs that start daemons |

## Mitigations
1. **Ephemeral runners** (best): one job per VM/container, then destroy. For GitHub, register runners with `--ephemeral`.
2. Per-job isolated HOME: `export HOME=$RUNNER_TEMP/home` (GitHub cleans `RUNNER_TEMP` per job), `DOCKER_CONFIG=$RUNNER_TEMP/docker`.
3. Always log out in an `always()` step:
```yaml
- name: Cleanup credentials
  if: always()
  run: |
    docker logout ghcr.io || true
    rm -rf ~/.docker/config.json ~/.aws ~/.kube ~/.npmrc ~/.git-credentials
```
4. `actions/checkout` with `persist-credentials: false` when later steps don't push (credentials are persisted by default; recent versions keep them in a file under `RUNNER_TEMP`, older ones in the local git config).
5. Use short-lived OIDC credentials so leftovers expire in minutes.
6. Never run untrusted fork PRs on persistent self-hosted runners.
7. Separate runner groups per trust level; restrict which repositories can use each group.

## Audit an existing runner
```bash
sudo -u runner bash -c 'ls -la ~; cat ~/.docker/config.json 2>/dev/null | jq ".auths | keys"'
sudo <secret-scanner> ~runner /tmp <runner-work-dir>
docker images; docker ps -a; ps -u runner -o pid,etime,cmd
```
Found credentials: rotate them (assume exposure), then fix the workflow that wrote them.

## Verify
- [ ] A canary job that writes a dummy token to `~` is not visible to the next job (`test ! -f`).
- [ ] Production runners are ephemeral or reimaged per job; runner groups restrict repositories.

## Checked

2026-10-28. Confirmed: GitLab runner security page (`docker login` writes ~/.docker/config.json that every job on the runner can read; do not run it as the runner user on shared runners), GitHub ephemeral runners (`--ephemeral`), GitHub variables page (`RUNNER_TEMP` is emptied at the start and end of each job), Docker CLI reference (`DOCKER_CONFIG`, `docker logout`), actions/checkout README (`persist-credentials`, default true), and `always()` in workflow conditions. `aws eks update-kubeconfig` passed the command check. Removed: the per-tool credential file table rows, the Docker ARG and --secret claim, named runner controllers and executors, the GitHub public/private repo recommendation, and the secret-pattern regexes.

Method: documentation only; no commands were run.
