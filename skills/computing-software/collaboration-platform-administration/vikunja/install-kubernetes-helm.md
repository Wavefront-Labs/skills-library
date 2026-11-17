---
id: computing-software.collaboration-platform-administration.vikunja.install-kubernetes-helm
name: install-kubernetes-helm
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, helm-chart, kubernetes-deploy, require-availability, third-party-charts]
level: intro
status: docs-checked
description: "Deploy Vikunja on Kubernetes with the official Helm chart or the listed third-party charts, and make startup fail fast when an OIDC provider is down."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/k8s.mdx
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vikunja has an official Helm chart in the `go-vikunja/helm-chart` repository on GitHub; its README explains usage.

Third-party options listed in the docs:
- the Truecharts Vikunja chart
- the app-template chart from bjw-s-labs

Orchestrator tip from the config reference: setting `auth.openid.providers.<provider key>.requireavailability` to `true` makes Vikunja crash at startup if it cannot reach the OpenID provider, so Kubernetes restarts the pod until the provider is available. The option defaults to false.

## Checked

2026-11-04. Confirmed against the Vikunja Hosting with k8s page (setup/k8s: official chart repo and the two third-party charts) and config-raw.json (requireavailability default and its orchestrator note). Removed: the single-deployable, environment variable and UID or no-shell claims, which those pages do not state.

Method: documentation only; no commands were run.
