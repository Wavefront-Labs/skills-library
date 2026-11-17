---
id: computing-software.cybersecurity-defensive.authentik.outposts-overview
name: outposts-overview
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, outposts, proxy-outpost, ldap-outpost, integrations, prometheus]
level: practitioner
status: docs-checked
description: "Create and understand authentik outposts: which providers need them, service account token, Docker or Kubernetes integration, manual deployment and the metrics port."
sources:
  - https://docs.goauthentik.io/add-secure-apps/outposts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: deploy the component that serves LDAP, Proxy, RADIUS and RAC providers.

An outpost is a service that needs only a connection to the authentik API, not the wider internet, so it works in firewalled or air-gapped deployments. It is granted rights only to its configured application/provider pairs (and related objects like certificates).

## Create
**Applications > Outposts > Create**: set **Name**, **Type** (Proxy, LDAP, Radius, RAC), **Integration** (Docker, Kubernetes, or `----` to deploy manually), **Applications**, and optional advanced settings. Creation generates a service account and token with read access to outpost and provider configuration; the outpost uses the token to connect.

## Integrations
- authentik on Docker Compose: an integration for the local Docker socket is created automatically.
- authentik on Kubernetes with `kubernetesIntegration` true (default): an integration for the local cluster is created automatically.
Selecting an integration starts a background task that creates the container or deployment; follow it on **Dashboards > System Tasks**. Manual deployment has Kubernetes and Docker Compose guides.

## Behavior
Changes to the app or provider push an update to the outpost over websockets; the outpost also sends healthchecks over websockets.

## Metrics
Prometheus metrics at port `:9300/metrics`, unauthenticated, so Docker does not map it. The embedded outpost returns both outpost and core server metrics at that endpoint.

## Checked

Method: docs-checked 2026-11-09 against https://docs.goauthentik.io/add-secure-apps/outposts/ (read in full).
