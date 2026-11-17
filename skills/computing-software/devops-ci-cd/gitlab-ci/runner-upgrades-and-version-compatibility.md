---
id: computing-software.devops-ci-cd.gitlab-ci.runner-upgrades-and-version-compatibility
name: runner-upgrades-and-version-compatibility
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, runner-upgrade, runner-version-compatibility, runner-authentication-token, graceful-shutdown]
level: advanced
status: docs-checked
description: "Upgrade GitLab Runner fleets safely: version matching with GitLab, graceful SIGQUIT drains, version pinning, and migrating from registration tokens to glrt tokens."
sources: ["https://docs.gitlab.com/runner/#gitlab-runner-versions", "https://docs.gitlab.com/runner/commands/#signals", "https://docs.gitlab.com/ci/runners/new_creation_workflow/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runner upgrades and version compatibility

## 1. Compatibility rule
Keep runner **major.minor in step with GitLab**. Older runners may still work with newer GitLab and
vice versa, but features may be unavailable or misbehave when versions differ. Backward
compatibility is guaranteed between minor updates, yet some GitLab minor releases add features that
need a runner on the same minor, so upgrade runners alongside GitLab.

## 2. Drain, then upgrade
`SIGQUIT` = graceful: stop accepting new builds, exit once running builds finish. `SIGTERM`/`SIGINT`
abort all running builds and exit as soon as possible (sent twice: exit now). The runner docs suggest
registering the service with `KillSignal=SIGQUIT` so `systemctl stop` drains.
```bash
sudo systemctl kill -s SIGQUIT gitlab-runner     # wait until no jobs are running
# upgrade the package to the pinned <version>, then:
sudo systemctl start gitlab-runner && gitlab-runner --version
```
On Kubernetes give pods a termination grace period at least as long as your longest job, and pin the
chart and image versions explicitly (check the chart's values for the exact fields). Pin Docker
images to a version tag, never `latest`.

## 3. Rolling a fleet
Upgrade one runner per tag group first (canary), watch job failures, then the rest. Hold package
upgrades so unattended updates do not bump runners mid-day.

## 4. Registration token migration
The legacy registration-token workflow (`gitlab-runner register --registration-token`) is not
recommended; from GitLab 17.0 instance admins or group owners can disable it, and existing runners
keep working after the upgrade. New workflow: create the runner in the GitLab UI (Runners page) to
get an authentication token with the `glrt-` prefix, then
```bash
gitlab-runner register --non-interactive --url https://gitlab.example.com \
  --token glrt-XXXX --executor docker
```
When registration tokens are disabled, options such as tags, run-untagged and locked cannot be set at
registration; configure them on the runner in GitLab. Autoscaling setups (Helm chart, Operator) reuse one
runner configuration instead of creating a runner per job.

## Gotchas
- Helm: with `runnerRegistrationToken` on Kubernetes runners attached to GitLab.com, 17.0+ tries the legacy registration API; use the authentication token.

## Verify
- [ ] Every runner reports the same version after the upgrade.
- [ ] No job failures traced to the drain/upgrade window.

## Checked
2026-10-31. Confirmed in the GitLab Runner versions, signals and runner creation workflow docs pages: major.minor sync rule, SIGQUIT versus SIGTERM/SIGINT, `KillSignal=SIGQUIT`, 17.0 disable option, `glrt-` prefix, server-side options, Helm token behaviour.
Removed: pinned example versions, `shutdown_timeout`, `terminationGracePeriodSeconds` and `image.tag` field names, `apt-mark hold`, `POST /user/runners`, 18.0 removal plan, helper-image and metric claims (not found in the fetched pages).
Method: documentation only; no commands were run.
