---
id: computing-software.devops-ci-cd.spinnaker.halyard-deploy-and-connect
name: halyard-deploy-and-connect
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [halyard, hal-deploy-apply, hal-version, deploy, ui-access, troubleshooting]
level: intro
status: draft
description: "Pick a Spinnaker version, deploy with hal deploy apply, reach the UI with hal deploy connect, and use hal deploy diff when a deployment misbehaves."
sources:
  - https://spinnaker.io/docs/setup/install/deploy/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
After providers, environment and storage are configured, the deploy sequence is short.

1. `hal version list` shows available versions with links to their changelogs.
2. `hal config version edit --version $VERSION` sets the one you want.
3. `hal deploy apply` deploys. If deploying to the local machine you may need `sudo hal deploy apply`.
4. `hal deploy connect` forwards port 9000 (Deck) and 8084 (Gate). Set up an SSH tunnel to the Halyard host if needed, then browse to localhost:9000.

A successful `hal deploy apply` does not mean the install is finished, especially for distributed Kubernetes installs. Errors such as `Connection refused` can simply mean not all containers are up yet. Wait, or check them with the provider's tooling, for example `kubectl get pods --namespace spinnaker`.

**If a deploy fails:** once you have had one successful deployment, `hal deploy diff` shows which of your changes may be the cause, and you can re-run `hal deploy apply` after fixing them. The page asks first-time failures to be raised on the community Slack.

**Upgrading** uses the same commands: list versions, edit the version, apply. The page points to publicly exposing Spinnaker and setting up authentication as follow-ups, and suggests backing up your configuration afterwards.

## Checked

2026-11-04. Command sequence, port forwarding, the not-yet-ready warning and the diff troubleshooting advice were confirmed on the Deploy Spinnaker and Connect to the UI page.

Method: documentation only; no commands were run.
