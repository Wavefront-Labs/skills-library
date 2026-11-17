---
id: computing-software.qa-testing-engineering.selenium.grid-on-kubernetes-with-keda
name: grid-on-kubernetes-with-keda
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [grid-kubernetes, keda, selenium-grid, autoscaling, helm]
level: practitioner
status: docs-checked
description: "Run Selenium Grid on Kubernetes with the docker-selenium Helm chart and KEDA autoscaling: scaledJobs vs deployments, queue-based scaling, video and cleanup."
sources:
  - https://github.com/SeleniumHQ/docker-selenium/tree/trunk/charts/selenium-grid
  - https://keda.sh/docs/latest/scalers/selenium-grid-scaler/
  - https://github.com/SeleniumHQ/docker-selenium
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grid on Kubernetes with autoscaling (KEDA)

**Goal:** browser nodes scale with the session queue, from zero when idle to many during CI peaks.

## Install
```bash
helm repo add docker-selenium https://www.selenium.dev/docker-selenium
helm upgrade --install selenium-grid docker-selenium/selenium-grid -n selenium --create-namespace \
  --set isolateComponents=false \
  --set autoscaling.enabled=true \
  --set autoscaling.scalingType=job \
  --set chromeNode.scaledOptions.maxReplicaCount=20 \
  --set firefoxNode.scaledOptions.maxReplicaCount=10 \
  --set ingress.hostname=grid.example.test
```
`autoscaling.enabled=true` installs KEDA with the chart; to use an existing KEDA install enable autoscaling with `autoscaling.enableWithExistingKEDA` instead. `autoscaling.scalingType` is `job` (default) or `deployment`.

## Scaling types
- `job` (KEDA ScaledJob): the node drains after `nodeMaxSessions` sessions (default 1), so each pod is effectively one-time.
- `deployment` (KEDA ScaledObject): long-lived pods; the HPA picks pods to terminate at random, so a busy pod is only protected by `autoscaling.terminationGracePeriodSeconds` (default 3600) and the default preStop drain hook.

## The KEDA scaler
The KEDA `selenium-grid` trigger reads the Grid GraphQL URL and creates one browser node per pending queued request divided by the node's max sessions; one trigger per browser capability (`browserName`, `browserVersion`, `platformName`). Set `nodeMaxSessions` to match the node's `--max-sessions`. In the chart, `autoscaling.scaledOptions` (overridable per node type) holds `minReplicaCount`, `maxReplicaCount` and `pollingInterval`.

## Resources
- Chart defaults for a Chrome node: request 1 CPU and 1Gi memory, limit 1 CPU and 2Gi.
- By default `dshmVolumeSizeLimit` is empty: the `/dev/shm` mount is disabled and the browser gets `--disable-dev-shm-usage`; set e.g. `chromeNode.dshmVolumeSizeLimit: 2Gi` to mount it.
- The cluster's node pool autoscaler must add machines fast enough for CI peaks.

## Extras
- Video recording (`videoRecorder.enabled=true`); since chart 0.44.0 recording runs inside the node container unless `videoRecorder.sidecarContainer: true`. Uploads use rclone (for example an S3-compatible `destinationPrefix`).
- Basic auth (`basicAuth.enabled`) and an ingress with a TLS secret.

## Gotchas
- Capabilities in tests must match the trigger's `browserName`/`browserVersion`/`platformName` and the node stereotypes, or the right node type is not scaled.
- For ScaledJobs, review the chart's `successfulJobsHistoryLimit` (default 0) when debugging leftover job pods.

## Verify
Submitting 30 parallel sessions scales nodes up, all tests run, and nodes return to zero after the cooldown.

## Checked

Checked 2026-10-25 against the docker-selenium chart README and values.yaml (pushed 2026-10-20, images 4.51.0-20261010) and the KEDA documentation source for the selenium-grid scaler (kedacore/keda-docs, 2.22 tree). Confirmed: the helm repo URL, `isolateComponents`, `autoscaling.enabled`, `autoscaling.enableWithExistingKEDA`, `autoscaling.scalingType` (job default), `ingress.hostname`, `videoRecorder.enabled`, `autoscaling.terminationGracePeriodSeconds` default 3600 and the preStop drain hook, `nodeDrainAfterSessionCount` behaviour for job scaling, Chrome node default resources, `dshmVolumeSizeLimit` default, KEDA trigger semantics. Corrected: `chromeNode.maxReplicaCount` is `chromeNode.scaledOptions.maxReplicaCount`; `/dev/shm` is not an emptyDir by default.

Method: documentation only; no commands were run.
